from __future__ import annotations

import argparse
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

from dissect.target.tools import (
    build_magic,
    build_pluginlist,
    dd,
    diff,
    dump,
    fs,
    info,
    inspect,
    mount,
    qfind,
    query,
    reg,
    shell,
    yara,
)

_COMMANDS: dict[str, tuple[str, Callable[[], int | None]]] = {
    "build-magic": ("Build magic signatures", build_magic.main),
    "build-pluginlist": ("Build the plugin list", build_pluginlist.main),
    "dd": ("Copy target data", dd.main),
    "diff": ("Show differences between targets", diff.main),
    "dump": ("Dump target data", dump.main),
    "fs": ("Interact with the target filesystem", fs.main),
    "info": ("Display target information", info.main),
    "inspect": ("Inspect a target", inspect.main),
    "mount": ("Mount a target filesystem", mount.main),
    "qfind": ("Quick find on a target", qfind.main),
    "query": ("Query target plugins", query.main),
    "reg": ("Interact with the target registry", reg.main),
    "shell": ("Open an interactive shell on a target", shell.main),
    "yara": ("Run YARA rules on a target", yara.main),
}

root = argparse.ArgumentParser("dissect-target")
subparsers = root.add_subparsers(dest="command")

for name, (help_text, _) in _COMMANDS.items():
    subparsers.add_parser(name, help=help_text, add_help=False)


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in _COMMANDS:
        root.print_help()
        return 1

    command = sys.argv[1]
    _, func = _COMMANDS[command]

    # Strip the subcommand so each tool's own ArgumentParser sees clean argv.
    sys.argv = [f"{sys.argv[0]} {command}", *sys.argv[2:]]
    return func() or 0


if __name__ == "__main__":
    sys.exit(main())
