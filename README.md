# Thumbnail Match

Screens declared thumbnail layouts against frozen visual anchors, then lets separate audience-segment votes determine a winner for each segment.

## Why it is an Intelligent Contract

Return a fixed-order anchor mask and CLEAR, CROWDED, or MISMATCH for each declared design. GenLayer validators independently replay that semantic judgment before it becomes shared state. Anchor and segment setup, one design per address, one revision per design, eligibility, one vote per address per segment, tie rejection, and winner tallies are deterministic.

## Reusable deployment model

Deploy once per thumbnail campaign. Reuse the source in a fresh deployment with a different creative brief, anchors, audience segments, and candidates.

A completed deployment is an auditable record and is not reset or silently repurposed. Reuse means deploying the same reviewed source with new constructor data.

## Roles and workflow

The deployer owns the campaign. Each designer address may submit one candidate; any address can vote once per segment; only the owner closes segment tallies.

State path: `PLANNING → DESIGNS_OPEN → SCREENING → AUDIENCE_VOTE → COMPLETE`

## Evidence boundary

The stored creative brief, overlay rule, ordered visual-anchor declarations, audience-segment descriptions, and each candidate's declared visible elements, overlay text, and crop note. No image pixels are fetched.

## Core invariants

- At least two anchors and two audience segments freeze before designs open.
- Each designer address can submit one candidate and revise it at most once.
- Only CLEAR candidates can receive segment votes.
- AI cannot choose the campaign winner; each segment winner comes from at least two non-tied votes.

## Public interface

Write methods: `add_audience_segment, add_visual_anchor, cast_segment_vote, close_segment, lock_designs, open_designs, revise_design, screen_design, submit_design`

View methods: `get_candidate, get_policy, get_segment, get_state`

`get_policy` exposes the machine-readable operating boundary and confirms that this contract never custodies funds.

## Verification

Pinned GenVM runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

```powershell
python -m pip install -r requirements.txt
genvm-lint check contracts/thumbnail_match.py
genvm-lint typecheck contracts/thumbnail_match.py
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The StudioNet smoke test is opt-in and uses three disposable Mimi-only accounts protected outside the workspace. It asserts finalized successful execution and reads committed state with `LATEST_FINAL`.

## Final StudioNet proof

- Contract: https://explorer-studio.genlayer.com/address/0xeE296B9918cb6F8a7B02DAd234105E5c7f12FD93
- Studio import: https://studio.genlayer.com/?import-contract=0xeE296B9918cb6F8a7B02DAd234105E5c7f12FD93
- Deployment transaction: https://explorer-studio.genlayer.com/tx/0x14f5f077793388853ed44c69702514f3d96c937cf076fa0cf6c30c274f8034e7
- Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x8df1e8b453f29d46aaffa0d0c5295892dea036feeab77a064a2e415281103019
- Observed committed state: `{"anchor_mask":"11","layout":"CLEAR"}`
- Audited source SHA-256: `263c98b49512e0b26d3d4c0d9a1f0d1d5158277c6632ca55f933f7ac42f6c0c1`

## Limitations

- The contract screens declared layout text and does not inspect actual image pixels.
- Audience addresses are not demographic identities and votes do not predict click-through rate.
- Tied segment tallies must be resolved by additional product process outside this completed tally attempt.

## Repository map

- `contracts/thumbnail_match.py` — Intelligent Contract source
- `tests/direct` — hardened leader/validator and lifecycle tests
- `tests/integration/test_glsim_consensus.py` — five-validator simulator flow
- `tests/integration/test_studionet_smoke.py` — live opt-in proof
- `deployments/studionet.json` — source-bound public deployment evidence
- `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md` — reviewer material

License: MIT.
