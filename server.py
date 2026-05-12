from flask import Flask, request, jsonify
from vault import unlock_vault, get_password, add_generated_entry, list_entries

app = Flask(__name__)

session = {
    "key": None,
    "vault_data": None
}

@app.route("/login", methods=["POST"])
def login():
    data     = request.get_json()
    password = data.get("master_password")

    key, vault_data = unlock_vault(password)

    if key is None:
        return jsonify({"success": False, "error": "Wrong password"}), 401

    session["key"]        = key
    session["vault_data"] = vault_data
    return jsonify({"success": True})


@app.route("/get", methods=["POST"])
def get():
    if session["key"] is None:
        return jsonify({"error": "Not logged in"}), 401

    data     = request.get_json()
    site     = data.get("site")
    username = data.get("username")

    password = get_password(session["vault_data"], session["key"], site, username)

    if password is None:
        return jsonify({"error": "No entry found"}), 404

    return jsonify({"password": password})


@app.route("/add", methods=["POST"])
def add():
    if session["key"] is None:
        return jsonify({"error": "Not logged in"}), 401

    data     = request.get_json()
    site     = data.get("site")
    username = data.get("username")
    length   = data.get("length", 20)

    password = add_generated_entry(session["vault_data"], session["key"], site, username, length)
    return jsonify({"password": password})


@app.route("/list", methods=["GET"])
def list_all():
    if session["key"] is None:
        return jsonify({"error": "Not logged in"}), 401

    entries = list_entries(session["vault_data"])
    return jsonify({"entries": entries})


@app.route("/logout", methods=["POST"])
def logout():
    session["key"]        = None
    session["vault_data"] = None
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(port=5000)