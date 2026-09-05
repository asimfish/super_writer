#!/usr/bin/env python3
"""Install this checkout offline to an explicit, new super-writer directory.

No existing target is replaced, including an empty directory or dangling symlink.
The allowlist and checksum format are shared with build_release.py. No runtime
script is executed. The skill discovery marker is published only after its files.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import sys
import tempfile

if __package__:
    from . import build_release as distribution
else:
    import build_release as distribution


def _remove_created(created: list[tuple[Path, os.stat_result]]) -> None:
    # Remove only entries owned by this attempt; never recurse through a target.
    for path, identity in reversed(created):
        try:
            if os.path.samestat(identity, path.lstat()):
                if path.is_dir() and not path.is_symlink():
                    path.rmdir()
                else:
                    path.unlink()
        except OSError:
            pass


def install_skill(root: Path, destination: Path) -> Path:
    destination = destination.expanduser()
    if destination.name != distribution.SKILL_ID:
        raise distribution.DistributionError("Destination basename must be super-writer")
    # Resolve the parent only: resolving the leaf would hide a symlink target.
    destination = destination.parent.resolve() / destination.name
    if os.path.lexists(destination):
        raise distribution.DistributionError(f"Destination already exists: {destination}")
    _, payload = distribution.collect_payload(root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".super-writer-install-", dir=destination.parent) as temporary:
        staged = Path(temporary)
        for name, data in sorted(payload.items()):
            path = staged / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(data)
            path.chmod(distribution.file_mode(name))
            if hashlib.sha256(path.read_bytes()).digest() != hashlib.sha256(data).digest():
                raise distribution.DistributionError(f"Staged file verification failed: {name}")

        created: list[tuple[Path, os.stat_result]] = []
        try:
            # mkdir is exclusive even if another installer wins after the preflight.
            destination.mkdir()
            created.append((destination, destination.lstat()))
            names = sorted(name for name in payload if name != "SKILL.md") + ["SKILL.md"]
            directories = {destination}
            for name in names:
                target = destination / name
                parent = destination
                for component in Path(name).parts[:-1]:
                    parent = parent / component
                    if parent not in directories:
                        parent.mkdir()
                        created.append((parent, parent.lstat()))
                        directories.add(parent)
                # Same-filesystem hard links publish complete files without overwriting.
                os.link(staged / name, target)
                created.append((target, target.lstat()))
        except BaseException:
            _remove_created(created)
            raise
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, required=True,
                        help="Explicit new skill directory; basename must be super-writer")
    args = parser.parse_args(argv)
    if sys.version_info < (3, 10):
        parser.error("Python 3.10 or newer is required")
    try:
        destination = install_skill(Path(__file__).resolve().parents[1], args.destination)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"Installation failed: {exc}\n")
    print(f"Installed {distribution.SKILL_ID}: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
