# Git History Cleanup Guide

This guide provides step-by-step instructions for cleaning sensitive information from the Git history before making the repository public.

## ⚠️ Important Warnings

**READ THIS CAREFULLY BEFORE PROCEEDING:**

- 🔴 **This process REWRITES Git history** - it will change all commit SHAs
- 🔴 **A FORCE PUSH is required** - this will overwrite the remote repository
- 🔴 **All collaborators MUST re-clone** the repository after this process
- 🔴 **Open pull requests will be invalidated** and may need to be recreated
- 🔴 **Local branches of collaborators will be out of sync** with the remote
- ✅ **A backup branch will be created** before any changes are made
- ✅ **The script is idempotent** - safe to run multiple times if needed

## Background

This repository contains sensitive information in its Git history that must be removed before making the repository public:

### Sensitive Data to Remove:

1. **Exposed SECRET_KEY** in old `.env.example` commits:
   - The secret key `09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7` will be replaced with `your-secret-key-here`

2. **Database credentials** in old `.env.example` commits:
   - `DATABASE_PASSWORD=postgres` → `DATABASE_PASSWORD=your_password_here`
   - `DATABASE_USERNAME=postgres` → `DATABASE_USERNAME=your_username_here`
   - Note: Only the exact env var patterns will be replaced, not "postgres" in other contexts

3. **Personal email** in commit metadata:
   - `mouadelhourre50@gmail.com` → `111998759+OneM1@users.noreply.github.com`
   - Affects commits: `2b07d39`, `1df5deb`, `ee09042` and potentially others

## Prerequisites

### 1. Install git-filter-repo

`git-filter-repo` is the modern, recommended tool for rewriting Git history. It's much faster and safer than the deprecated `git filter-branch`.

**macOS (Homebrew):**
```bash
brew install git-filter-repo
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install git-filter-repo
```

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install git-filter-repo
```

**Using pip:**
```bash
pip3 install git-filter-repo
```

**Manual installation:**
```bash
curl -o git-filter-repo https://raw.githubusercontent.com/newren/git-filter-repo/main/git-filter-repo
chmod +x git-filter-repo
sudo mv git-filter-repo /usr/local/bin/
```

### 2. Verify installation
```bash
git-filter-repo --version
```

### 3. Prerequisites checklist
- [ ] `git-filter-repo` is installed
- [ ] You have a fresh clone of the repository (or are prepared to re-clone)
- [ ] All local changes are committed or stashed
- [ ] You have notified all collaborators about the upcoming history rewrite
- [ ] You have admin access to force push to the repository

## Step-by-Step Instructions

### Step 1: Clone the repository (if not already done)

```bash
git clone https://github.com/OneM1/Fastapi.git
cd Fastapi
```

### Step 2: Verify current state

Check the current `.env.example` file to confirm it already has safe placeholder values:

```bash
cat .env.example
```

You should see placeholders like `your-secret-key-here`, not actual credentials.

### Step 3: Run the cleanup script

```bash
./scripts/clean-history.sh
```

The script will:
1. Check that `git-filter-repo` is installed
2. Show you what will be changed
3. Ask for confirmation
4. Create a backup branch named `backup-before-history-clean`
5. Rewrite all commits to remove sensitive data
6. Replace commit author emails
7. Provide verification instructions

**Follow the on-screen prompts and carefully read all warnings.**

### Step 4: Verify the changes

After the script completes, verify that sensitive information has been removed:

#### Check commit emails:
```bash
git log --all --format="%H %ae %an %s" | head -20
```

You should see `111998759+OneM1@users.noreply.github.com` instead of the personal email.

#### Search for sensitive data:
```bash
# This should return no results
git log -p | grep "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

# Check if DATABASE_PASSWORD has been cleaned
git log -p | grep -C 2 "DATABASE_PASSWORD"

# Check if DATABASE_USERNAME has been cleaned  
git log -p | grep -C 2 "DATABASE_USERNAME"
```

#### Check specific historical files:
```bash
# View .env.example from various points in history
git log --all --oneline -- .env.example

# Pick a commit SHA from the output and view it
git show <commit-sha>:.env.example
```

All instances should now show placeholder values.

### Step 5: Force push to GitHub

**⚠️ WARNING: This step overwrites the remote repository history!**

Before proceeding:
1. Ensure you've verified the changes are correct
2. Notify all collaborators to backup their work
3. Consider the timing (avoid force pushing during active development)

```bash
# Push all branches
git push --force-with-lease origin --all

