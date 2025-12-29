#!/usr/bin/env python3

import sys
import subprocess
import shutil
import json
from pathlib import Path

# ============================================================
# Argument parsing
# ============================================================
args = sys.argv[1:]
json_output = "-j" in args
show_deinstall = "-d" in args
run_tests = "-u" in args

for flag in ("-j", "-d", "-u"):
    if flag in args:
        args.remove(flag)

if run_tests:
    import unittest
    import tempfile

    class TestHelpers(unittest.TestCase):
        def test_run_missing_command(self):
            self.assertEqual(run(["doesnotexist"]), "")

        def test_keyword_match(self):
            self.assertTrue(match("cura", "Ultimaker Cura"))

    unittest.main(argv=[sys.argv[0]])
    sys.exit(0)

if not args:
    print("Usage: fpack.py [-j] [-d] [-u] <keyword>")
    sys.exit(1)

KEYWORD = args[0].lower()

# ============================================================
# Helpers
# ============================================================
def run(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""

def match(keyword, text):
    return keyword in text.lower()

def out(text=""):
    if not json_output:
        print(text)

def header(title):
    if not json_output:
        print(f"\n=== {title} ===")

# ============================================================
# Result structure
# ============================================================
result = {
    "keyword": KEYWORD,
    "apt": [],
    "flatpak": [],
    "snap": [],
    "appimage": [],
    "path": [],
    "config_candidates": [],
    "multiple_installations": False,
    "deinstall_hints": []
}

# ============================================================
# APT / DPKG
# ============================================================
header("APT / dpkg")

apt_list = run(["apt", "list", "--installed"])
for line in apt_list.splitlines():
    if match(KEYWORD, line):
        pkg = line.split("/")[0]
        version = line.split()[1] if len(line.split()) > 1 else "unknown"

        entry = {
            "package": pkg,
            "version": version,
            "deinstall": f"sudo apt remove {pkg}"
        }

        result["apt"].append(entry)
        out(f"- {pkg} ({version})")

# ============================================================
# Flatpak
# ============================================================
header("Flatpak")

if shutil.which("flatpak"):
    flatpak_list = run(["flatpak", "list", "--columns=name,application,version"])
    for line in flatpak_list.splitlines():
        if match(KEYWORD, line):
            name, appid, version = line.split("\t")

            entry = {
                "name": name,
                "appid": appid,
                "version": version,
                "deinstall": f"flatpak uninstall {appid}"
            }

            result["flatpak"].append(entry)
            out(f"- {name} ({appid}) {version}")
else:
    out("Flatpak not installed.")

# ============================================================
# Snap
# ============================================================
header("Snap")

if shutil.which("snap"):
    snap_list = run(["snap", "list"])
    for line in snap_list.splitlines()[1:]:
        if match(KEYWORD, line):
            name, version = line.split()[:2]

            entry = {
                "name": name,
                "version": version,
                "deinstall": f"sudo snap remove {name}"
            }

            result["snap"].append(entry)
            out(f"- {name} {version}")
else:
    out("Snap not installed.")

# ============================================================
# AppImage
# ============================================================
header("AppImage")

for d in [Path.home(), Path.home() / "Applications", Path.home() / "AppImages"]:
    if d.exists():
        for f in d.glob("*.AppImage"):
            if match(KEYWORD, f.name):
                entry = {
                    "file": str(f),
                    "deinstall": f"rm '{f}'"
                }
                result["appimage"].append(entry)
                out(f"- {f}")

# ============================================================
# PATH binary
# ============================================================
header("Executable in PATH")

binary = shutil.which(KEYWORD)
if binary:
    result["path"].append(binary)
    out(f"- {binary}")

# ============================================================
# Config candidates
# ============================================================
header("Possible config locations")

for base in [Path.home() / ".config", Path.home() / ".local/share"]:
    if base.exists():
        for p in base.iterdir():
            if match(KEYWORD, p.name):
                result["config_candidates"].append(str(p))
                out(f"- {p}")

# ============================================================
# Multiple installation detection
# ============================================================
install_sources = sum(bool(result[x]) for x in ["apt", "flatpak", "snap", "appimage"])
if install_sources > 1:
    result["multiple_installations"] = True
    out("\n⚠ Multiple installations detected!")

# ============================================================
# Deinstall hints
# ============================================================
if show_deinstall:
    header("Deinstallation hints")

    for section in ("apt", "flatpak", "snap", "appimage"):
        for entry in result[section]:
            hint = entry.get("deinstall")
            if hint:
                result["deinstall_hints"].append(hint)
                out(hint)

# ============================================================
# JSON output
# ============================================================
if json_output:
    print(json.dumps(result, indent=2))
