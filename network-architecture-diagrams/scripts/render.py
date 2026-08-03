#!/usr/bin/env python3
"""Render a diagram source file to PNG/SVG.

Auto-detects the source format from its extension and shells out to the
right renderer:

    .mmd / .mermaid  -> Mermaid CLI via `npx @mermaid-js/mermaid-cli`
    .dot / .gv       -> Graphviz `dot`
    .py              -> executed with the current Python (a mingrammer
                        `diagrams` script writes its own output file)

Usage:
    python render.py diagram.mmd -o diagram.png
    python render.py topology.dot -o topology.svg
    python render.py architecture.py

Design goal: never fail silently. If a renderer is missing, print the exact
install command for this environment and exit non-zero, so the caller knows
what to do instead of guessing.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _run(cmd):
    """Run a command, streaming output; return the exit code."""
    print("+ " + " ".join(cmd), file=sys.stderr)
    return subprocess.run(cmd).returncode


def _puppeteer_config() -> str:
    """Write a puppeteer config that lets Chromium launch in containers/CI.

    Headless Chromium refuses to run as root without --no-sandbox, which is
    exactly the situation inside most CI runners and dev containers. Passing
    the flag here keeps the common case working instead of dead-ending on a
    sandbox error. If PUPPETEER_EXECUTABLE_PATH is set (e.g. a preinstalled
    browser), honor it so puppeteer doesn't try to download its own.
    """
    cfg = {"args": ["--no-sandbox", "--disable-setuid-sandbox"]}
    exe = os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if exe:
        cfg["executablePath"] = exe
    fd, path = tempfile.mkstemp(prefix="puppeteer-", suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(cfg, f)
    return path


def render_mermaid(src: Path, out: Path) -> int:
    # Prefer a globally installed mmdc; otherwise use npx, which fetches the
    # package on demand so no global install is required.
    if shutil.which("mmdc"):
        base = ["mmdc"]
    elif shutil.which("npx"):
        base = ["npx", "-y", "@mermaid-js/mermaid-cli"]
    else:
        print("Mermaid renderer not found. Install Node.js (which provides "
              "npx), or run:\n  npm install -g @mermaid-js/mermaid-cli\n"
              "Or skip rendering — a ```mermaid fenced block renders as-is "
              "on GitHub and in Claude artifacts.", file=sys.stderr)
        return 1
    cfg = _puppeteer_config()
    try:
        return _run(base + ["-p", cfg, "-i", str(src), "-o", str(out)])
    finally:
        try:
            os.unlink(cfg)
        except OSError:
            pass


def render_dot(src: Path, out: Path) -> int:
    if not shutil.which("dot"):
        print("Graphviz not found. Install it:\n"
              "  Debian/Ubuntu: sudo apt-get install -y graphviz\n"
              "  macOS:         brew install graphviz\n"
              "  conda:         conda install -c conda-forge graphviz",
              file=sys.stderr)
        return 1
    fmt = out.suffix.lstrip(".").lower() or "png"
    return _run(["dot", f"-T{fmt}", str(src), "-o", str(out)])


def run_python(src: Path) -> int:
    # A `diagrams` script sets its own filename/outformat, so just execute it.
    print("Running Python diagram script; it writes its own output file "
          "(check the script's filename= / Diagram title).", file=sys.stderr)
    return _run([sys.executable, str(src)])


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", type=Path, help="diagram source (.mmd/.dot/.py)")
    p.add_argument("-o", "--output", type=Path,
                   help="output image path (.png/.svg); ignored for .py "
                        "scripts, which name their own output")
    args = p.parse_args()

    src = args.source
    if not src.exists():
        print(f"error: source not found: {src}", file=sys.stderr)
        return 2

    ext = src.suffix.lower()
    if ext in (".mmd", ".mermaid"):
        out = args.output or src.with_suffix(".png")
        return render_mermaid(src, out)
    if ext in (".dot", ".gv"):
        out = args.output or src.with_suffix(".svg")
        return render_dot(src, out)
    if ext == ".py":
        return run_python(src)

    print(f"error: unrecognized source type '{ext}'. Expected "
          ".mmd/.mermaid, .dot/.gv, or .py", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
