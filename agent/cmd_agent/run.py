"""
Entry point for the CLI Tool Builder Agent.

Usage:
    python run.py "Build a CLI-based habit tracker with streak counter"
    python run.py "Build a password generator with strength scoring"
    python run.py "Build a CLI calculator with history and memory"
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cmd_builder_agent import build_cli_tool


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py \"<description of CLI tool>\"")
        print()
        print("Examples:")
        print('  python run.py "Build a CLI todo list app with add/delete/list/done"')
        print('  python run.py "Build a CLI-based habit tracker with streak counter"')
        print('  python run.py "Build a password generator with strength scoring"')
        print('  python run.py "Build a CLI calculator with history and memory"')
        print('  python run.py "Build a CLI note taking app with search"')
        sys.exit(1)

    request = " ".join(sys.argv[1:])
    print(f"Building: {request}")
    print("=" * 60)

    result = build_cli_tool(request, verbose=True)

    print()
    print("=" * 60)
    print("  RESULT")
    print("=" * 60)
    if result["success"]:
        print(f"  Status:  SUCCESS")
        print(f"  File:    {result['filepath']}")
        print(f"  Turns:   {result['turns_used']}")
    else:
        print(f"  Status:  FAILED (agent did not save a file)")
        print(f"  Turns:   {result['turns_used']}")
    print("-" * 60)
    print(result["summary"])

    if result["success"] and result["filepath"]:
        print()
        print("  To run your new CLI tool:")
        print(f"    python {result['filepath']} --help")


if __name__ == "__main__":
    main()
