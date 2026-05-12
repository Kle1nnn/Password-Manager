# 🔐 PM-Vault

A command-line password manager built in Python. No cloud, no third parties. Everything runs locally and stays encrypted on your machine.

---

## How It Works

**Generated passwords** are derived from your master key + site + username using HMAC-SHA256. Never written to disk — same inputs always reproduce the same password.

**Stored passwords** are encrypted with AES-256-GCM before saving. A random nonce is generated per entry.

**Your master password is never stored. Ever.**

---

## Installation

```bash
git clone https://github.com/Kle1nnn/Password-Manager
cd pm-vault
pip install cryptography flask
```

---

## Usage

```bash
# First time setup
python main.py --init

# Every time after
python main.py

# Run the local API server
python server.py
```

---

## Security

| Component | Implementation |
|---|---|
| Key derivation | PBKDF2-HMAC-SHA256, 600,000 iterations |
| Password generation | HMAC-SHA256(master\_key \| site \| username) |
| Encryption | AES-256-GCM, random nonce per entry |
| Salt | 32 bytes, `os.urandom`, stored per vault |
| Vault writes | Atomic `.tmp` → replace |

---

## Project Structure

```
pm-vault/
├── main.py        # CLI interface
├── vault.py       # Vault CRUD operations
├── encrypt.py     # Cryptographic primitives
├── server.py      # Local Flask API server
└── extension/
    ├── manifest.json
    ├── popup.html
    └── popup.js
```

---

## Roadmap

- [x] v1 — CLI password manager
- [x] Browser extension for Firefox and Brave with full GUI

---

> ⚠️ **Do not lose your master password. There is no recovery mechanism.**
