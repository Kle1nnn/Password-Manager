import json
import base64
import os
from datetime import datetime, timezone
from pathlib import Path
from encrypt import derive_key, generate_salt, encrypt, decrypt, generate_site_password

VAULT_FILE = Path.home() / ".my_vault.json"

def create_vault(master_password):
    if VAULT_FILE.exists():
        print("Vault file already exists")
        return False

    salt = generate_salt()
    key  = derive_key(master_password, salt)

    vault_data = {
        "salt":    base64.b64encode(salt).decode(),
        "entries": {}
    }

    with open(VAULT_FILE, "w") as f:
        json.dump(vault_data, f, indent=2)

    print(f"Vault created at {VAULT_FILE}")
    return key


def unlock_vault(master_password):
    if not VAULT_FILE.exists():
        print("No vault file found.")
        return None, None

    with open(VAULT_FILE, "r") as f:
        vault_data = json.load(f)

    salt = base64.b64decode(vault_data["salt"])
    key  = derive_key(master_password, salt)

    return key, vault_data


def save_vault(vault_data):
    tmp = VAULT_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(vault_data, f, indent=2)
    tmp.replace(VAULT_FILE)


def add_generated_entry(vault_data, key, site, username, length=20):
    entry_key = f"{site.lower()}::{username.lower()}"
    now = datetime.now(timezone.utc).isoformat()

    vault_data["entries"][entry_key] = {
        "site":     site,
        "username": username,
        "type":     "generated",
        "length":   length,
        "version":  1,
        "created":  now,
        "modified": now,
    }

    save_vault(vault_data)
    password = generate_site_password(key, site, username, length, 1)
    return password


def add_stored_entry(vault_data, key, site, username, password):
    entry_key = f"{site.lower()}::{username.lower()}"
    now = datetime.now(timezone.utc).isoformat()

    vault_data["entries"][entry_key] = {
        "site":     site,
        "username": username,
        "type":     "stored",
        "password": encrypt(password, key),
        "created":  now,
        "modified": now,
    }

    save_vault(vault_data)


def get_password(vault_data, key, site, username):
    entry_key = f"{site.lower()}::{username.lower()}"
    entry = vault_data["entries"].get(entry_key)

    if not entry:
        return None

    if entry["type"] == "stored":
        return decrypt(entry["password"], key)
    else:
        return generate_site_password(
            key,
            entry["site"],
            entry["username"],
            entry["length"],
            entry["version"],
        )


def list_entries(vault_data):
    return list(vault_data["entries"].values())


def delete_entry(vault_data, site, username):
    entry_key = f"{site.lower()}::{username.lower()}"
    if entry_key in vault_data["entries"]:
        del vault_data["entries"][entry_key]
        save_vault(vault_data)
        return True
    return False