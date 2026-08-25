from pathlib import Path
import json

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Screen a declared thumbnail design"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"anchor_mask": "11", "layout": "CLEAR"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_segment_vote_campaign():
    owner_account, first_designer, second_designer = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "thumbnail_match.py")
    deployed = factory.deploy_contract_tx(args=["How the seed exchange works", "Create a thumbnail for a public video about the library seed exchange, foregrounding a labeled envelope and the exchange drawer.", "Overlay text uses no more than five words and leaves both visual anchors unobstructed."], account=owner_account, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    address = extract_contract_address(deployed)
    owner = factory.build_contract(address, account=owner_account)
    first = factory.build_contract(address, account=first_designer)
    second = factory.build_contract(address, account=second_designer)
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
    ok(owner.screen_design(args=["blue"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.screen_design(args=["green"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    for segment in ("NEW", "MEMBER"):
        ok(owner.cast_segment_vote(args=[segment, "blue"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
        ok(first.cast_segment_vote(args=[segment, "blue"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
        ok(owner.close_segment(args=[segment]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert owner.get_state(args=[]).call()["phase"] == "COMPLETE"
