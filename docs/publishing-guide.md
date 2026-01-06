# PyPI Publishing Guide

This guide covers how to publish and update the whisper-srt package on PyPI.

## Prerequisites

### 1. PyPI Account
- Already registered at https://pypi.org/account/register/

### 2. API Token Generation
1. Log in to https://pypi.org
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Name: `whisper-srt` (or any descriptive name)
5. Scope: "Entire account" (for first publish) or "Project: whisper-srt" (after first publish)
6. Copy the token (starts with `pypi-`)

### 3. Token Storage (Optional but Recommended)

Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Set file permissions:
```bash
chmod 600 ~/.pypirc
```

## First-time Publishing

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install build tools
pip install build twine

# 3. Clean any old builds
rm -rf dist/ build/ *.egg-info

# 4. Build package
python -m build

# 5. Verify the build
ls dist/
# Should show:
# whisper_srt-0.2.0-py3-none-any.whl
# whisper_srt-0.2.0.tar.gz

# 6. Upload to PyPI
twine upload dist/*
# If ~/.pypirc is configured, it will use the token automatically
# Otherwise, enter:
#   Username: __token__
#   Password: pypi-YOUR_TOKEN_HERE
```

## Version Update Procedure

When releasing a new version:

```bash
# 1. Update version in pyproject.toml
# Change: version = "0.2.0" → "0.2.1"

# 2. Commit the version change
git add pyproject.toml
git commit -m "chore: bump version to 0.2.1"

# 3. Clean old builds
rm -rf dist/ build/ *.egg-info

# 4. Build new version
python -m build

# 5. Upload to PyPI
twine upload dist/*
```

## GitHub Actions (Automated Publishing)

The repository includes automated publishing via `.github/workflows/publish.yml`.

### Setup (One-time)

#### Option A: Trusted Publisher (Recommended)
1. Go to https://pypi.org/manage/project/whisper-srt/settings/publishing/
2. Add a new "trusted publisher":
   - Owner: `tomada1114`
   - Repository: `whisper-srt`
   - Workflow name: `publish.yml`
   - Environment: (leave empty)

#### Option B: API Token
1. Generate a project-scoped token on PyPI
2. Go to GitHub repo → Settings → Secrets → Actions
3. Add secret: `PYPI_TOKEN` with the token value

### Usage
1. Create a new release on GitHub
2. Tag format: `v0.2.1`
3. GitHub Actions automatically builds and publishes to PyPI

## Verification

After publishing, verify:

```bash
# Check package on PyPI
# Visit: https://pypi.org/project/whisper-srt/

# Install from PyPI
pip install whisper-srt

# Or with pipx
pipx install whisper-srt

# Verify installation
whisper-srt --version
```

## Troubleshooting

### "File already exists" Error
- You cannot overwrite an existing version on PyPI
- Solution: Increment the version number in `pyproject.toml`

### "Invalid or non-existent authentication"
- Check that your API token is correct
- Ensure `~/.pypirc` has correct format
- For manual upload, use `__token__` as username

### Build Errors
```bash
# Ensure build tools are up to date
pip install --upgrade build twine setuptools
```

## Quick Reference

| Action | Command |
|--------|---------|
| Build | `python -m build` |
| Upload | `twine upload dist/*` |
| Check package | `twine check dist/*` |
| Clean | `rm -rf dist/ build/ *.egg-info` |
