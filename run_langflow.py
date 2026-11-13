"""
run_langflow.py — Starts the Langflow server and auto-imports the EduSimplify flow.

Usage:
    py run_langflow.py

Then open: http://localhost:7860
Import the flow via: Flow menu → Import → select edusimplify_flow.json
"""

import os
import sys
import time
import json
import subprocess
import urllib.request
import urllib.error

LANGFLOW_PORT = 7860
FLOW_FILE = os.path.join(os.path.dirname(__file__), "edusimplify_flow.json")
LANGFLOW_API = f"http://localhost:{LANGFLOW_PORT}/api/v1"


def wait_for_server(timeout=60):
    """Poll until Langflow is ready."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"{LANGFLOW_API}/flows/", timeout=2)
            return True
        except Exception:
            time.sleep(2)
    return False


def import_flow():
    """POST the flow JSON to Langflow's upload endpoint."""
    with open(FLOW_FILE, "r", encoding="utf-8") as f:
        flow_data = json.load(f)

    payload = json.dumps(flow_data).encode("utf-8")
    req = urllib.request.Request(
        f"{LANGFLOW_API}/flows/",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            flow_id = result.get("id", "unknown")
            print(f"\n✅ Flow imported successfully! Flow ID: {flow_id}")
            print(f"   Open: http://localhost:{LANGFLOW_PORT}/flow/{flow_id}\n")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "already exists" in body or e.code == 409:
            print("\n✅ Flow already exists in Langflow — skipping import.\n")
        else:
            print(f"\n⚠️  Could not auto-import flow (HTTP {e.code}): {body}")
            print(f"   Manually import: Flow menu → Import → edusimplify_flow.json\n")
    except Exception as ex:
        print(f"\n⚠️  Auto-import skipped: {ex}")
        print(f"   Manually import: Flow menu → Import → edusimplify_flow.json\n")


if __name__ == "__main__":
    python = sys.executable
    print("=" * 60)
    print("  EduSimplify AI — Langflow Server")
    print("=" * 60)
    print(f"\n▶  Starting Langflow on http://localhost:{LANGFLOW_PORT} …\n")

    env = os.environ.copy()
    proc = subprocess.Popen(
        [python, "-m", "langflow", "run", "--port", str(LANGFLOW_PORT), "--no-open-browser"],
        env=env,
    )

    print("⏳ Waiting for Langflow to be ready …")
    if wait_for_server(timeout=90):
        print("✅ Langflow is up!")
        import_flow()
    else:
        print("⚠️  Langflow took too long to start. Import the flow manually.")
        print(f"   Flow menu → Import → edusimplify_flow.json\n")

    print(f"🌐 Open Langflow at: http://localhost:{LANGFLOW_PORT}")
    print("   Press Ctrl+C to stop.\n")

    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        print("\nLangflow stopped.")
