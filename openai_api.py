import openai
import os
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Bạn cần thiết lập biến môi trường OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def ask_openai(prompt: str, conversation_history: List[Dict] = None, model="gpt-3.5-turbo"):
    """
    Gửi prompt đến OpenAI API với lịch sử cuộc trò chuyện
    
    Args:
        prompt: Tin nhắn hiện tại của user
        conversation_history: Danh sách các tin nhắn trước đó [{"role": "user", "content": "..."}, ...]
        model: Model OpenAI để sử dụng
    """
    # Tạo messages array với system message
    messages = [
        {"role": "system", "content": "Bạn là một trợ lý AI hữu ích tên Sunny. Hãy trả lời bằng tiếng Việt."}
    ]
    
    # Thêm lịch sử cuộc trò chuyện nếu có
    if conversation_history:
        messages.extend(conversation_history)
    
    # Thêm tin nhắn hiện tại
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip() 