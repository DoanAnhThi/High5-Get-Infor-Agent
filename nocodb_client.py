import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class NocoDBClient:
    def __init__(self):
        self.base_url = os.getenv("NOCODB_URL", "http://localhost:8080")
        self.api_key = os.getenv("NOCODB_API_KEY")
        self.project_id = os.getenv("NOCODB_PROJECT_ID")
        
        if not self.base_url or not self.api_key or not self.project_id:
            raise ValueError("Missing NocoDB configuration. Please set NOCODB_URL, NOCODB_API_KEY, and NOCODB_PROJECT_ID in .env file")
        
        self.headers = {
            "xc-auth": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make HTTP request to NocoDB API"""
        url = f"{self.base_url}/api/v1/{self.project_id}/{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to NocoDB: {e}")
            return None

class ChatDatabase:
    def __init__(self):
        self.client = NocoDBClient()
    
    def create_conversation(self, title: str = None) -> Optional[str]:
        """Create a new conversation"""
        data = {
            "title": title or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        result = self.client._make_request("POST", "conversations", data)
        if result and "Id" in result:
            return result["Id"]
        return None
    
    def save_message(self, conversation_id: str, role: str, content: str) -> bool:
        """Save a message to the conversation"""
        data = {
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        result = self.client._make_request("POST", "messages", data)
        return result is not None
    
    def get_conversation_messages(self, conversation_id: str) -> List[Dict]:
        """Get all messages for a conversation"""
        result = self.client._make_request("GET", f"messages?where=(conversation_id,eq,{conversation_id})")
        if result and "list" in result:
            return result["list"]
        return []
    
    def get_all_conversations(self) -> List[Dict]:
        """Get all conversations"""
        result = self.client._make_request("GET", "conversations")
        if result and "list" in result:
            return result["list"]
        return []
    
    def update_conversation_title(self, conversation_id: str, title: str) -> bool:
        """Update conversation title"""
        data = {
            "title": title,
            "updated_at": datetime.now().isoformat()
        }
        
        result = self.client._make_request("PUT", f"conversations/{conversation_id}", data)
        return result is not None 