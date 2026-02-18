"""E2B Shadowsocks - Complete Example"""

from e2b import Sandbox
import time

def setup_e2b_with_internet():
    print("🚀 Creating E2B sandbox...")
    sandbox = Sandbox()
    
    print("📦 Uploading installer...")
    setup_script = open("e2b_shadowsocks_setup.py").read()
    sandbox.files.write("/home/user/setup.py", setup_script)
    
    print("📦 Uploading helper...")
    helper_script = open("shadowsocks_helper.py").read()
    sandbox.files.write("/home/user/shadowsocks_helper.py", helper_script)
    
    print("⚙️  Installing Shadowsocks...")
    result = sandbox.process.start_and_wait("python /home/user/setup.py", timeout=60)
    
    if result.exit_code != 0:
        print(f"❌ Installation failed: {result.stderr}")
        return None
    
    print("✅ Shadowsocks installed!")
    
    print("🌐 Starting proxy...")
    sandbox.process.start(
        "bash",
        ["-c", "cd /home/user && python -c \"from shadowsocks_helper import quick_start; quick_start()\" &"]
    )
    
    time.sleep(3)
    
    print("🧪 Testing internet...")
    test_code = """
import httpx
client = httpx.Client(proxy='socks5://127.0.0.1:1080', timeout=10)
resp = client.get('https://api.ipify.org?format=json')
print(f"✅ IP: {resp.json()['origin']}")
"""
    
    result = sandbox.process.start_and_wait(f"python -c \"{test_code}\"")
    print(result.stdout)
    
    return sandbox

if __name__ == "__main__":
    setup_e2b_with_internet()
