#!/usr/bin/env python3
"""Build an offline, reproducible super_writer skill release (Python >= 3.10).

MANIFEST.sha256 uses sha256sum's text format, with paths relative to super-writer/.
It covers every payload file except itself; the adjacent ZIP checksum covers it.
Only the explicitly listed source roots below are distribution inputs.
"""

from __future__ import annotations

import argparse
from contextlib import ExitStack
import hashlib
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import zipfile


SKILL_ID = "super-writer"
REPO_NAME = "super_writer"
MANIFEST = "MANIFEST.sha256"
REQUIRED_FILES = (
    "SKILL.md", "PATTERNS.md", "LICENSE", "VERSION", "UPSTREAM.md", "skill-card.md",
)
REQUIRED_DIRS = ("agents", "scripts", "references", "evals")
OPTIONAL_FILES = ("README.md", "README.en.md", "CONTRIBUTING.md", "SECURITY.md", "CITATION.cff")
OPTIONAL_DIRS = ("docs", "examples")
EXCLUDED_NAMES = frozenset({
    "__pycache__", "venv", "env", "virtualenv", "site-packages", "node_modules",
    "paper_rewriting_output", "dist", "build", "private", "secrets",
})
EXCLUDED_SUFFIXES = frozenset({".pyc", ".pyo", ".pem", ".key"})
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


class DistributionError(ValueError):
    """A source or destination violates the distribution contract."""


def _check_name(name: str) -> None:
    if (name in {".", ".."} or name.endswith((" ", "."))
            or any(ord(char) < 32 or ord(char) == 127 or char in '\\:<>"|?*' for char in name)):
        raise DistributionError(f"Non-portable source name: {name!r}")


def _check_entry(path: Path) -> os.stat_result:
    info = path.lstat()
    if (stat.S_ISLNK(info.st_mode)
            or getattr(info, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)):
        raise DistributionError(f"Symlink or reparse point is not allowed: {path}")
    if not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)):
        raise DistributionError(f"Not a regular file or directory: {path}")
    if stat.S_ISREG(info.st_mode) and info.st_nlink != 1:
        raise DistributionError(f"Hard-linked source file is not allowed: {path}")
    return info


def _checked_path(root: Path, relative: Path) -> os.stat_result:
    if relative.is_absolute() or not relative.parts:
        raise DistributionError(f"Invalid source path: {relative}")
    path = root
    for name in relative.parts:
        _check_name(name)
        path = path / name
        info = _check_entry(path)
    if not path.resolve(strict=True).is_relative_to(root):
        raise DistributionError(f"Source escapes repository: {path}")
    return info


def _read_source(root: Path, relative: Path) -> bytes:
    before = _checked_path(root, relative)
    if not stat.S_ISREG(before.st_mode):
        raise DistributionError(f"Expected a regular source file: {relative}")
    with ExitStack() as stack:
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NONBLOCK", 0)
        # Anchor every component on POSIX, so a directory swap cannot follow a link.
        if (os.open in os.supports_dir_fd and hasattr(os, "O_NOFOLLOW")
                and hasattr(os, "O_DIRECTORY")):
            directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            parent_fd = os.open(root, directory_flags)
            stack.callback(os.close, parent_fd)
            for name in relative.parts[:-1]:
                parent_fd = os.open(name, directory_flags, dir_fd=parent_fd)
                stack.callback(os.close, parent_fd)
            fd = os.open(relative.name, flags | os.O_NOFOLLOW, dir_fd=parent_fd)
        else:
            fd = os.open(root / relative, flags | getattr(os, "O_NOFOLLOW", 0))
        stream = stack.enter_context(os.fdopen(fd, "rb"))
        opened = os.fstat(stream.fileno())
        if (not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1
                or not os.path.samestat(before, opened)):
            raise DistributionError(f"Source changed while opening: {relative}")
        data = stream.read()
        after = os.fstat(stream.fileno())
    current = _checked_path(root, relative)
    # Windows may give lstat/fstat different ctime semantics; compare each API
    # against itself across the read, while matching file identity across APIs.
    if (not os.path.samestat(opened, current)
            or (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns)
            != (after.st_size, after.st_mtime_ns, after.st_ctime_ns)
            or (before.st_size, before.st_mtime_ns, before.st_ctime_ns)
            != (current.st_size, current.st_mtime_ns, current.st_ctime_ns)
            or (after.st_size, after.st_mtime_ns)
            != (current.st_size, current.st_mtime_ns)):
        raise DistributionError(f"Source changed while reading: {relative}")
    return data


