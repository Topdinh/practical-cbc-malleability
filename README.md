Practical CBC Malleability Attack & Secure Encrypt-then-MAC Design
A practical demonstration of CBC malleability, controlled bit-flipping attacks, and a secure Encrypt-then-MAC (EtM) mitigation implemented in Python.

Overview
AES in CBC mode provides confidentiality, but does not guarantee integrity.
This project demonstrates how an attacker can modify ciphertext in a controlled way, altering meaningful fields in the decrypted plaintext without knowing the secret key. It then implements a correct countermeasure using Encrypt-then-MAC with HMAC-SHA256.
The key lesson:
	Confidentiality does not imply integrity.

What This Project Demonstrates
+ Implementation of AES-CBC with PKCS#7 padding
+ Practical bit-flipping attack exploiting CBC malleability
+ Controlled modification of structured transaction data
+ Secure redesign using Encrypt-then-MAC
+ Verify-before-decrypt principle
+ Security reasoning and composition analysis

CBC Malleability in Practice
In CBC mode, each plaintext block depends on the previous ciphertext block during decryption.
If an attacker modifies a ciphertext block:
+ The corresponding plaintext block is modified predictably
+ Decryption still succeeds
+ No error is raised (in CBC-only systems)
Example target field:
	AMOUNT=000100;
After controlled ciphertext modification:
	AMOUNT=000999;
The attacker does not need the encryption key.
This attack succeeds because CBC-only encryption provides no integrity protection.

Secure Fix: Encrypt-then-MAC (EtM)
To prevent manipulation, this project implements Encrypt-then-MAC:
01. Encrypt plaintext using AES-CBC
02. Compute HMAC over (IV || Ciphertext)
03. Send: IV || Ciphertext || Tag
04. Verify MAC before decrypting
If the packet is modified:
	ValueError: AUTHENTICATION FAILED
Decryption is never executed on unauthenticated data.

Why Verify-Before-Decrypt Matters
Authenticating before decryption:
+ Prevents controlled plaintext manipulation
+ Eliminates CBC malleability exploitation
+ Reduces risk of padding-oracle style attacks
+ Avoids processing corrupted structured data
Correct composition of primitives is essential for secure system design.

## Project Structure

practical-cbc-malleability/
├── src/cbc_malleability/
│   ├── core/        # CBC, HMAC, EtM implementation
│   ├── attacks/     # Bit-flipping attack logic
│   └── benchmark/   # Performance measurement scaffold
├── scripts/         # Demonstration scripts
├── tests/           # Unit tests
├── data/            # Sample keys and packets
└── pyproject.toml   # Python packaging configuration
The project follows a proper src layout and can be installed in editable mode.

Running the Demo
Install:
	python -m pip install -e .

Run Encrypt-then-MAC demo:
	python scripts/demo_etm.py

You should see successful encryption and decryption.
To observe tampering detection, modify the packet and re-run decryption.

Security Analysis
This project highlights several important security principles:
+ AES is secure, but composition matters.
+ CBC provides confidentiality, not integrity.
+ Malleability is a structural property, not a broken cipher.
+ Encrypt-then-MAC prevents ciphertext manipulation under standard assumptions.
+ Authentication must precede decryption.

Real-World Context
Historically, improper composition of encryption and authentication led to vulnerabilities in protocols such as early TLS versions (e.g., padding oracle attacks).
Modern cryptographic standards recommend:
+ AES-GCM
+ ChaCha20-Poly1305
+ Authenticated Encryption with Associated Data (AEAD)
Encrypt-then-MAC is a correct manual composition when AEAD is not used.

Key Takeaway
Strong algorithms do not automatically produce secure systems.
Security depends on:
+ Correct primitive selection
+ Proper composition
+ Explicit integrity protection
+ Strict verification order
This project demonstrates how a seemingly secure CBC system can be vulnerable — and how to fix it properly.

Author

Topdinh
GitHub: https://github.com/Topdinh
