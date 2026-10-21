# Exercise the changed Windows stubs in PR CI

## Goal

Wire the existing dev-group/Pyright authority for libloader PR #15. Smallest
change: one roughly 40-line workflow and this single task note; no product,
dependency, support, test or existing release-workflow changes.

## State

Exact origin git@github.com:accessibleapps/libloader.git. Fresh master/base
a753993f635fe355a0e98e8e4f51a357e7667a89; original open PR #15 head
f1da9d1237881fa87c00ac4f1f90f6e52b4141bf on
dependabot/pip/types-pywin32-lt-313.0.0. The PR only widens the dev-only stub
bound from <310 to <313. Actual Claude approved that original source diff but
identified missing type-check execution. The push-only distribution build is
green; it does not install dev dependencies or run Pyright.

New isolated branch repair/task6-libloader-pr15-ci is feature-derived at
task-6/worktrees/libloader-ci. Separate local-review and remote feature backups
backup/task6-libloader-pr15-local-before-ci and
backup/task6-libloader-pr15-remote-before-ci both retain the original f1da9d1
head. Canonical master, detached review checkout, ignored environment/lock and
untracked test_architecture_fix.py/tmpclaude-085a-cwd remain untouched.

## Decisions and why

Read global instructions, all tracked source/config/workflow/readme files,
repository-ci skill and current primary PyPI metadata. No repository AGENTS,
CLAUDE, .agents or existing task note. No tracked lock or tracked tests.

Python 3.9 resolves changed stubs 311.0.0.20251008 (Requires-Python >=3.9), while
3.10+ resolves 312.0.0.20261006 (>=3.10). Python 3.8 retains unchanged
308.0.0.20241221. Therefore use only 3.9 and 3.10 on Windows to exercise the two
changed dependency branches, not a support-version/platform matrix. Keep
requires-python >=3.8 and configured Pyright pythonVersion=3.8 unchanged.

Install the existing dev group, print the actual installed stub version, run
configured Pyright with the selected venv interpreter. Static checking calls
no COM service and loads no user DLL. CI resolves dependencies because there is
no authoritative tracked lock; no lock is added. Existing push build/tag release
workflow remains byte-identical. New workflow uses verified full action pins,
uv 0.13.4, contents:read, no stored checkout credentials/cache, 10-minute timeout
and workflow/ref cancellation. No extra lint/tests/scripts are introduced.

## Surprises

Canonical uv.lock is ignored user work, not tracked command authority. The
original workflow's green package build does not test the changed stub bound.
The new workflow is not yet published or claimed green; no local CI is run.
Actionlint v1.7.12 passed and zizmor v1.31.1 offline reported no findings for
the authored YAML. CRLF-aware diff check and unchanged source/manifest/release
workflow checks passed. No project lock or runtime output was generated.

## Next step

Return the committed workflow/note diff and exact local head for coordinator
review before publication. Obtain actual final-head Claude review
and relevant hosted success before merge. Preserve original feature tips and
do not edit PR descriptions, release workflow or source.
