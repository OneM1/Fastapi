# Git History Cleanup Script

This directory contains the script for cleaning sensitive information from the Git history.

## Quick Start

```bash
# From the repository root
./scripts/clean-history.sh
```

## What It Does

Removes sensitive information from Git history:
- Replaces exposed SECRET_KEY
- Replaces database credentials (PASSWORD and USERNAME)
- Updates commit author emails from personal to GitHub noreply

## Documentation

For complete instructions, see: [`docs/CLEAN_HISTORY_GUIDE.md`](../docs/CLEAN_HISTORY_GUIDE.md)

## Requirements

- `git-filter-repo` must be installed
- Run from repository root directory
- Requires force push permissions

## ⚠️ Warning

This script rewrites Git history. All collaborators must re-clone the repository after running it.
