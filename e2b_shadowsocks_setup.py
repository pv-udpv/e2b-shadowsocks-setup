#!/usr/bin/env python3
"""
E2B Shadowsocks Complete Setup
Версия: 1.0
"""

import os
import sys
import json
import subprocess
import tarfile
import hashlib
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

VERSION = "1.24.0"
ARCH = "x86_64-unknown-linux-musl"
GITHUB_RELEASE = f"https://github.com/shadowsocks/shadowsocks-rust/releases/download/v{VERSION}"
TARBALL_NAME = f"shadowsocks-v{VERSION}.{ARCH}.tar.xz"
TARBALL_URL = f"{GITHUB_RELEASE}/{TARBALL_NAME}"
SHA256_URL = f"{TARBALL_URL}.sha256"

SERVER_CONFIG = {
    "server": "46.161.5.162",
    "server_port": 9999,
    "password": "QpJ6f5W/7DQlgZD5qm8IvlMsUDjzi8CRclffXD3kmWY=",
    "method": "chacha20-ietf-poly1305",
    "local_address": "127.0.0.1",
    "local_port": 1080,
    "timeout": 300
}

INSTALL_DIR = Path.home() / ".shadowsocks"
CONFIG_FILE = INSTALL_DIR / "config.json"
SSLOCAL_BIN = INSTALL_DIR / "sslocal"

class Colors:
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"

def print_step(msg):
    print(f"[*] {msg}")

def print_success(msg):
    print(f"{Colors.OKGREEN}[✓]{Colors.ENDC} {msg}")

def print_error(msg):
    print(f"{Colors.FAIL}[✗]{Colors.ENDC} {msg}")

def download_file(url, dest):
    print_step(f"Downloading {url}")
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=30) as response:
            with open(dest, "wb") as f:
                f.write(response.read())
        print_success(f"Downloaded: {dest}")
        return True
    except Exception as e:
        print_error(f"Download failed: {e}")
        return False

def verify_sha256(file_path, expected_sha):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest() == expected_sha

def extract_tarball(tarball_path, dest_dir):
    with tarfile.open(tarball_path, "r:xz") as tar:
        tar.extractall(dest_dir)
    return True

def setup_shadowsocks():
    print("=" * 60)
    print("  E2B Shadowsocks Setup - v1.24.0")
    print("=" * 60)
    
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    
    sha_file = INSTALL_DIR / f"{TARBALL_NAME}.sha256"
    if not download_file(SHA256_URL, sha_file):
        return False
    
    with open(sha_file, "r") as f:
        expected_sha = f.read().strip().split()[0]
    
    tarball_path = INSTALL_DIR / TARBALL_NAME
    if not tarball_path.exists():
        if not download_file(TARBALL_URL, tarball_path):
            return False
    
    if not verify_sha256(tarball_path, expected_sha):
        print_error("SHA256 mismatch!")
        return False
    
    if not extract_tarball(tarball_path, INSTALL_DIR):
        return False
    
    sslocal_extracted = INSTALL_DIR / "sslocal"
    if sslocal_extracted.exists():
        os.chmod(sslocal_extracted, 0o755)
        print_success(f"sslocal ready: {sslocal_extracted}")
    else:
        print_error("sslocal not found!")
        return False
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(SERVER_CONFIG, f, indent=2)
    print_success(f"Config saved: {CONFIG_FILE}")
    
    return True

if __name__ == "__main__":
    if setup_shadowsocks():
        print("\n✅ Installation complete!")
        print(f"Run: {SSLOCAL_BIN} -c {CONFIG_FILE}")
    else:
        print("\n❌ Installation failed")
        sys.exit(1)
