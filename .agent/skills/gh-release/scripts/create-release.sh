#!/bin/bash
set -e

VERSION=$1
if [ -z "$VERSION" ]; then
  echo "Usage: $0 <version>"
  exit 1
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "main" ]]; then
  echo "Error: You must be on the main branch to create a release."
  exit 1
fi

if [[ -n $(git status -s) ]]; then
  echo "Error: Working directory is not clean. Please commit or stash your changes."
  exit 1
fi

if ! command -v gh &> /dev/null; then
    echo "gh command could not be found, please install it first"
    exit 1
fi

PYPROJECT="pyproject.toml"

if [ ! -f "$PYPROJECT" ]; then
    echo "Error: No pyproject.toml found in the current directory."
    exit 1
fi

# Using python to update the toml file safely
python -c "
import re
from pathlib import Path

content = Path('$PYPROJECT').read_text()
content = re.sub(
    r'^version\s*=\s*\"[^\"]*\"',
    'version = \"$VERSION\"',
    content,
    count=1,
    flags=re.MULTILINE,
)
Path('$PYPROJECT').write_text(content)
print(f'Updated $PYPROJECT to version $VERSION')
"

git add "$PYPROJECT"
git commit -m "chore(release): $VERSION"
git push
gh release create "$VERSION" --generate-notes
