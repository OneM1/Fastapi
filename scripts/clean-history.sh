#!/usr/bin/env bash

# Git History Cleanup Script
# This script removes sensitive information from Git history before making the repository public
# WARNING: This will rewrite Git history and requires a force push

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print header
echo ""
echo "=========================================="
echo "  Git History Cleanup Script"
echo "=========================================="
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    print_error "Not in a Git repository. Please run this script from the repository root."
    exit 1
fi

# Check if git-filter-repo is installed
print_info "Checking for git-filter-repo..."
if ! command -v git-filter-repo &> /dev/null; then
    print_error "git-filter-repo is not installed."
    echo ""
    echo "Please install git-filter-repo using one of the following methods:"
    echo ""
    echo "  macOS (Homebrew):"
    echo "    brew install git-filter-repo"
    echo ""
    echo "  Ubuntu/Debian:"
    echo "    sudo apt-get install git-filter-repo"
    echo ""
    echo "  Fedora/RHEL:"
    echo "    sudo dnf install git-filter-repo"
    echo ""
    echo "  pip:"
    echo "    pip3 install git-filter-repo"
    echo ""
    echo "  Manual installation:"
    echo "    curl -o git-filter-repo https://raw.githubusercontent.com/newren/git-filter-repo/main/git-filter-repo"
    echo "    chmod +x git-filter-repo"
    echo "    sudo mv git-filter-repo /usr/local/bin/"
    echo ""
    exit 1
fi

print_success "git-filter-repo is installed"

# Warn user about the implications
echo ""
print_warning "This script will:"
echo "  1. Create a backup branch 'backup-before-history-clean'"
echo "  2. Rewrite ALL commits in the repository history"
echo "  3. Replace sensitive values in file contents"
echo "  4. Replace commit author/committer email addresses"
echo ""
print_warning "After running this script, you will need to force push to GitHub."
print_warning "All collaborators will need to re-clone the repository."
echo ""

# Ask for confirmation
read -p "Do you want to continue? (yes/no): " -r
echo
if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
    print_info "Operation cancelled."
    exit 0
fi

# Get current branch name
CURRENT_BRANCH=$(git branch --show-current)
print_info "Current branch: $CURRENT_BRANCH"

# Create backup branch
print_info "Creating backup branch 'backup-before-history-clean'..."
if git rev-parse --verify backup-before-history-clean &> /dev/null; then
    print_warning "Backup branch 'backup-before-history-clean' already exists."
    read -p "Do you want to overwrite it? (yes/no): " -r
    echo
    if [[ $REPLY =~ ^[Yy]es$ ]]; then
        git branch -D backup-before-history-clean
        git branch backup-before-history-clean
        print_success "Backup branch updated"
    else
        print_info "Using existing backup branch"
    fi
else
    git branch backup-before-history-clean
    print_success "Backup branch created"
fi

# Create temporary directory for replacements
TEMP_DIR=$(mktemp -d)
print_info "Created temporary directory: $TEMP_DIR"

# Create expressions file for text replacements
EXPRESSIONS_FILE="$TEMP_DIR/expressions.txt"

cat > "$EXPRESSIONS_FILE" << 'EOF'
# Replace the exposed SECRET_KEY
09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7==>your-secret-key-here

# Replace DATABASE_PASSWORD (exact pattern)
regex:DATABASE_PASSWORD=postgres(?!\w)==>DATABASE_PASSWORD=your_password_here

# Replace DATABASE_USERNAME (exact pattern - only when it's the env var assignment)
regex:DATABASE_USERNAME=postgres(?!\w)==>DATABASE_USERNAME=your_username_here
EOF

print_success "Created expressions file"

# Create mailmap file for email/name replacements
MAILMAP_FILE="$TEMP_DIR/mailmap.txt"

cat > "$MAILMAP_FILE" << 'EOF'
OneM1 <111998759+OneM1@users.noreply.github.com> OneM1 <mouadelhourre50@gmail.com>
OneM1 <111998759+OneM1@users.noreply.github.com> <mouadelhourre50@gmail.com>
EOF

print_success "Created mailmap file"

# Display what will be replaced
echo ""
print_info "The following replacements will be made:"
echo ""
echo "  File Content Replacements:"
echo "    - SECRET_KEY: '09d25e094faa...d3e7' → 'your-secret-key-here'"
echo "    - DATABASE_PASSWORD: 'postgres' → 'your_password_here' (env var pattern only)"
echo "    - DATABASE_USERNAME: 'postgres' → 'your_username_here' (env var pattern only)"
echo ""
echo "  Commit Metadata Replacements:"
echo "    - Email: 'mouadelhourre50@gmail.com' → '111998759+OneM1@users.noreply.github.com'"
echo "    - Author name will remain 'OneM1'"
echo ""

# Confirm before proceeding
read -p "Proceed with history rewrite? (yes/no): " -r
echo
if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
    print_info "Operation cancelled."
    rm -rf "$TEMP_DIR"
    exit 0
fi

print_info "Starting Git history rewrite..."
echo ""

# Run git-filter-repo with text replacements and mailmap
# Note: --force is needed if the repo has already been filtered or if there are remote tracking branches
git filter-repo \
    --force \
    --replace-text "$EXPRESSIONS_FILE" \
    --mailmap "$MAILMAP_FILE" \
    --refs HEAD \
    --refs refs/heads/* \
    --refs refs/tags/*

print_success "Git history has been rewritten successfully!"

# Clean up temporary files
rm -rf "$TEMP_DIR"
print_info "Cleaned up temporary files"

# Show summary
echo ""
echo "=========================================="
echo "  Summary"
echo "=========================================="
echo ""
print_success "History cleanup completed!"
echo ""
print_info "What was changed:"
echo "  ✓ All instances of the exposed SECRET_KEY were replaced"
echo "  ✓ All instances of DATABASE_PASSWORD=postgres were replaced"
echo "  ✓ All instances of DATABASE_USERNAME=postgres were replaced"
echo "  ✓ Commit author/committer email 'mouadelhourre50@gmail.com' was replaced"
echo ""

# Verification instructions
echo "=========================================="
echo "  Next Steps"
echo "=========================================="
echo ""
print_info "1. Verify the changes:"
echo "     git log --all --format='%H %ae %an %s' | head -20"
echo "     git log -p | grep -C 3 'SECRET_KEY\\|DATABASE_PASSWORD\\|DATABASE_USERNAME'"
echo ""
print_info "2. Check specific old commits if you know their SHAs:"
echo "     git show <commit-sha>:.env.example"
echo ""
print_warning "3. Force push to GitHub (THIS WILL OVERWRITE REMOTE HISTORY):"
echo "     git push --force-with-lease origin --all"
echo "     git push --force-with-lease origin --tags"
echo ""
print_warning "4. Notify all collaborators:"
echo "     - They must re-clone the repository (not pull)"
echo "     - Old commits/branches will be orphaned"
echo "     - They should backup any local work before re-cloning"
echo ""
print_info "5. After force pushing, delete these cleanup files:"
echo "     git rm scripts/clean-history.sh"
echo "     git rm docs/CLEAN_HISTORY_GUIDE.md"
echo "     git commit -m 'Remove history cleanup tools after successful cleanup'"
echo "     git push"
echo ""
print_success "Backup branch 'backup-before-history-clean' contains the original history"
echo ""
