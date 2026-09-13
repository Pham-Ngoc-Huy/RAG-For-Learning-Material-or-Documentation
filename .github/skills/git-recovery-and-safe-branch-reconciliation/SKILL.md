# Git Recovery & Diverged-Branch Recovery Skill

## Purpose

Safely recover local work after accidental Git operations such as an interrupted rebase, failed push, divergent branches, merge conflicts, or a commit that appears to have been “lost”.

The core principle is:

> **Protect references first, inspect history second, modify files last, and never use destructive Git commands until the desired state is proven.**

This skill is designed for repositories where both local and remote work may contain valuable changes.

---

## 1. First rule: freeze the situation

When files appear lost or Git reports a rebase/merge problem:

### Do NOT immediately run

```bash
git reset --hard
git clean -fd
git checkout .
git pull
git rebase
 git push --force
git push --force-with-lease
git merge --abort
git rebase --abort
```

Some of these commands are safe in specific circumstances, but they should not be used blindly during recovery.

First inspect:

```bash
git status
git branch -avv
git log --oneline --decorate --graph --all -20
git reflog --all -20
```

---

## 2. If Git says a commit is “leaving 1 commit behind”

This is usually recoverable.

Example warning:

```text
Warning: you are leaving 1 commit behind, not connected to any of your branches:

  8c44c2e update#api/: api for login and logout
```

Immediately protect the commit with a branch:

```bash
git branch rescue 8c44c2e
```

For extra safety, create a second backup reference:

```bash
git branch backup-rescue rescue
```

Verify:

```bash
git branch -avv
```

The desired result is something like:

```text
rescue         8c44c2e ...
backup-rescue  8c44c2e ...
```

Once a commit has a branch pointing to it, it is much harder to accidentally lose it.

---

## 3. If Git blocks checkout because of an unresolved index

Typical error:

```text
requirements.txt: needs merge
error: you need to resolve your current index first
```

Do not force a checkout.

Inspect:

```bash
git status
git ls-files -u
```

If you are in an unwanted or accidental rebase, and a known-good recovery reference already exists, the rebase can be aborted safely:

```bash
git rebase --abort
```

Then verify:

```bash
git status
git branch -avv
```

The goal is to return to a clean state before continuing recovery.

---

## 4. If `git stash` fails because a file needs merge

Typical result:

```text
requirements.txt: needs merge
```

Normal stash cannot always handle an unresolved merge state.

Do not keep retrying stash.

If the file itself may contain valuable work, make an external copy first:

```bash
cp requirements.txt /tmp/requirements.txt.conflicted-backup
```

Then inspect the conflict:

```bash
git diff -- requirements.txt
git diff --cc requirements.txt
git ls-files -u
```

---

## 5. Understand the branch topology before changing it

A common recovery situation looks like:

```text
                 rescue
                   |
                   X   <- recovered local commit
                  /
                 /
        local main
             |
             |
       common ancestor
             |
       origin/main
```

A repository may report:

```text
Your branch and 'origin/main' have diverged,
and have 1 and 2 different commits each, respectively.
```

This means local and remote histories contain different commits. It does **not** mean files are lost.

Inspect unique commits without producing a huge repository diff:

```bash
git log --oneline --left-right origin/main...main
```

Useful ancestry checks:

```bash
git merge-base --is-ancestor rescue origin/main; echo "rescue->origin: $?"
git merge-base --is-ancestor origin/main rescue; echo "origin->rescue: $?"
```

Avoid large `git diff` commands when the repository contains very large files. Prefer commit/history metadata first.

---

## 6. Compare trees cheaply

When you only need to know whether two commits contain identical file trees, use:

```bash
git rev-parse origin/main^{tree} rescue^{tree}
```

If the two tree hashes are identical, the repository contents are identical at those commits even if their commit histories differ.

This is usually much faster than:

```bash
git diff origin/main rescue
```

especially when large Markdown or generated files exist.

---

## 7. Inspect a recovered commit before cherry-picking it

A recovered commit may contain both the desired work and unrelated edits.

Inspect metadata:

```bash
git show --format=fuller --no-patch <commit>
```

Inspect its file-level changes:

```bash
git show --stat <commit>
git diff --name-status <commit>^ <commit>
git diff --stat <commit>^ <commit>
```

This distinction is important:

- **API changes** may be the intended recovery.
- **Documentation rewrites**, dependency rewrites, configuration changes, or large data-file modifications may be unrelated.

Do **not** automatically cherry-pick a large mixed commit if only part of it is wanted.

---

## 8. Selective file recovery

When a recovery commit contains useful files mixed with unwanted changes, restore only the desired paths.

Example:

```bash
git restore --source=rescue -- \
  src/api/routes/__init__.py \
  src/api/routes/auth.py \
  src/api/routes/chat.py \
  src/api/routes/documents.py \
  src/api/schemas/__init__.py \
  src/api/schemas/auth.py \
  src/api/schemas/chat.py \
  src/api/schemas/documents.py \
  src/api/services/auth.py
```

Important:

> Git tracks files, not directories.

Therefore this may fail:

```bash
git restore --source=rescue -- src/api/routes
```

with:

```text
pathspec 'src/api/routes' did not match any file(s) known to git
```

In that case, specify the tracked files explicitly.

---

## 9. Abort an accidental merge before separating recovery work

If you accidentally start:

```bash
git merge origin/main
```

and it produces conflicts, do not mix recovery-file restoration into that unresolved merge unless you intentionally know what you are doing.

If the merge is not the operation you want to resolve at that moment, abort it:

