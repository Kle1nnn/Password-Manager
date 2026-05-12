# 🔐 PM-Vault

A command-line password manager built in Python. No cloud, no third parties. Everything runs locally and stays encrypted on your machine.

---

## How It Works

- **Generated passwords** are derived from your master key + site + username using HMAC-SHA256. Never written to disk — same inputs always reproduce the same password.
- **Stored passwords** are encrypted with AES-256-GCM before saving.
- **Your master password** is never stored. Ever.

---

## Installation

```bash
git clone https://github.com/yourusername/pm-vault.git
cd pm-vault
pip install cryptography
```

---

## Usage

```bash
# First time
python main.py --init

# Every time after
python main.py
```

---

## Security

| Component | Implementation |
|-----------|---------------|
| Key derivation | PBKDF2-HMAC-SHA256, 600,000 iterations |
| Password generation | HMAC-SHA256(master_key + site + username) |
| Encryption | AES-256-GCM, random nonce per entry |

---

## Roadmap

- [x] v1 — CLI password manager
- [ ] v2 — Browser extension for Firefox and Brave with full GUI

---

> ⚠️ Do not lose your master password. There is no recovery mechanism.
