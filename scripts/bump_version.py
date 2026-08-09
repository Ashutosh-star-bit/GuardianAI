"""
GuardianAI Semantic Versioning Automation Script
Usage: python scripts/bump_version.py [patch|minor|major]
"""

import sys
import re
import os

def bump_semver(version_str: str, bump_type: str) -> str:
    parts = version_str.strip().lstrip('v').split('.')
    if len(parts) != 3:
        raise ValueError(f"Invalid SemVer string '{version_str}'")

    major, minor, patch = map(int, parts)
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    else:
        raise ValueError(f"Invalid bump type '{bump_type}'. Must be major, minor, or patch.")

    return f"v{major}.{minor}.{patch}"

def main():
    bump_type = sys.argv[1] if len(sys.argv) > 1 else 'patch'
    current_version = "v1.0.0"
    new_version = bump_semver(current_version, bump_type)
    print(f"Bumping GuardianAI version: {current_version} -> {new_version} ({bump_type.upper()})")

if __name__ == "__main__":
    main()
