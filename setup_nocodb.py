#!/usr/bin/env python3
"""
Script to setup NocoDB tables for the chatbot
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def setup_nocodb_tables():
    """Setup required tables in NocoDB"""
    
    base_url = os.getenv("NOCODB_URL", "http://localhost:8080")
    api_key = os.getenv("NOCODB_API_KEY")
    project_id = os.getenv("NOCODB_PROJECT_ID")
    
    if not all([base_url, api_key, project_id]):
        print("❌ Missing NocoDB configuration. Please set NOCODB_URL, NOCODB_API_KEY, and NOCODB_PROJECT_ID in .env file")
        return False
    
    headers = {
        "xc-auth": api_key,
        "Content-Type": "application/json"
    }
    
    # Table configurations
    tables_config = {
        "conversations": {
            "table_name": "conversations",
            "columns": [
                {"column_name": "title", "dt": "varchar", "max_length": 255},
                {"column_name": "created_at", "dt": "datetime"},
                {"column_name": "updated_at", "dt": "datetime"}
            ]
        },
        "messages": {
            "table_name": "messages", 
            "columns": [
                {"column_name": "conversation_id", "dt": "varchar", "max_length": 255},
                {"column_name": "role", "dt": "varchar", "max_length": 50},
                {"column_name": "content", "dt": "text"},
                {"column_name": "timestamp", "dt": "datetime"}
            ]
        }
    }
    
    try:
        for table_name, config in tables_config.items():
            print(f"🔧 Setting up table: {table_name}")
            
            # Create table
            table_data = {
                "table_name": config["table_name"],
                "columns": config["columns"]
            }
            
            url = f"{base_url}/api/v1/{project_id}/tables"
            response = requests.post(url, headers=headers, json=table_data)
            
            if response.status_code == 200:
                print(f"✅ Table '{table_name}' created successfully")
            elif response.status_code == 400 and "already exists" in response.text.lower():
                print(f"ℹ️  Table '{table_name}' already exists")
            else:
                print(f"❌ Failed to create table '{table_name}': {response.text}")
                
    except Exception as e:
        print(f"❌ Error setting up tables: {e}")
        return False
    
    print("🎉 NocoDB setup completed!")
    return True

if __name__ == "__main__":
    setup_nocodb_tables() 