```bash
git merge --abort
```

Then verify:

```bash
git status
```

It is acceptable for recovered files to remain untracked after the abort. Do **not** delete them just because they are untracked.

---

## 10. Stage only recovered files

After selectively restoring the desired files, inspect:

```bash
git status
```

Then stage only the intended paths:

```bash
git add src/api/routes src/api/schemas src/api/services
```

Verify again:

```bash
git status
```

Before committing, make sure unrelated files such as these are not accidentally staged:

```text
README.md
READ.md
main.py
config/config.yml
requirements.txt
large documentation files
lockfiles
```

unless those changes are explicitly intended.

Commit the recovered work separately:

```bash
git commit -m "feat(api): restore authentication routes and schemas"
```

This gives the recovery a clean, identifiable history entry.

---

## 11. Protect the current main before reconciliation

Before rewriting or merging branch history, create a backup reference:

```bash
git branch backup-main-before-recovery main
```

For the recovered commit:

```bash
git branch backup-rescue rescue
```

A safe recovery state may therefore look like:

```text
backup-main-before-recovery -> old local main
backup-rescue              -> recovered commit
rescue                     -> recovered commit
main                       -> working recovery branch
origin/main                -> remote branch
```

---

## 12. Reconcile with remote only after local recovery is clean

Once the desired local changes are committed and the working tree is clean:

```bash
git fetch origin
```

Then inspect:

```bash
git log --oneline --left-right origin/main...main
```

If both sides contain legitimate work, integrate them with a normal merge:

```bash
git merge origin/main
```

If a conflict occurs, resolve it deliberately.

Do not use:

```bash
git checkout --ours .
git checkout --theirs .
```

unless you fully understand that you are discarding one side's contents.

---

## 13. Resolve dependency-file conflicts deliberately

Files such as `requirements.txt` are especially likely to conflict after a recovery.

When Git reports:

```text
CONFLICT (content): Merge conflict in requirements.txt
```

inspect the file and combine the required dependencies manually.

After resolving conflict markers:

```bash
git add requirements.txt
git commit
```

Use the merge commit Git provides unless a deliberate custom message is required.

---

## 14. Verify the final history before pushing

After the merge succeeds:

```bash
git status
git log --oneline --decorate --graph -8
```

Desired state:

```text
nothing to commit, working tree clean
```

Then confirm the local branch is ahead of remote rather than diverged:

```bash
git status
```

Typical final state:

```text
Your branch is ahead of 'origin/main' by N commits.
nothing to commit, working tree clean
```

Optionally inspect only local changes relative to the remote:

```bash
git diff --stat origin/main..main
```

Avoid full-repository diffs when files are very large.

---

## 15. Push normally — never force during this recovery pattern

When the branch is clean and ahead of remote:

```bash
git push origin main
```

Do **not** use:

```bash
git push --force
```

or:

```bash
git push --force-with-lease
```

unless rewriting the remote history is explicitly intended and independently verified.

After pushing:

```bash
git status
```

Expected result:

```text
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

---

## 16. Recovery checklist

Use this order:

```text
1. Freeze Git operations.
2. Inspect status / branches / graph / reflog.
3. Protect suspicious commits with rescue branches.
4. Exit accidental rebase/merge states cleanly.
5. Inspect recovered commit contents.
6. Decide which files are actually wanted.
7. Restore only those files.
8. Stage only recovered files.
9. Commit recovery separately.
10. Fetch remote.
11. Merge remote into local if both sides contain real work.
12. Resolve conflicts deliberately.
13. Verify clean status and history.
14. Push normally.
15. Verify remote is synchronized.
```

---

## 17. Anti-patterns

### Do not panic because a commit is “unreachable”

A commit shown by Git as no longer belonging to a branch is often recoverable through its SHA, reflog, or an existing backup reference.

### Do not assume “diverged” means “lost files”

Divergence is about commit ancestry, not necessarily file disappearance.

### Do not merge a mixed recovery commit blindly

One commit can contain both the desired feature and unrelated changes.

### Do not stage everything during recovery

Avoid:

```bash
git add .
```

until you have deliberately inspected the working tree.

Prefer specific paths.

### Do not force-push while the state is uncertain

A normal merge plus normal push is generally much safer when both local and remote histories contain valid work.

---

## 18. Minimal command recipe

For a similar incident, the compact recovery sequence is:

```bash
# Inspect
git status
git branch -avv
git log --oneline --decorate --graph --all -20

# Protect an important commit
git branch rescue <lost-commit-sha>
git branch backup-rescue rescue

# Escape accidental rebase if appropriate
git rebase --abort

# Protect current main
git branch backup-main-before-recovery main

# Recover only selected files
git restore --source=rescue -- <specific-files>

git status
git add <specific-files>
git commit -m "feat(...): restore ..."

# Reconcile histories
git fetch origin
git merge origin/main

# Resolve conflicts, then
git add <resolved-files>
git commit

# Verify
git status
git log --oneline --decorate --graph -8

# Publish normally
git push origin main
```

---

## Desired end state

The final repository should have:

```text
- local main contains the intended recovered work
- remote main contains the previous remote work
- both histories are reconciled
- no unresolved merge/rebase state
- working tree is clean
- backup references exist until recovery is fully verified
- push is performed without force
```

Once the remote is verified and the recovery is no longer needed, backup branches can be deleted intentionally:

```bash
git branch -d backup-main-before-recovery
git branch -d backup-rescue
```

Only delete recovery references after confirming the final state is correct.
