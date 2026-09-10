"""
WEEX Bot License Server
=========================
A minimal Flask API that checks whether a license key is valid. Deployed on
Render (free tier), so keep in mind:
  - Free instances spin down after inactivity — the first request after a
    while can take up to ~50 seconds to respond while it wakes up.
  - Free tier has no persistent disk, so valid keys are stored in this code
    (or via an environment variable) rather than a database file — adding a
    new key means updating LICENSE_KEYS below and redeploying, or setting
    the LICENSE_KEYS environment variable in Render's dashboard.

Endpoints:
  GET  /                 -> health check
  POST /verify           -> body: {"key": "ABC-123"} -> {"valid": true/false}
"""

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---- Valid license keys ----
# Option 1 (simplest to start): hardcode keys here, redeploy to add more.
HARDCODED_KEYS = {
    "Fytrhuyr",
}

# Option 2 (no redeploy needed to add a key): set an env var in Render's
# dashboard called LICENSE_KEYS with a comma-separated list, e.g.
# LICENSE_KEYS=ABC-123,DEF-456
env_keys = os.environ.get("LICENSE_KEYS", "")
ENV_KEYS = set(k.strip() for k in env_keys.split(",") if k.strip())

VALID_KEYS = HARDCODED_KEYS | ENV_KEYS


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "wx-license-server"})


@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json(silent=True) or {}
    key = str(data.get("key", "")).strip()

    if not key:
        return jsonify({"valid": False, "reason": "No key provided"}), 400

    is_valid = key in VALID_KEYS
    return jsonify({"valid": is_valid})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
