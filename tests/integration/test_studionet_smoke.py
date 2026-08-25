import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address


def ok(receipt):
    assert tx_execution_succeeded(receipt)
    assert receipt.get("status_name") == TransactionStatus.FINALIZED.value
    assert receipt.get("result_name") in (None, "AGREE", "MAJORITY_AGREE")
    assert receipt.get("tx_execution_result_name") in (None, "FINISHED_WITH_RETURN")
    return receipt


@pytest.mark.integration
def test_studionet_thumbnail_screen(default_account, secondary_account, tertiary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "thumbnail_match.py")
    deployed = ok(factory.deploy_contract_tx(args=["How the seed exchange works", "Create a thumbnail for a public video about the library seed exchange, foregrounding a labeled envelope and the exchange drawer.", "Overlay text uses no more than five words and leaves both visual anchors unobstructed."], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    owner = factory.build_contract(address, account=default_account)
    first = factory.build_contract(address, account=secondary_account)
    second = factory.build_contract(address, account=tertiary_account)
    ok(owner.add_visual_anchor(args=["ENVELOPE", "A clearly visible paper seed envelope with a readable variety label."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.add_visual_anchor(args=["DRAWER", "The library seed-exchange drawer is visible and not covered by overlay text."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.add_audience_segment(args=["NEW", "Viewers who have never used a community seed exchange."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.add_audience_segment(args=["MEMBER", "Existing library members familiar with the exchange drawer."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.open_designs(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    elements = "The declared layout shows a labeled tomato seed envelope in front of the open library exchange drawer."
    crop = "The crop keeps the envelope label and drawer visible, with upper-left space for overlay text."
    ok(first.submit_design(args=["blue", elements, "Swap Seeds in 3 Steps", crop]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(second.submit_design(args=["green", elements, "Library Seed Exchange", crop]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.lock_designs(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(owner.screen_design(args=["blue"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    candidate = owner.get_candidate(args=["blue"]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert candidate["layout"] in ("CLEAR", "CROWDED", "MISMATCH")
    observed = {"anchor_mask": candidate["anchor_mask"], "layout": candidate["layout"]}
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": observed}, sort_keys=True))
