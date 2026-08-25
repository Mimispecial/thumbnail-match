from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "thumbnail_match.py"
SDK = "v0.2.16"
PROMPT = "Screen a declared thumbnail design"
BRIEF = "Create a thumbnail for a short public video showing how the library's seed exchange works. It should foreground a labeled seed envelope and the exchange drawer without promising free commercial seed."
OVERLAY = "Overlay text must be no more than five words, remain separate from the envelope label, and leave both required visual anchors unobstructed in the declared crop."


def campaign(vm, direct_deploy, owner):
    vm.sender = owner
    contract = direct_deploy(str(CONTRACT), "How the seed exchange works", BRIEF, OVERLAY, sdk_version=SDK)
    contract.add_visual_anchor("ENVELOPE", "A clearly visible paper seed envelope with a readable variety label.")
    contract.add_visual_anchor("DRAWER", "The library seed-exchange drawer is visible and not covered by overlay text.")
    contract.add_audience_segment("NEW", "Viewers who have never used a community seed exchange.")
    contract.add_audience_segment("MEMBER", "Existing library members familiar with the exchange drawer.")
    contract.open_designs()
    return contract


def submit(contract, candidate_id, overlay):
    contract.submit_design(candidate_id, "The declared layout shows a labeled tomato seed envelope in the foreground and the open library seed-exchange drawer behind it.", overlay, "The crop keeps the envelope label and full drawer visible, with open space at the upper left for the overlay.")


def test_screening_and_segment_vote_winner(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = campaign(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    submit(contract, "blue", "Swap Seeds in 3 Steps")
    direct_vm.sender = direct_charlie
    submit(contract, "green", "Library Seed Exchange")
    direct_vm.sender = direct_alice
    contract.lock_designs()
    direct_vm.mock_llm(PROMPT, json.dumps({"anchor_mask": "11", "layout": "CLEAR"}))
    contract.screen_design("blue")
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True
    contract.screen_design("green")
    contract.cast_segment_vote("NEW", "blue")
    direct_vm.sender = direct_bob
    contract.cast_segment_vote("NEW", "blue")
    direct_vm.sender = direct_alice
    contract.close_segment("NEW")
    assert contract.get_segment("NEW")["winner"] == "blue"


def test_designer_revision_and_tied_segment_stays_open(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = campaign(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    submit(contract, "blue", "Seed Exchange Guide")
    contract.revise_design("blue", "A labeled tomato seed envelope sits in front of the open library exchange drawer, and no other objects cover either anchor.", "Swap Seeds in 3 Steps", "The revised crop keeps both anchors clear and reserves the upper-left corner for text.")
    direct_vm.sender = direct_charlie
    submit(contract, "green", "Library Seed Exchange")
    direct_vm.sender = direct_alice
    contract.lock_designs()
    direct_vm.mock_llm(PROMPT, json.dumps({"anchor_mask": "11", "layout": "CLEAR"}))
    contract.screen_design("blue")
    contract.screen_design("green")
    contract.cast_segment_vote("MEMBER", "blue")
    direct_vm.sender = direct_bob
    contract.cast_segment_vote("MEMBER", "green")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("segment_vote_tie"):
        contract.close_segment("MEMBER")
    assert contract.get_candidate("blue")["revision_used"] is True


def test_owner_control_and_invalid_layout_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = campaign(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    submit(contract, "blue", "Swap Seeds in 3 Steps")
    direct_vm.sender = direct_charlie
    submit(contract, "green", "Library Seed Exchange")
    with direct_vm.expect_revert("only_campaign_owner"):
        contract.lock_designs()
    direct_vm.sender = direct_alice
    contract.lock_designs()
    direct_vm.mock_llm(PROMPT, json.dumps({"anchor_mask": "11", "layout": "POPULAR"}))
    with direct_vm.expect_revert("invalid_layout"):
        contract.screen_design("blue")
    assert contract.get_candidate("blue")["state"] == "SUBMITTED"
