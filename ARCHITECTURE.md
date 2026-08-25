# Architecture

## Deployment boundary

Deploy once per thumbnail campaign. Reuse the source in a fresh deployment with a different creative brief, anchors, audience segments, and candidates.

Constructor data establishes the deployment subject and fixed role boundary. Later writes add only the bounded records permitted by the lifecycle; a completed instance cannot be reopened.

## Participants

The deployer owns the campaign. Each designer address may submit one candidate; any address can vote once per segment; only the owner closes segment tallies.

Addresses are normalized before authorization comparisons. Role checks and lifecycle gates execute before semantic assessment.

## State machine

`PLANNING → DESIGNS_OPEN → SCREENING → AUDIENCE_VOTE → COMPLETE`

The phase-like field is the primary lifecycle lock. Each write advances that path, performs a documented bounded loop, or fails with an `[EXPECTED]` user error.

## Evidence assembly

The stored creative brief, overlay rule, ordered visual-anchor declarations, audience-segment descriptions, and each candidate's declared visible elements, overlay text, and crop note. No image pixels are fetched.

Before consensus, the contract normalizes bounded text, copies required storage into plain local values, serializes a sorted JSON packet, and places it between explicit START/END delimiters. Nondeterministic callbacks do not read contract storage.

## Consensus boundary

Return a fixed-order anchor mask and CLEAR, CROWDED, or MISMATCH for each declared design.

The leader callback validates exact JSON shape, field types, closed labels, masks or codes, and length bounds. A validator reruns the same semantic operation and rejects disagreement before state is committed.

## Deterministic boundary

Anchor and segment setup, one design per address, one revision per design, eligibility, one vote per address per segment, tie rejection, and winner tallies are deterministic.

Important invariants:

- At least two anchors and two audience segments freeze before designs open.
- Each designer address can submit one candidate and revise it at most once.
- Only CLEAR candidates can receive segment votes.
- AI cannot choose the campaign winner; each segment winner comes from at least two non-tied votes.

No method sends value, pays rewards, escrows assets, deletes external data, calls another contract, or invokes a webhook.

## Failure model

- Invalid caller input or lifecycle use raises `[EXPECTED]` and leaves state unchanged.
- Malformed or out-of-policy model output raises `[LLM_ERROR]` and cannot be stored.
- Validator disagreement cannot commit the semantic result.
- StudioNet proof reads explicitly target `LATEST_FINAL`, avoiding stale pre-final state.
