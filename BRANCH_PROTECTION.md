# Branch Protection Guide

This document explains how branch protection is configured for this repository to ensure code quality and prevent accidental or malicious changes to the main branch.

## What is Branch Protection?

Branch protection rules help enforce certain workflows and quality standards before code can be merged into important branches like `main`. These rules prevent:
- Force pushes that could overwrite history
- Accidental deletion of important branches
- Merging code without proper review or testing

## Configuration Files

### 1. `.github/settings.yml`

This file contains the branch protection rules that can be automatically applied using the [Probot Settings app](https://github.com/probot/settings). The configuration includes:

- **Pull Request Reviews**: Requires at least 1 approving review before merging
- **Status Checks**: Requires the "build" workflow to pass before merging
- **Force Push Protection**: Prevents force pushes to the main branch
- **Deletion Protection**: Prevents the main branch from being deleted
- **Conversation Resolution**: Requires all PR conversations to be resolved before merging

### 2. `.github/workflows/branch-protection-check.yml`

This GitHub Actions workflow runs automatically on:
- Pushes to the main branch
- Pull requests targeting the main branch

The workflow performs:
- Code checkout
- Python environment setup
- Dependency installation
- Linting with flake8
- Basic test execution

### 3. `.github/CODEOWNERS`

Defines code owners who are automatically requested for review when pull requests are opened. This ensures that the right people review changes to specific parts of the codebase.

## How to Apply Branch Protection Rules

### Option 1: Using Probot Settings App (Recommended)

1. Install the [Probot Settings app](https://github.com/apps/settings) on your repository
2. The app will automatically read the `.github/settings.yml` file
3. Branch protection rules will be applied automatically

### Option 2: Manual Configuration via GitHub UI

1. Go to your repository on GitHub
2. Click on **Settings** → **Branches**
3. Under "Branch protection rules", click **Add rule**
4. Configure the following settings:

   **Branch name pattern**: `main`
   
   ✅ **Require a pull request before merging**
   - Require approvals: 1
   - Dismiss stale pull request approvals when new commits are pushed
   
   ✅ **Require status checks to pass before merging**
   - Require branches to be up to date before merging
   - Status checks: Select "build" (from GitHub Actions workflow)
   
   ✅ **Require conversation resolution before merging**
   
   ✅ **Do not allow bypassing the above settings** (Optional)
   
   ✅ **Restrict who can push to matching branches** (Optional)
   
   ✅ **Do not allow force pushes**
   
   ✅ **Do not allow deletions**

5. Click **Create** to save the rule

### Option 3: Using GitHub API or CLI

You can also use the GitHub API or GitHub CLI to configure branch protection programmatically. See the [GitHub API documentation](https://docs.github.com/en/rest/branches/branch-protection) for details.

Example using GitHub CLI:
```bash
gh api repos/OneM1/Fastapi/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["build"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions=null \
  --field allow_force_pushes=false \
  --field allow_deletions=false \
  --field required_conversation_resolution=true
```

## Benefits of Branch Protection

1. **Code Quality**: Ensures all code is reviewed before merging
2. **Testing**: Prevents broken code from reaching production
3. **History Preservation**: Protects against force pushes that could lose work
4. **Collaboration**: Enforces team review processes
5. **Security**: Prevents unauthorized changes to critical branches

## Working with Protected Branches

### Creating a Pull Request

1. Create a new branch from main:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Add my feature"
   ```

3. Push your branch:
   ```bash
   git push origin feature/my-feature
   ```

4. Open a pull request on GitHub

5. Wait for:
   - Status checks to pass
   - At least 1 review approval
   - All conversations to be resolved

6. Merge the pull request

### If Status Checks Fail

1. Review the error messages in the GitHub Actions workflow
2. Fix the issues in your branch
3. Push the fixes
4. Status checks will run again automatically

### If Review is Requested

1. Address reviewer feedback
2. Push additional commits or make requested changes
3. Request re-review if needed

## Troubleshooting

### "Required status check is missing"

Make sure the GitHub Actions workflow has run at least once. Push a commit to your pull request to trigger it.

### "Branch protection rules not applied"

If using Probot Settings app, ensure it's properly installed. Otherwise, apply rules manually via GitHub Settings.

### "Cannot push to protected branch"

This is expected behavior. Create a pull request instead of pushing directly to main.

## Additional Resources

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Probot Settings App](https://github.com/probot/settings)

## Summary

Branch protection is now configured for this repository through:
- Configuration files in `.github/`
- GitHub Actions workflow for automated checks
- CODEOWNERS file for automatic review requests

To fully activate these protections, apply the branch protection rules using one of the methods described above.
