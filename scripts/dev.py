#!/usr/bin/env python3
"""
Dev runner for ai-translate-assistant
- Start FastAPI backend (uvicorn) in ./backend
- Start static frontend server (python -m http.server) in ./frontend

Usage:
  python scripts/dev.py
  python scripts/dev.py --api-port 8000 --web-port 5173
  python scripts/dev.py --no-reload
"""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


def is_windows() -> bool:
    return os.name == "nt"


def run_process(cmd: list[str], cwd: Path) -> subprocess.Popen:
    """
    Start process in a new process group/session so we can terminate it cleanly.
    """
    creationflags = 0
    preexec_fn = None

    if is_windows():
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore[attr-defined]
    else:
        preexec_fn = os.setsid  # start new session

    return subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=sys.stdout,
        stderr=sys.stderr,
        text=False,
        creationflags=creationflags,
        preexec_fn=preexec_fn,
    )


def terminate_process(p: subprocess.Popen, name: str) -> None:
    if p.poll() is not None:
        return

    try:
        if is_windows():
            # Try to stop the whole process group nicely
            try:
                p.send_signal(signal.CTRL_BREAK_EVENT)  # type: ignore[attr-defined]
                time.sleep(0.8)
            except Exception:
                pass
            p.terminate()
        else:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        time.sleep(1.2)
    except Exception:
        pass

    if p.poll() is None:
        try:
            if is_windows():
                p.kill()
            else:
                os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except Exception:
            pass

    print(f"[dev] stopped: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-host", default="127.0.0.1", help="Backend host")
    parser.add_argument("--api-port", type=int, default=8000, help="Backend port")
    parser.add_argument("--web-host", default="127.0.0.1", help="Frontend host")
    parser.add_argument("--web-port", type=int, default=5173, help="Frontend port")
    parser.add_argument("--no-reload", action="store_true", help="Disable uvicorn --reload")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    backend_dir = repo_root / "backend"
    frontend_dir = repo_root / "frontend"

    if not backend_dir.exists():
        print(f"[dev] ERROR: backend directory not found: {backend_dir}")
        return 1
    if not frontend_dir.exists():
        print(f"[dev] ERROR: frontend directory not found: {frontend_dir}")
        return 1

    # Backend command (assumes backend/main.py defines `app`)
    backend_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "main:app",
        "--host",
        args.api_host,
        "--port",
        str(args.api_port),
    ]
    if not args.no_reload:
        backend_cmd.append("--reload")

    # Frontend static server
    frontend_cmd = [
        sys.executable,
        "-m",
        "http.server",
        str(args.web_port),
        "--bind",
        args.web_host,
    ]

    print("[dev] starting backend:", " ".join(backend_cmd))
    api_proc = run_process(backend_cmd, cwd=backend_dir)

    time.sleep(0.6)

    print("[dev] starting frontend:", " ".join(frontend_cmd))
    web_proc = run_process(frontend_cmd, cwd=frontend_dir)

    api_url = f"http://{args.api_host}:{args.api_port}"
    web_url = f"http://{args.web_host}:{args.web_port}"

    print()
    print("[dev] ✅ running")
    print(f"[dev] API  -> {api_url}")
    print(f"[dev] WEB  -> {web_url}")
    print("[dev] press Ctrl+C to stop")
    print()

    try:
        while True:
            if api_proc.poll() is not None:
                print(f"[dev] backend exited with code {api_proc.returncode}")
                break
            if web_proc.poll() is not None:
                print(f"[dev] frontend exited with code {web_proc.returncode}")
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[dev] stopping...")

    terminate_process(web_proc, "frontend")
    terminate_process(api_proc, "backend")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
