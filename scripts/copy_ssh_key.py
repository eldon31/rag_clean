#!/usr/bin/env python3
"""Copy SSH public key to DigitalOcean Droplet using paramiko"""

import os
import sys
from pathlib import Path

try:
    import paramiko
except ImportError:
    print("Installing paramiko...")
    os.system("pip install paramiko")
    import paramiko

# Configuration
DROPLET_IP = "165.232.174.154"
USER = "root"
PASSWORD = "837829318aA!a"

# SSH key path
ssh_dir = Path.home() / ".ssh"
pub_key_path = ssh_dir / "id_rsa.pub"

if not pub_key_path.exists():
    print(f"ERROR: SSH public key not found at {pub_key_path}")
    sys.exit(1)

# Read public key
with open(pub_key_path, 'r') as f:
    pub_key = f.read().strip()

print(f"Public key found. Copying to {USER}@{DROPLET_IP}...")

try:
    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Connect with password
    print("Connecting to server...")
    ssh.connect(DROPLET_IP, username=USER, password=PASSWORD, timeout=10)
    
    # Execute commands to add the key
    commands = [
        "mkdir -p ~/.ssh",
        "chmod 700 ~/.ssh",
        f"echo '{pub_key}' >> ~/.ssh/authorized_keys",
        "chmod 600 ~/.ssh/authorized_keys",
        # Remove duplicates if any
        "sort -u ~/.ssh/authorized_keys -o ~/.ssh/authorized_keys"
    ]
    
    for cmd in commands:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        exit_code = stdout.channel.recv_exit_status()
        if exit_code != 0:
            error = stderr.read().decode()
            print(f"Warning: Command '{cmd}' returned exit code {exit_code}")
            if error:
                print(f"Error output: {error}")
    
    print("\n✓ SSH key copied successfully!")
    
    # Test the connection
    print("\nTesting key-based authentication...")
    ssh.close()
    
    # Reconnect using key
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    private_key_path = ssh_dir / "id_rsa"
    key = paramiko.RSAKey.from_private_key_file(str(private_key_path))
    
    ssh.connect(DROPLET_IP, username=USER, pkey=key, timeout=10)
    stdin, stdout, stderr = ssh.exec_command("echo 'SSH key authentication working!'")
    result = stdout.read().decode().strip()
    
    print(f"✓ {result}")
    print(f"\nYou can now SSH to your Droplet without a password:")
    print(f"  ssh {USER}@{DROPLET_IP}")
    
    ssh.close()
    
except paramiko.AuthenticationException:
    print("\n✗ Authentication failed. Please check the password.")
    sys.exit(1)
except paramiko.SSHException as e:
    print(f"\n✗ SSH error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Error: {e}")
    sys.exit(1)
