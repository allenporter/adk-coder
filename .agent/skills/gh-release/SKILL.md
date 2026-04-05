---
name: gh-release
<<<<<<< ours
description: Automates version bumping in pyproject.toml and creating GitHub releases. Use when releasing a new version of a project.
=======
description: Automates version bumping in pyproject.toml and creating GitHub releases. Use when releasing a new version of the project.
>>>>>>> theirs
---

# GitHub Release Skill

## Overview

<<<<<<< ours
This skill automates the process of creating a new release. It updates the `version` in `pyproject.toml`, commits the change, and then creates a GitHub release using the `gh` CLI tool.
=======
This skill automates the process of creating a new release for this Python project. It updates the `version` in `pyproject.toml`, commits the change, and then creates a GitHub release using the `gh` CLI tool.
>>>>>>> theirs

## Semantic Versioning (SemVer)

This project follows [Semantic Versioning](https://semver.org/) (SemVer) for releasing versions. SemVer uses a `MAJOR.MINOR.PATCH` format:

- **MAJOR** version when you make incompatible API changes.
- **MINOR** version when you add functionality in a backward compatible manner.
- **PATCH** version when you make backward compatible bug fixes.

Example: `1.0.0` -> `1.1.0` (new feature), `1.1.0` -> `1.1.1` (bug fix), `1.1.1` -> `2.0.0` (breaking change).

## Usage

To use this skill, execute the `create-release.sh` script from the root of your project with the desired new version number as an argument.

**Example:**

```bash
<<<<<<< ours
./.agent/skills/gh-release/scripts/create-release.sh 0.1.0
=======
.agent/skills/gh-release/scripts/create-release.sh 0.9.1
>>>>>>> theirs
```

This will perform the following actions:

<<<<<<< ours
1. Find the `pyproject.toml` file in the project root.
2. Update the `version` field in `pyproject.toml` to the specified version.
3. Stage the `pyproject.toml` file.
4. Commit the change with the message `chore(release): <version>`.
5. Create a GitHub release with auto-generated release notes using `gh release create`.
=======
1. Ensure the working directory is clean and in the `main` branch.
2. Update the `version` field in `pyproject.toml` to `0.9.1`.
3. Stage the `pyproject.toml` file.
4. Commit the change with the message `chore(release): 0.9.1`.
5. Push the changes to the `main` branch.
6. Create a GitHub release named `0.9.1` with auto-generated release notes using `gh release create "0.9.1" --generate-notes`.
>>>>>>> theirs

## Requirements

- `gh` CLI tool must be installed and authenticated.
- The script should be run from the root of the project repository.
<<<<<<< ours
- `python` must be available (used for safe TOML editing).
=======
- The script expects to find `pyproject.toml` in the root.
>>>>>>> theirs

## Resources

### scripts/

- `create-release.sh`: The main script that performs the release automation.