def _excluded(path: Path) -> bool:
    name = path.name.casefold()
    return (name.startswith(".") or name in EXCLUDED_NAMES
            or path.suffix.casefold() in EXCLUDED_SUFFIXES)


def collect_payload(root: Path) -> tuple[str, dict[str, bytes]]:
    """Validate and snapshot the allowlist before creating any output."""
    root = root.resolve(strict=True)
    payload: dict[str, bytes] = {}
    portable_names: set[str] = set()

    def visit(relative: Path) -> None:
        path = root / relative
        info = _checked_path(root, relative)
        if _excluded(relative):
            return
        name = relative.as_posix()
        if name.casefold() in portable_names:
            raise DistributionError(f"Case-colliding source paths: {name}")
        portable_names.add(name.casefold())
        if stat.S_ISDIR(info.st_mode):
            if os.path.lexists(path / "pyvenv.cfg"):
                return
            for child in sorted(path.iterdir(), key=lambda entry: entry.name):
                visit(relative / child.name)
        else:
            payload[name] = _read_source(root, relative)

    for names, required, directory in (
        (REQUIRED_FILES, True, False), (REQUIRED_DIRS, True, True),
        (OPTIONAL_FILES, False, False), (OPTIONAL_DIRS, False, True),
    ):
        for name in names:
            path = root / name
            if not os.path.lexists(path):
                if required:
                    raise DistributionError(f"Required source is missing: {name}")
                continue
            info = _checked_path(root, Path(name))
            if stat.S_ISDIR(info.st_mode) != directory:
                raise DistributionError(f"Wrong source type: {name}")
            visit(Path(name))

    for name in ("agents/openai.yaml", "scripts/smoke_test.py", "evals/activation.json"):
        if name not in payload:
            raise DistributionError(f"Required source is missing: {name}")
    if (any(name in payload for name in ("README.md", "README.en.md"))
            and "CONTRIBUTING.md" not in payload):
        raise DistributionError("CONTRIBUTING.md is required when distributing a README")
    version = payload["VERSION"].decode("utf-8").strip()
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", version):
        raise DistributionError("VERSION must contain a plain MAJOR.MINOR.PATCH version")
    payload[MANIFEST] = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n"
        for name, data in sorted(payload.items())
    ).encode("utf-8")
    return version, payload


def file_mode(name: str) -> int:
    path = Path(name)
    return 0o755 if path.parts[0] == "scripts" and path.suffix in {".py", ".sh"} else 0o644


def build_release(root: Path, output_dir: Path) -> tuple[Path, Path]:
    version, payload = collect_payload(root)
    output_dir = output_dir.expanduser().resolve()
    for name in REQUIRED_DIRS + OPTIONAL_DIRS:
        if output_dir.is_relative_to(root.resolve() / name):
            raise DistributionError("Output directory must not be inside a distributed source directory")
    archive = output_dir / f"{REPO_NAME}-v{version}-skill.zip"
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    for path in (archive, checksum):
        if os.path.lexists(path) and not stat.S_ISREG(_check_entry(path).st_mode):
            raise DistributionError(f"Release output is not a regular file: {path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".super-writer-build-", dir=output_dir) as temporary:
        staged = Path(temporary) / archive.name
        # Stored entries avoid zlib-version-dependent output as well as source metadata.
        with zipfile.ZipFile(staged, "w", compression=zipfile.ZIP_STORED) as bundle:
            for name, data in sorted(payload.items()):
                entry = zipfile.ZipInfo(f"{SKILL_ID}/{name}", date_time=ZIP_TIMESTAMP)
                entry.create_system = 3
                entry.external_attr = (stat.S_IFREG | file_mode(name)) << 16
                bundle.writestr(entry, data)
        digest = hashlib.sha256(staged.read_bytes()).hexdigest()
        staged_checksum = Path(temporary) / checksum.name
        staged_checksum.write_bytes(f"{digest}  {archive.name}\n".encode("ascii"))
        os.replace(staged, archive)
        os.replace(staged_checksum, checksum)
    return archive, checksum


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("dist"),
                        help="Release directory, relative to the working directory (default: dist)")
    args = parser.parse_args(argv)
    if sys.version_info < (3, 10):
        parser.error("Python 3.10 or newer is required")
    try:
        archive, checksum = build_release(Path(__file__).resolve().parents[1], args.output_dir)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"Build failed: {exc}\n")
    print(archive)
    print(checksum)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
