"""E2B Shadowsocks Helper Module"""

import os
import subprocess
import time
from pathlib import Path

class ShadowsocksProxy:
    def __init__(self, install_dir=None):
        self.install_dir = install_dir or Path.home() / ".shadowsocks"
        self.sslocal_bin = self.install_dir / "sslocal"
        self.config_file = self.install_dir / "config.json"
        self.proc = None
        self.proxy_url = "socks5://127.0.0.1:1080"
    
    def start(self, wait_seconds=2):
        if not self.sslocal_bin.exists():
            raise RuntimeError("Shadowsocks not installed!")
        
        self.proc = subprocess.Popen(
            [str(self.sslocal_bin), "-c", str(self.config_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        print(f"✅ sslocal started (PID: {self.proc.pid})")
        time.sleep(wait_seconds)
        return True
    
    def stop(self):
        if self.proc:
            self.proc.terminate()
            self.proc.wait(timeout=5)
            print("🛑 sslocal stopped")
    
    def get_httpx_client(self, **kwargs):
        import httpx
        return httpx.Client(proxy=self.proxy_url, **kwargs)
    
    def test_connection(self):
        try:
            client = self.get_httpx_client(timeout=10)
            resp = client.get("https://api.ipify.org?format=json")
            data = resp.json()
            print(f"✅ Internet works! IP: {data['ip']}")
            client.close()
            return True
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

def quick_start():
    proxy = ShadowsocksProxy()
    proxy.start()
    proxy.test_connection()
    return proxy
