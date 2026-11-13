"""
run_langflow.py — Starts the Langflow server and auto-imports the EduSimplify flow.

Usage:
    py run_langflow.py

Then open: http://localhost:7860
Login with:  admin / admin123  (set in .env)
"""

import os
import sys
import time
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# Load .env so LANGFLOW_* vars are available
load_dotenv(Path(__file__).parent / ".env")

LANGFLOW_PORT = 7860
FLOW_FILE = Path(__file__).parent / "edusimplify_flow.json"
LANGFLOW_API = f"http://localhost:{LANGFLOW_PORT}/api/v1"


def wait_for_server(timeout=90):
    """Poll until Langflow HTTP endpoint is ready."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"http://localhost:{LANGFLOW_PORT}", timeout=3)
            return True
        except Exception:
            time.sleep(3)
    return False


def get_auth_token():
    """Obtain a JWT token from Langflow login endpoint."""
    user = os.getenv("LANGFLOW_SUPERUSER", "admin")
    pwd = os.getenv("LANGFLOW_SUPERUSER_PASSWORD", "admin123")
    payload = json.dumps({"username": user, "password": pwd}).encode()
    req = urllib.request.Request(
        f"{LANGFLOW_API}/login",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("access_token", "")
    except Exception as ex:
        print(f"⚠️  Could not authenticate with Langflow: {ex}")
        return ""


def import_flow(token: str):
    """POST the flow JSON to Langflow's upload endpoint."""
    with open(FLOW_FILE, "r", encoding="utf-8") as f:
        flow_data = json.load(f)

    payload = json.dumps(flow_data).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(
        f"{LANGFLOW_API}/flows/",
        data=payload,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            flow_id = result.get("id", "unknown")
            print(f"\n✅ Flow imported! Flow ID: {flow_id}")
            print(f"   Open: http://localhost:{LANGFLOW_PORT}/flow/{flow_id}\n")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "already exists" in body or e.code == 409:
            print("\n✅ Flow already exists — skipping import.\n")
        else:
            print(f"\n⚠️  Auto-import skipped (HTTP {e.code}). Import manually:")
            print(f"   Flow menu → Import → edusimplify_flow.json\n")
    except Exception as ex:
        print(f"\n⚠️  Auto-import skipped: {ex}")
        print(f"   Flow menu → Import → edusimplify_flow.json\n")


if __name__ == "__main__":
    print("=" * 60)
    print("  EduSimplify AI — Langflow Server")
    print("=" * 60)
    print(f"\n▶  Starting Langflow on http://localhost:{LANGFLOW_PORT} …\n")

    env = os.environ.copy()
    # Ensure required Langflow auth env vars are passed to the subprocess
    env.setdefault("LANGFLOW_SUPERUSER",          os.getenv("LANGFLOW_SUPERUSER", "admin"))
    env.setdefault("LANGFLOW_SUPERUSER_PASSWORD",  os.getenv("LANGFLOW_SUPERUSER_PASSWORD", "admin123"))
    env.setdefault("LANGFLOW_AUTO_LOGIN",          os.getenv("LANGFLOW_AUTO_LOGIN", "false"))

    langflow_exe = Path(sys.executable).parent / "Scripts" / "langflow.exe"
    if not langflow_exe.exists():
        langflow_exe = "langflow"  # fallback to PATH

    proc = subprocess.Popen(
        [str(langflow_exe), "run", "--port", str(LANGFLOW_PORT), "--no-open-browser"],
        env=env,
    )

    print("⏳ Waiting for Langflow to be ready (may take 30-60 s on first run) …")
    if wait_for_server(timeout=120):
        print("✅ Langflow is up!")
        token = get_auth_token()
        import_flow(token)
    else:
        print("⚠️  Langflow took too long. Import the flow manually once it starts.")
        print(f"   Flow menu → Import → edusimplify_flow.json\n")

    print(f"🌐 Open Langflow: http://localhost:{LANGFLOW_PORT}")
    print(f"   Login:  admin / admin123")
    print("   Press Ctrl+C to stop.\n")

    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        print("\nLangflow stopped.")
