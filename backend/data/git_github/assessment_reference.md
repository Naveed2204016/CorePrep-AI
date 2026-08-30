# Git and GitHub Assessment Reference

## Git Foundations
Git stores snapshots as content-addressed objects and distributes complete history. The working tree, index, and current commit are distinct states.
## Repository Lifecycle
Clone copies repository data and configures a remote; init creates a repository without history. Ignore rules affect untracked files, not files already committed.
## Staging & Commits
The index selects the exact next snapshot, so one working tree can produce focused commits. Amend replaces the current commit with a new object.
## Branching
A branch is a movable commit reference, and HEAD identifies the checked-out reference or commit. Creating branches does not duplicate file history.
## Merging
Fast-forward moves a reference when no divergence exists; three-way merge uses two tips and their merge base. Merge commits preserve integration topology.
## Rebasing
Rebase copies commits onto a new base and therefore changes commit IDs. Rewriting private work is useful; rewriting published shared history disrupts collaborators.
## Remotes
Fetch updates remote-tracking references without merging; pull combines fetch with integration. Push asks a remote to update references and may be rejected for non-fast-forward history.
## GitHub Pull Requests
Pull requests coordinate review and checks around proposed branch changes. Branch protection can require approvals, status checks, signed commits, or restricted updates.
## Conflict Resolution
Conflicts occur when Git cannot combine intent automatically. Resolution requires editing the result, staging it, and continuing or aborting the operation.
## Undo & Recovery
Revert adds an inverse commit safely to shared history; reset moves references and may alter index or files. Reflog records local reference movement and often enables recovery.
## Tags & Releases
Annotated tags are objects with metadata and optional signatures; lightweight tags are references. Releases attach human notes and artifacts but are not the Git tag itself.
## Stashing & Cherry-Picking
Stash records selected uncommitted state for later application. Cherry-pick copies a commit's change onto the current history and can conflict.
## Git Internals
Blobs store file content, trees store directory mappings, and commits point to trees and parents. Unreachable objects may remain temporarily before garbage collection.
## Team Workflows
Trunk-based development favors short-lived branches and frequent integration; feature and release flows add isolation at coordination cost. Workflow must match release and review needs.
## GitHub Actions & Security
Workflows react to events and run jobs with scoped tokens and secrets. Untrusted pull-request code must not receive privileged credentials.