# Push all tags
git push --force-with-lease origin --tags
```

**Using `--force-with-lease` instead of `--force`:**
- `--force-with-lease` is safer - it will fail if someone else has pushed changes
- If it fails, you may need to pull first (but this defeats the purpose of history cleaning)
- In that case, coordinate with collaborators or use `--force` (more dangerous)

### Step 6: Notify collaborators

Send this message to all collaborators:

```
🚨 Git History Rewrite Completed

The repository history has been rewritten to remove sensitive information.

ACTION REQUIRED:
1. Backup any uncommitted local changes
2. Delete your local clone
3. Re-clone the repository from GitHub
4. Recreate any local branches if needed

DO NOT:
- Do not try to pull or merge
- Do not try to push from old clones
- Do not use old commit SHAs

If you have open PRs, you may need to recreate them from the new commits.
```

### Step 7: Clean up

After confirming everything works correctly, delete the cleanup files:

```bash
git rm scripts/clean-history.sh
git rm docs/CLEAN_HISTORY_GUIDE.md
git commit -m "Remove history cleanup tools after successful cleanup"
git push
```

### Step 8: Update documentation

If your README or other docs reference old commit SHAs, update them to use the new SHAs.

## Verification Checklist

Use this checklist to ensure the cleanup was successful:

- [ ] `git-filter-repo` completed without errors
- [ ] Commit history shows updated email `111998759+OneM1@users.noreply.github.com`
- [ ] Search for old SECRET_KEY returns no results in history
- [ ] Search for `DATABASE_PASSWORD=postgres` returns no results in history
- [ ] Search for `DATABASE_USERNAME=postgres` returns no results in history
- [ ] Current `.env.example` still has correct placeholder values
- [ ] Application still works with proper `.env` configuration
- [ ] Force push to GitHub completed successfully
- [ ] All collaborators have been notified
- [ ] Repository is accessible and viewable on GitHub

## Troubleshooting

### "git-filter-repo not found"
- Ensure git-filter-repo is installed and in your PATH
- Try the installation methods in the Prerequisites section

### "Not in a Git repository"
- Run the script from the root of your repository
- Ensure you're in the correct directory: `cd /path/to/Fastapi`

### "Backup branch already exists"
- The script will ask if you want to overwrite it
- If unsure, choose "no" and manually check the branch
- You can delete it with: `git branch -D backup-before-history-clean`

### Force push fails with "stale info"
- This means someone pushed changes after you ran the cleanup
- Coordinate with your team to ensure no one is pushing
- As a last resort, use `git push --force` (be very careful!)

### "Refs are not updated"
- Make sure you're pushing all refs: `--all` and `--tags`
- Check that you have write access to all branches

### Application breaks after cleanup
- The cleanup should only change historical file contents and commit metadata
- If the app breaks, check the current working directory files
- Compare with the backup branch: `git diff backup-before-history-clean`

## Rolling Back

If something goes wrong and you need to restore the original history:

```bash
# Switch to the backup branch
git checkout backup-before-history-clean

# Create a new main branch from backup
git branch -D main
git checkout -b main

# Force push to restore
git push --force origin main

# Restore other branches as needed
```

## What the Script Does

The `clean-history.sh` script uses `git-filter-repo` to:

1. **Create a backup**: Saves the current state to `backup-before-history-clean` branch

2. **Replace text in all files across all commits**:
   - SECRET_KEY: `09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7` → `your-secret-key-here`
   - DATABASE_PASSWORD: `postgres` → `your_password_here` (exact pattern only)
   - DATABASE_USERNAME: `postgres` → `your_username_here` (exact pattern only)

3. **Update commit metadata**:
   - Replace email `mouadelhourre50@gmail.com` with `111998759+OneM1@users.noreply.github.com`
   - Preserve author name `OneM1`

4. **Process all refs**:
   - All branches
   - All tags
   - HEAD

## Additional Resources

- [git-filter-repo documentation](https://github.com/newren/git-filter-repo)
- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Git history rewriting best practices](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Review the git-filter-repo documentation
3. Ensure you have a backup before attempting fixes
4. Consider reaching out to the team for help

---

**Remember: Always backup before rewriting history, and coordinate with your team!**
