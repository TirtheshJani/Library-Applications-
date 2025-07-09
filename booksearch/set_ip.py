#!/usr/bin/env python3
"""
Check your current IP address and test database connectivity
"""
import requests
import psycopg2
import socket
import sys

def get_public_ip():
    """Get your current public IP address"""
    try:
        # Try multiple services in case one is down
        services = [
            'https://api.ipify.org',
            'https://ipinfo.io/ip',
            'https://ifconfig.me/ip',
            'https://icanhazip.com'
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                ip = response.text.strip()
                print(f"✅ Your current public IP: {ip}")
                return ip
            except:
                continue
        
        print("❌ Could not determine your public IP address")
        return None
    except Exception as e:
        print(f"❌ Error getting IP: {e}")
        return None

def test_port_connectivity(host, port):
    """Test if we can connect to the host and port"""
    try:
        socket.setdefaulttimeout(10)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {port} is open on {host}")
            return True
        else:
            print(f"❌ Port {port} is closed or filtered on {host}")
            return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def test_postgres_connection():
    """Test PostgreSQL connection"""
    DB_HOST = "34.130.181.235"
    DB_PORT = 5432
    DB_NAME = "bookinfo"
    DB_USER = "booknerd"
    DB_PASSWORD = ".~h*ns%`VT#14gS9"
    
    try:
        print(f"🔍 Testing PostgreSQL connection to {DB_HOST}:{DB_PORT}...")
        
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=10
        )
        
        print("✅ PostgreSQL connection successful!")
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 DATABASE CONNECTION TROUBLESHOOTER")
    print("=" * 60)
    
    # Step 1: Get current IP
    print("\n1️⃣ CHECKING YOUR CURRENT IP ADDRESS")
    print("-" * 40)
    current_ip = get_public_ip()
    
    if current_ip:
        print(f"\n📋 IMPORTANT: Add this IP to Google Cloud authorized networks:")
        print(f"    IP Address: {current_ip}/32")
        print(f"    Format: {current_ip}/32")
    
    # Step 2: Test port connectivity
    print("\n2️⃣ TESTING NETWORK CONNECTIVITY")
    print("-" * 40)
    port_open = test_port_connectivity("34.130.181.235", 5432)
    
    # Step 3: Test PostgreSQL connection
    print("\n3️⃣ TESTING POSTGRESQL CONNECTION")
    print("-" * 40)
    db_connected = test_postgres_connection()
    
    # Step 4: Provide recommendations
    print("\n4️⃣ RECOMMENDATIONS")
    print("-" * 40)
    
    if db_connected:
        print("🎉 Everything is working! Your Flask app should connect successfully.")
    elif not port_open:
        print("❌ Network connectivity issue detected.")
        print("\n🔧 Troubleshooting steps:")
        print("   1. Add your IP to Google Cloud authorized networks:")
        if current_ip:
            print(f"      • IP: {current_ip}/32")
        print("   2. Check your firewall settings")
        print("   3. Try connecting from a different network")
        print("   4. Consider using Google Cloud SQL Proxy")
    else:
        print("❌ Port is open but PostgreSQL authentication failed.")
        print("\n🔧 Check:")
        print("   • Database credentials")
        print("   • Database is running")
        print("   • User permissions")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    if current_ip:
        print(f"1. Go to: https://console.cloud.google.com/sql/instances")
        print(f"2. Click on 'illo-0101' → Connections → Add network")
        print(f"3. Add: {current_ip}/32")
        print(f"4. Save and try again")
    print("5. If still failing, we'll set up Cloud SQL Proxy")
    print("=" * 60)

if __name__ == "__main__":
    main()