import requests
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Cấu hình logging
logger = logging.getLogger(__name__)

class NocoDBClient:
    def __init__(self):
        self.base_url = os.getenv("NOCODB_URL", "http://localhost:8080")
        self.api_key = os.getenv("NOCODB_API_KEY")
        self.project_id = os.getenv("NOCODB_PROJECT_ID")
        
        if not self.base_url or not self.api_key or not self.project_id:
            raise ValueError("Missing NocoDB configuration. Please set NOCODB_URL, NOCODB_API_KEY, and NOCODB_PROJECT_ID in .env file")
        
        # Sử dụng xc-token thay vì xc-auth
        self.headers = {
            "xc-token": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make HTTP request to NocoDB API"""
        # Sử dụng API v2 endpoint
        url = f"{self.base_url}/api/v2/{endpoint}"
        
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
            logger.error(f"Error making request to NocoDB: {e}")
            return None

class ChatDatabase:
    def __init__(self):
        self.client = NocoDBClient()
        # Table IDs từ NocoDB Admin
        self.conversations_table_id = "mjcgx9i3k5d0l7o"  # ID của bảng conversations
        self.messages_table_id = None  # Sẽ cần lấy từ bảng messages
    
    def create_conversation(self, conversation_id: str = None, title: str = None) -> bool:
        """Create a new conversation with optional custom ID"""
        data = {
            "title": title or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
        
        # Không gửi custom ID, để NocoDB tự tạo
        # if conversation_id:
        #     data["id"] = conversation_id
        
        endpoint = f"tables/{self.conversations_table_id}/records"
        logger.debug(f"DEBUG: create_conversation endpoint: {endpoint}")
        logger.debug(f"DEBUG: create_conversation data: {data}")
        
        result = self.client._make_request("POST", endpoint, data)
        logger.debug(f"DEBUG: create_conversation result: {result}")
        
        return result is not None
    
    def save_message(self, conversation_id: str, role: str, content: str) -> bool:
        """Save a message to the conversation"""
        # Cần lấy messages table ID trước
        if not self.messages_table_id:
            logger.error("Messages table ID not set")
            return False
            
        data = {
            "conversation_id": conversation_id,
            "role": role,
            "content": content
        }
        
        endpoint = f"tables/{self.messages_table_id}/records"
        logger.debug(f"DEBUG: save_message endpoint: {endpoint}")
        logger.debug(f"DEBUG: save_message data: {data}")
        
        result = self.client._make_request("POST", endpoint, data)
        logger.debug(f"DEBUG: save_message result: {result}")
        
        return result is not None
    
    def get_conversation_messages(self, conversation_id: str) -> List[Dict]:
        """Get all messages for a conversation"""
        if not self.messages_table_id:
            logger.error("Messages table ID not set")
            return []
            
        endpoint = f"tables/{self.messages_table_id}/records?where=(conversation_id,eq,{conversation_id})"
        result = self.client._make_request("GET", endpoint)
        logger.debug(f"DEBUG: get_conversation_messages result: {result}")
        
        if result and isinstance(result, dict) and "list" in result:
            return result["list"]
        elif result and isinstance(result, list):
            return result
        else:
            logger.debug(f"DEBUG: Unexpected result format: {type(result)}")
            return []
    
    def get_all_conversations(self) -> List[Dict]:
        """Get all conversations"""
        endpoint = f"tables/{self.conversations_table_id}/records"
        result = self.client._make_request("GET", endpoint)
        logger.debug(f"DEBUG: get_all_conversations result: {result}")
        
        if result and isinstance(result, dict) and "list" in result:
            return result["list"]
        elif result and isinstance(result, list):
            return result
        else:
            logger.debug(f"DEBUG: Unexpected result format: {type(result)}")
            return []
    
    def update_conversation_title(self, conversation_id: str, title: str) -> bool:
        """Update conversation title"""
        data = {
            "title": title
        }
        
        endpoint = f"tables/{self.conversations_table_id}/records/{conversation_id}"
        result = self.client._make_request("PUT", endpoint, data)
        return result is not None
    
    def set_messages_table_id(self, table_id: str):
        """Set the messages table ID"""
        self.messages_table_id = table_id 