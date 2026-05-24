# Repository Cleanup Guide

This guide explains how to clean up the repository after the .gitignore has been added.

## ⚠️ Important: Understanding What Will Happen

The `.gitignore` file prevents new files from being tracked, but **doesn't remove already-committed files**. To remove large files committed before, you need to follow these steps.

## Step 1: Remove Virtual Environment from Git History

The virtual environment (venv/) is taking up massive space. Here's how to remove it:

```bash
# First, ensure everyone has committed their work
git status

# Remove the venv folder from Git tracking (doesn't delete local files)
git rm -r --cached venv/

# Add and commit this change
git add .
git commit -m "Remove virtual environment from version control"

# Push to remote
git push origin main
```

## Step 2: Verify .gitignore is Working

After adding .gitignore, verify it's working:

```bash
# Check what files are currently tracked
git ls-files

# Make sure venv/ and other files are not listed
git ls-files | grep -E "venv/|\.exe|\.pyd"
```

## Step 3: Clean Up Large/Unnecessary Files

### Option A: Lightweight Cleanup (Keep History)

This approach removes files from tracking but keeps commit history.

```bash
# Remove compiled Python files
git rm -r --cached __pycache__/
git rm -r --cached *.pyc

# Remove log files
git rm -r --cached logs/

# Remove data files
git rm -r --cached data/raw/
git rm -r --cached audio_cache/

# Remove web events CSVs
git rm -r --cached web_events_*.csv

# Commit all removals
git add .
git commit -m "Remove cached and generated files from tracking

- Removed __pycache__ directories
- Removed .pyc compiled files
- Removed application logs
- Removed data files and caches
- These are now covered by .gitignore

Repository size should decrease significantly."

git push origin main
```

### Option B: Full Cleanup (Rewrite History) - FOR ADVANCED USERS ONLY

⚠️ **WARNING**: This rewrites git history. Only do this if:
- No one else is working on this repo
- You haven't pushed to GitHub yet OR you have direct access to reset

```bash
# Use git-filter-branch to remove all large files
git filter-branch --tree-filter 'rm -rf venv' HEAD

# Or use BFG Repo-Cleaner (faster, safer)
# Download from https://rtyley.github.io/bfg-repo-cleaner/
bfg --delete-folders venv
bfg --delete-files '*.exe'
bfg --delete-files '*.pyd'

# Clean up reflog
git reflog expire --all --expire=now
git gc --prune=now --aggressive

# Force push (dangerous! only if you own the repo)
git push origin --force main
```

## Step 4: Verify Repository Size

Check if the cleanup worked:

```bash
# Size of entire repo
du -sh .git

# Before cleanup: Probably 500MB+
# After cleanup: Should be 1-5MB

# List largest files still in repo
git ls-files -z | xargs -0 ls -lhS | head -20
```

## Step 5: Instruct Collaborators

If you have collaborators, they need to update their local repos:

```bash
# They should do this:
git fetch origin
git reset --hard origin/main
rm -rf venv/  # Delete local venv

# Then recreate venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

## What to Do Next

### Create Proper Directory Structure

```bash
# Create directories mentioned in SETUP.md
mkdir -p backend frontend data/{raw,cleaned,database} logs audio_cache tests docs

# Verify structure
tree -d -L 2
```

### Move Existing Code

If you have code files in the root, move them:

```bash
# Python files to backend/
mv app.py backend/
mv search.py backend/
mv intent.py backend/
mv *.py backend/  # All Python files

# React components to frontend/
mv *.tsx frontend/components/
mv *.ts frontend/hooks/

# Data files to data/
mv books_metadata.csv data/
cp *.csv data/  # CSV files to data

# Create .env file (not committed)
cat > .env << EOF
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///data/database/library.db
EOF
```

### Recreate Virtual Environment

```bash
# Remove old venv (if present)
rm -rf venv

# Create fresh venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Verification Checklist

- [ ] `.gitignore` file added
- [ ] Large files removed from tracking
- [ ] Repository size decreased significantly
- [ ] Can run: `python backend/app.py`
- [ ] Tests pass: `pytest tests/`
- [ ] All collaborators updated their local repos
- [ ] Documentation reflects new structure

## Troubleshooting

### Issue: Files still showing in git status

**Solution:**
```bash
# Clear git cache
git rm -r --cached .
git add .
git commit -m "Update git tracking to respect .gitignore"
```

### Issue: Accidentally committed sensitive data

**Solution:**
```bash
# Use git-filter-branch or BFG Repo-Cleaner
# See "Option B" above

# Or use git rm to remove specific file
git rm --cached path/to/sensitive/file
git commit -m "Remove sensitive file"
```

### Issue: Repository still huge after cleanup

**Solution:**
```bash
# Check what's taking space
git rev-list --all --objects | sort -k2 | tail -20

# Remove specific large objects
git filter-branch --tree-filter 'rm -rf path/to/large/folder' HEAD
```

## References

- [GitHub - Removing Files](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Pro Git - Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

---

**Next Steps**: After cleanup, follow the [SETUP.md](SETUP.md) guide to properly set up the project.
