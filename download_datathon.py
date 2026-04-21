from __future__ import annotations

import os
import shutil
from pathlib import Path

import kagglehub


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip()


def main() -> None:
    load_env_file(Path(__file__).with_name(".env"))

    slug = "datathon-2026-round-1"
    source = Path(kagglehub.competition_download(slug))
    print(f"DOWNLOAD_PATH={source}")

    workspace_data = Path(__file__).with_name("data") / slug
    workspace_data.mkdir(parents=True, exist_ok=True)

    for item in source.rglob("*"):
        relative = item.relative_to(source)
        target = workspace_data / relative
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)

    print(f"WORKSPACE_DATA={workspace_data}")
    print("FILES=")
    for file_path in sorted(workspace_data.rglob("*")):
        if file_path.is_file():
            print(file_path.relative_to(workspace_data))


if __name__ == "__main__":
    main()
