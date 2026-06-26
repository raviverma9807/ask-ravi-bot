from pathlib import Path


def load_profile():
    profile_path = Path("knowledge-base/profile.md")

    if profile_path.exists():
        return profile_path.read_text(encoding="utf-8")

    return ""