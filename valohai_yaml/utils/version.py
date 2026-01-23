import subprocess

from valohai_yaml import __version__


def get_current_version() -> str:
    """
    Get the current version (based on latest release).

    If there have been commits after the tagged release version,
    a '+' is added to the version.
    """
    version = __version__
    suffix = "+" if _has_changed_after_release(version) else ""
    return f"{version}{suffix}"


def _has_changed_after_release(version: str) -> bool:
    """Check for commits after the given version tag."""
    tag = f"v{version}"
    try:
        result = subprocess.run(
            ["git", "rev-list", f"{tag}..HEAD", "--count"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        if result.returncode == 0:
            commit_count = int(result.stdout.strip())
            return commit_count > 0
    except (subprocess.TimeoutExpired, ValueError, FileNotFoundError):
        # could not determine, assume no changes
        pass
    return False
