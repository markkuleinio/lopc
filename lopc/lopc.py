import argparse
import fnmatch
import sys
from pathlib import Path
from typing import List, Tuple


DEFAULT_EXCLUDED_DIRS = [
    ".*",
    "venv",
    "__pycache__",
]


class Config:
    excluded_dirs: List[str]
    verbosity: int


def is_excluded(name: str) -> bool:
    """ Returns True if the given name matches the exclude directory patterns,
    False otherwise.
    """
    for exclude in Config.excluded_dirs:
        if fnmatch.fnmatchcase(name, exclude):
            return True
    return False


def read_file(file: Path) -> int:
    """ Reads the given file, returns number of non-empty and non-comment lines.
    """
    if Config.verbosity >= 1:
        print(f"File: {file} ", end="", flush=True)
    lines = 0
    try:
        for line in file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                lines += 1
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError while reading {file}, ignoring it", file=sys.stderr)
        if Config.verbosity >= 1:
            # "Close" the pending verbose output line in stdout
            print("(ignored)", flush=True)
        return 0
    except OSError as e:
        print(f"Error reading {file}: {e}", file=sys.stderr)
        sys.exit(1)
    if Config.verbosity >= 1:
        print(f"({lines} lines)", flush=True)
    return lines


def recurse_dir(dir: Path) -> Tuple[int, int]:
    """ Reads the given directory, for files reads the lines of code,
    for directories recurses into them.

    Returns tuple: number of files handled, number of lines of code
    """
    if Config.verbosity >= 2:
        print("Directory:", dir)
    total_files = total_lines = 0
    dirs_list = []
    files_list = []
    # First populate the lists so that we can show files first
    for item in dir.iterdir():
        if item.is_dir():
            dirs_list.append(item)
        else:
            files_list.append(item)
    # First read the files (or "non-directories")
    for item in files_list:
        if item.suffix == ".py":
            total_files += 1
            total_lines += read_file(item)
    # Then recurse the directories
    for item in dirs_list:
        if not is_excluded(item.name):
            files, lines = recurse_dir(item)
            total_files += files
            total_lines += lines
    return (total_files, total_lines)


def scan(target_name: str) -> Tuple[int, int]:
    """ Scans the given target (directory or file) and prints the number
    of files and number of lines of code.

    Returns tuple: number of files handled, number of lines of code
    """
    target = Path(target_name)
    if target.is_dir():
        files, lines = recurse_dir(target)
    else:
        files = 1
        lines = read_file(target)
    print(f"{target_name} Files: {files} Lines: {lines}")
    return (files, lines)


def main():
    parser = argparse.ArgumentParser(description="Count lines of Python code")
    parser.add_argument(
        "target",
        nargs="+",
        help="File or directory to scan (can be given multiple times)",
        metavar="TARGET",
    )
    parser.add_argument(
        "-e", "--exclude-dir",
        action="append",
        help=(
            "Add directory (and its subdirectories) to the exclusion list. Can be given "
            "multiple times. Unix shell-style wildcards (?*) are allowed. "
            "Default = 'venv', '.*' and '__pycache__'"
        ),
    )
    parser.add_argument(
        "--no-defaults",
        action="store_true",
        help="Don't exclude any directories by default (use --exclude-dir as needed)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        help="More output (can be given multiple times, default = not verbose)",
        default=0,
    )
    args = parser.parse_args()
    Config.excluded_dirs = DEFAULT_EXCLUDED_DIRS
    if args.no_defaults:
        Config.excluded_dirs = []
    if args.exclude_dir:
        for exclude in args.exclude_dir:
            Config.excluded_dirs.append(exclude)
    Config.verbosity = args.verbose
    total_files = total_lines = 0
    for target_name in args.target:
        files, lines = scan(target_name)
        total_files += files
        total_lines += lines
    if len(args.target) > 1:
        print(f"Total: Files: {total_files} Lines: {total_lines}")
