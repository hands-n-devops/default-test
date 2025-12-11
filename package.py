# vuln_app.py
# This file intentionally contains insecure patterns for testing CodeQL/static analysis.
# DO NOT RUN with production data or expose to public networks.

import os
import subprocess
import sqlite3
import pickle
import hashlib
import ssl
import requests
import tempfile

# -------------------------
# VULN: Hardcoded credentials
# -------------------------
API_KEY = "AKIAAAAAAAAAAAAAAAAA"  # VULN: hardcoded secret / credential
DB_PASSWORD = "P@ssw0rd123"        # VULN: hardcoded password

# -------------------------
# VULN: SQL Injection via string formatting
# -------------------------
def get_user_from_db(username):
    # VULN: SQL built with string concatenation/formatting
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '%s'" % username
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# -------------------------
# VULN: Command Injection / shell=True
# -------------------------
def run_system_command(user_input):
    # VULN: using shell=True with untrusted input
    cmd = f"ls -la {user_input}"
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

# -------------------------
# VULN: Insecure deserialization (pickle.loads on user input)
# -------------------------
def load_user_profile(serialized_blob):
    # VULN: untrusted pickle loads
    obj = pickle.loads(serialized_blob)
    return obj

# -------------------------
# VULN: Use of eval on user data
# -------------------------
def calculate(expression):
    # VULN: eval on user-controlled expression
    return eval(expression)

# -------------------------
# VULN: Path traversal via naive open
# -------------------------
def read_config(filename):
    # VULN: no validation of filename -> path traversal possible
    with open("/app/configs/" + filename, "r") as f:
        return f.read()

# -------------------------
# VULN: Use of insecure temp file function
# -------------------------
def make_temp_file():
    name = tempfile.mktemp()  # VULN: mktemp is insecure (race condition)
    with open(name, "w") as f:
        f.write("temporary data")
    return name

# -------------------------
# VULN: Weak hashing algorithm for passwords
# -------------------------
def create_user_hash(password):
    # VULN: using MD5 for password hashing (weak)
    return hashlib.md5(password.encode()).hexdigest()

# -------------------------
# VULN: Insecure TLS verification
# -------------------------
def fetch_remote(url):
    # VULN: disabling TLS verification
    # (requests is used here purely for test; do NOT set verify=False in prod)
    r = requests.get(url, verify=False)
    return r.text

# -------------------------
# Example main to exercise behaviors
# -------------------------
def main():
    # Example inputs (in real tests, feed via test harness)
    print("=== VULNERABLE TEST APP ===")

    # Hardcoded credential usage (for detection)
    print("Using API key length:", len(API_KEY))

    # SQL injection example
    user = "alice' OR '1'='1"
    print("SQL query results for user:", get_user_from_db(user))

    # Command injection example
    run_system_command("; echo hacked")

    # Insecure deserialization example (we pass a safe serialized object for unit test)
    safe_blob = pickle.dumps({"user": "test"})
    print("Deserialized object:", load_user_profile(safe_blob))

    # eval example
    print("Eval result:", calculate("1 + 2"))

    # Path traversal example (unsafe example)
    try:
        print("Read conf:", read_config("../secrets.txt"))
    except Exception as e:
        print("Read config failed (expected in tests):", e)

    # Temp file example
    print("Created temp file:", make_temp_file())

    # Weak hash example
    print("MD5 hash:", create_user_hash("password123"))

    # Insecure TLS fetch (note: this will raise warnings about unverified HTTPS)
    try:
        fetch_remote("https://example.com")
    except Exception as e:
        print("Fetch remote likely blocked during offline tests:", e)

if __name__ == "__main__":
    main()
