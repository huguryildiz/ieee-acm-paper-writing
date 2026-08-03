# Post-64cec1a behavioral evidence

This bundle records three complete behavioral campaigns against the repository candidate built on
commit `64cec1afeb6d42a8bb1f2b0aec281f6f2bb91a32`. It is evidence for the post-commit candidate,
not a retroactive claim about the tagged `v0.6.1` files. The exact candidate identifiers are:

- installable-skill hash: `ea1badec6ce9cbfe590b73bf81265ddaad3c24e117ab3a17af44e936f906333d`;
- `evals/cases.json` hash: `2d824f6d18d003a5e2d8df3d8e08adf825f005a581782fb5af68488a068b007a`;
- denominator: 27 cases, 92 `must_pass` criteria, and 55 `must_not` criteria per campaign.

The collector explicitly named `skills/ieee-acm-paper-writing/SKILL.md` as its sole authority and
rejected same-named user-level, global, cached, or otherwise installed copies. This corrects an
authority ambiguity found during the campaign: name-only invocation could silently exercise a
different installed version.

## Results

| Campaign | Client and requested model | Result | Failed cases |
| --- | --- | --- | --- |
| Codex replication 1 | Codex CLI 0.144.6; `gpt-5.6-sol`; medium | 25/27 | `citation_metadata_vs_support`, `landmark_corpus_not_ranking` |
| Codex replication 2 | Codex CLI 0.144.6; `gpt-5.6-sol`; medium | 27/27 strict pass | none |
| Claude replication 1 | Claude Code 2.1.220; `sonnet` alias; high | 25/27 | `industrial_style_profile`, `humanize_preserves_claims` |

The first Codex run correctly rejected the unsupported transformer comparison but did not
explicitly state that correct metadata is insufficient for claim support. More seriously, it
gave approximate citation counts without a named database and query date. The Claude run copied a
sentence frame too closely from a supplied style excerpt and dropped the fixed-batch comparator
while humanizing a numerical result. These are retained failures, not exclusions or rerun-selected
successes. They show that the instructions are not a reliability guarantee even though one full
campaign passed.

Every campaign includes the complete response set, criterion-level score file, scoring rationale,
and generated HTML-map JSON/HTML pair. The machine-readable [manifest](post-64cec1a/manifest.json)
links the files and declares every failure. `scripts/validate_behavioral_evidence.py` recomputes the
current skill, case, response, and artifact hashes; checks all criterion keys and verdicts; requires
two clients and two distinct Codex replications; and fails if a declared denominator or failure list
drifts.

## Scoring boundary

Scoring was schema-constrained, agent-assisted criterion review with Claude Code 2.1.220,
requested Opus/high and resolved primary model `claude-opus-5`. `expected_routing` was not scored.
Missing or ambiguous `must_pass` evidence was scored `false`; a `must_not` verdict is `true` only
when the prohibited behavior appears. There was **no independent human review**. Accordingly, this
bundle is stronger than an unretained single existence run but is not a reliability estimate,
statistical benchmark, or proof of behavior across models and executions.

## Installation check

On 2026-08-03, the documented command using `skills` 1.5.21 and tag `v0.6.1` completed in a fresh
temporary Git project, installed exactly one skill under
`.agents/skills/ieee-acm-paper-writing`, and the installed standard-library audit-map renderer
validated its shipped JSON fixture. That clean installation checks the tagged release channel; it
does not substitute for the post-64cec1a candidate campaigns above.
