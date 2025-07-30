import streamlit as st
import random
from datetime import datetime
from openai_api import ask_openai
from nocodb_client import ChatDatabase

# Cấu hình trang
st.set_page_config(
    page_title="Sunny",
    page_icon="./static/robot.png",
    layout="wide"
)

# Khởi tạo session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = True  # Luôn bắt đầu là True
if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None
if "db" not in st.session_state:
    try:
        st.session_state.db = ChatDatabase()
    except Exception as e:
        st.error(f"Không thể kết nối đến NocoDB: {e}")
        st.session_state.db = None



def start_new_conversation():
    """Bắt đầu cuộc trò chuyện mới"""
    st.session_state.messages = []
    st.session_state.conversation_started = True
    st.session_state.current_conversation_id = None
    
    # Tạo conversation mới trong database
    if st.session_state.db:
        try:
            conversation_id = st.session_state.db.create_conversation()
            if conversation_id:
                st.session_state.current_conversation_id = conversation_id
                st.success("✅ Cuộc trò chuyện mới đã được tạo!")
        except Exception as e:
            st.error(f"Lỗi khi tạo cuộc trò chuyện mới: {e}")

def load_conversation(conversation_id: str):
    """Load một cuộc trò chuyện từ database"""
    if st.session_state.db:
        try:
            messages = st.session_state.db.get_conversation_messages(conversation_id)
            st.session_state.messages = [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in messages
            ]
            st.session_state.current_conversation_id = conversation_id
            st.session_state.conversation_started = True
            st.success("✅ Cuộc trò chuyện đã được tải!")
        except Exception as e:
            st.error(f"Lỗi khi tải cuộc trò chuyện: {e}")

def save_message_to_db(role: str, content: str):
    """Lưu tin nhắn vào database"""
    if st.session_state.db and st.session_state.current_conversation_id:
        try:
            st.session_state.db.save_message(
                st.session_state.current_conversation_id, 
                role, 
                content
            )
        except Exception as e:
            st.error(f"Lỗi khi lưu tin nhắn: {e}")

def main():
    # Header
    st.image("./static/robot.png", width=80)
    st.title("Sunny")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Điều khiển")
        
        if st.button("🆕 Cuộc trò chuyện mới"):
            start_new_conversation()
            st.rerun()
        
        # Hiển thị danh sách cuộc trò chuyện
        if st.session_state.db:
            st.markdown("---")
            st.subheader("📚 Lịch sử trò chuyện")
            
            try:
                conversations = st.session_state.db.get_all_conversations()
                if conversations:
                    for conv in conversations:
                        if st.button(f"💬 {conv.get('title', 'Untitled')}", key=f"conv_{conv['Id']}"):
                            load_conversation(conv['Id'])
                            st.rerun()
                else:
                    st.info("Chưa có cuộc trò chuyện nào")
            except Exception as e:
                st.error(f"Lỗi khi tải danh sách cuộc trò chuyện: {e}")
        
        st.markdown("---")

    
    # Main chat area
    if not st.session_state.conversation_started:
        st.info("👈 Click 'Cuộc trò chuyện mới' trong sidebar để bắt đầu chat!")
    else:
        # Hiển thị tin nhắn
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Nhập tin nhắn của bạn..."):
            # Thêm tin nhắn user
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Lưu tin nhắn user vào database
            save_message_to_db("user", prompt)
            
            # Tạo phản hồi từ bot
            with st.spinner("Bot đang suy nghĩ..."):
                try:
                    bot_response = ask_openai(prompt)
                except Exception as e:
                    bot_response = f"Đã xảy ra lỗi khi gọi OpenAI: {e}"
            
            # Thêm phản hồi bot
            st.chat_message("assistant").markdown(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
            # Lưu tin nhắn bot vào database
            save_message_to_db("assistant", bot_response)
            
            st.rerun()

if __name__ == "__main__":
    main() 