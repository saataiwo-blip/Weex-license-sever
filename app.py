from flask import Flask, request, jsonify

app = Flask(__name__)

# Add your customer license keys here.
# Format: "KEY": "machine_id or None if not yet locked to a device"
VALID_KEYS = {
    "WX-DEMO-0001": None,
    "WX-DEMO-0002": None,
}

@app.route("/")
def home():
    return "License server is running."

@app.route("/verify")
def verify():
    key = request.args.get("key")
    machine_id = request.args.get("machine_id")

    if not key or key not in VALID_KEYS:
        return jsonify({"valid": False, "reason": "Key not found"}), 200

    locked_machine = VALID_KEYS[key]

    # First time this key is used -> lock it to this machine
    if locked_machine is None:
        VALID_KEYS[key] = machine_id
        return jsonify({"valid": True, "reason": "Key activated"}), 200

    # Key already locked -> must match
    if locked_machine == machine_id:
        return jsonify({"valid": True, "reason": "Key OK"}), 200
    else:
        return jsonify({"valid": False, "reason": "Key already used on another device"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
