"""
Deploy Docker stack to DigitalOcean using paramiko
"""
import paramiko
import time
import sys

# Configuration
HOST = "165.232.174.154"
USER = "root"
PASSWORD = "837829318aA!a"

def execute_command(ssh, command, wait_for_output=True):
    """Execute a command and print output"""
    print(f"\n🔧 Executing: {command[:80]}...")
    stdin, stdout, stderr = ssh.exec_command(command)
    
    if wait_for_output:
        exit_status = stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if output:
            print(output)
        if error:
            print(f"⚠️  {error}")
        
        return exit_status == 0
    return True

def main():
    print("=" * 70)
    print("DIGITALOCEAN DOCKER DEPLOYMENT")
    print("=" * 70)
    print(f"Connecting to {HOST}...")
    
    # Connect via SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(HOST, username=USER, password=PASSWORD)
        print("✅ Connected successfully!")
        
        # Step 1: Kill blocking processes
        print("\n📦 Step 1: Stopping blocking processes...")
        execute_command(ssh, "killall unattended-upgrades apt-get 2>/dev/null || true")
        time.sleep(2)
        
        # Step 2: Configure firewall
        print("\n🔥 Step 2: Configuring firewall...")
        execute_command(ssh, "ufw --force enable")
        execute_command(ssh, "ufw allow 6333/tcp")
        execute_command(ssh, "ufw allow 6334/tcp")
        execute_command(ssh, "ufw allow 5432/tcp")
        execute_command(ssh, "ufw allow 7474/tcp")
        execute_command(ssh, "ufw allow 7687/tcp")
        execute_command(ssh, "ufw reload")
        
        # Step 3: Create directory
        print("\n📁 Step 3: Creating deployment directory...")
        execute_command(ssh, "mkdir -p /opt/rag-stack && cd /opt/rag-stack")
        
        # Step 4: Create docker-compose.yml
        print("\n📝 Step 4: Creating docker-compose.yml...")
        compose_content = """version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_storage:/qdrant/storage
    restart: unless-stopped
  postgres:
    image: postgres:16-alpine
    container_name: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=raguser
      - POSTGRES_PASSWORD=ragpass123
      - POSTGRES_DB=rag_knowledge
    restart: unless-stopped
  neo4j:
    image: neo4j:5.15-community
    container_name: neo4j
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j_data:/data
    environment:
      - NEO4J_AUTH=neo4j/ragpass123
      - NEO4J_dbms_memory_pagecache_size=512M
      - NEO4J_dbms_memory_heap_max__size=1G
    restart: unless-stopped
volumes:
  qdrant_storage:
  postgres_data:
  neo4j_data:
"""
        
        # Write compose file
        execute_command(ssh, f"cat > /opt/rag-stack/docker-compose.yml << 'EOFMARKER'\n{compose_content}\nEOFMARKER")
        
        # Step 5: Start Docker services
        print("\n🚀 Step 5: Starting Docker services...")
        execute_command(ssh, "cd /opt/rag-stack && docker compose up -d")
        
        print("\n⏳ Waiting for services to start...")
        time.sleep(15)
        
        # Step 6: Check status
        print("\n📊 Step 6: Checking service status...")
        execute_command(ssh, "cd /opt/rag-stack && docker compose ps")
        
        # Step 7: Test Qdrant
        print("\n🔍 Step 7: Testing Qdrant...")
        execute_command(ssh, "curl -s http://localhost:6333/")
        
        print("\n" + "=" * 70)
        print("🎉 DEPLOYMENT COMPLETE!")
        print("=" * 70)
        print(f"\n📋 Service URLs:")
        print(f"  Qdrant HTTP: http://{HOST}:6333")
        print(f"  Qdrant gRPC: http://{HOST}:6334")
        print(f"  PostgreSQL:  {HOST}:5432")
        print(f"  Neo4j HTTP:  http://{HOST}:7474")
        print(f"  Neo4j Bolt:  bolt://{HOST}:7687")
        print(f"\n🔐 Credentials:")
        print(f"  PostgreSQL: raguser / ragpass123")
        print(f"  Neo4j:      neo4j / ragpass123")
        print(f"\n📤 Next step: Upload embeddings")
        print(f"  python scripts/upload_to_cloud.py")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        ssh.close()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
