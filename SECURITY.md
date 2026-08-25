# Security

## Scope

This repository contains one bounded Intelligent Contract, direct tests, a five-validator GLSim test, and an opt-in StudioNet smoke test. It has no frontend, backend, database, token, payout, proxy upgrade, or repository secret.

## Trust model

Untrusted evidence is delimited as data, model outputs use closed schemas, and validator replay must agree before semantic state is stored.

The deployer owns the campaign. Each designer address may submit one candidate; any address can vote once per segment; only the owner closes segment tallies.

## Implemented controls

- Concrete immutable GenVM runner hash; no floating runner dependency.
- Address normalization, explicit role separation, collection caps, one-time actions, and lifecycle locks.
- Bounded text plus strict `[EXPECTED]` and `[LLM_ERROR]` failure classes.
- Sorted, delimited evidence packets and independent validator replay.
- Storage is copied before nondeterministic callbacks; static audit requires zero callback reads from `self`.
- No cross-contract calls, fund custody, transfer, automated purchase, external deletion, or webhook.
- `.env`, caches, artifacts, wallet files, and local secrets are ignored. Live wallets are encrypted outside the workspace.

## Contract-specific safety properties

- At least two anchors and two audience segments freeze before designs open.
- Each designer address can submit one candidate and revise it at most once.
- Only CLEAR candidates can receive segment votes.
- AI cannot choose the campaign winner; each segment winner comes from at least two non-tied votes.

## Residual risks

- The contract screens declared layout text and does not inspect actual image pixels.
- Audience addresses are not demographic identities and votes do not predict click-through rate.
- Tied segment tallies must be resolved by additional product process outside this completed tally attempt.

Do not use this contract to make legal, medical, financial, employment, admission, credit, or physical-safety decisions beyond the explicit low-risk policy in its source. A new use case requires a fresh deployment and independent domain review.

## Reporting

Report vulnerabilities privately to the repository owner with the contract name, affected method, reproduction, expected invariant, and impact. Never include private keys, wallet passwords, or personal data.
