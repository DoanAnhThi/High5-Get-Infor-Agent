import streamlit as st
import random
import uuid
import logging
from datetime import datetime
from openai_api import ask_openai
from nocodb_client import ChatDatabase

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        # Set messages table ID
        st.session_state.db.set_messages_table_id("mds17rprnz5bzj5")
    except Exception as e:
        st.error(f"Không thể kết nối đến NocoDB: {e}")
        st.session_state.db = None

def generate_conversation_id():
    """Tạo ID duy nhất cho cuộc trò chuyện"""
    return str(uuid.uuid4())

def start_new_conversation():
    """Bắt đầu cuộc trò chuyện mới"""
    st.session_state.messages = []
    st.session_state.conversation_started = True
    
    # Tạo conversation ID mới
    conversation_id = generate_conversation_id()
    st.session_state.current_conversation_id = conversation_id
    
    logger.debug(f"DEBUG: Creating new conversation with ID: {conversation_id}")
    
    # Tạo conversation mới trong database
    if st.session_state.db:
        try:
            success = st.session_state.db.create_conversation(conversation_id)
            if success:
                logger.debug(f"DEBUG: Conversation created successfully")
                st.success(f"✅ Cuộc trò chuyện mới đã được tạo! ID: {conversation_id[:8]}...")
            else:
                logger.debug(f"DEBUG: Failed to create conversation")
                st.error("❌ Không thể tạo cuộc trò chuyện mới")
        except Exception as e:
            logger.debug(f"DEBUG: Error creating conversation: {e}")
            st.error(f"Lỗi khi tạo cuộc trò chuyện mới: {e}")

def create_conversation_and_get_id():
    """Tạo conversation mới và trả về ID từ NocoDB"""
    if st.session_state.db:
        try:
            # Tạo conversation không có custom ID
            result = st.session_state.db.create_conversation()
            if result:
                # Lấy conversation mới nhất
                conversations = st.session_state.db.get_all_conversations()
                if conversations:
                    latest_conv = conversations[-1]
                    return latest_conv.get('Id')
            return None
        except Exception as e:
            logger.debug(f"DEBUG: Error creating conversation: {e}")
            return None
    return None

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
            st.success(f"✅ Cuộc trò chuyện đã được tải! ID: {conversation_id[:8]}...")
        except Exception as e:
            st.error(f"Lỗi khi tải cuộc trò chuyện: {e}")

def save_message_to_db(role: str, content: str):
    """Lưu tin nhắn vào database"""
    if st.session_state.db and st.session_state.current_conversation_id:
        try:
            logger.debug(f"DEBUG: Saving message - role: {role}, content: {content[:50]}..., conversation_id: {st.session_state.current_conversation_id}")
            success = st.session_state.db.save_message(
                st.session_state.current_conversation_id, 
                role, 
                content
            )
            if success:
                logger.debug(f"DEBUG: Message saved successfully")
            else:
                logger.debug(f"DEBUG: Failed to save message")
        except Exception as e:
            logger.debug(f"DEBUG: Error saving message: {e}")
            st.error(f"Lỗi khi lưu tin nhắn: {e}")

def main():
    # Header
    st.image("./static/robot.png", width=80)
    st.title("Sunny")
    st.markdown("---")
    
    # Hiển thị conversation ID hiện tại
    if st.session_state.current_conversation_id:
        st.info(f"🆔 Conversation ID: {st.session_state.current_conversation_id[:8]}...")
    
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
                        conv_id = conv.get('Id', conv.get('id', 'Unknown'))
                        # Chuyển conv_id thành string trước khi slice
                        conv_id_str = str(conv_id)
                        title = conv.get('title', f'Conversation {conv_id_str[:8]}...')
                        if st.button(f"💬 {title}", key=f"conv_{conv_id_str}"):
                            load_conversation(conv_id_str)
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
            # Tự động tạo conversation mới nếu chưa có
            if not st.session_state.current_conversation_id:
                logger.debug("DEBUG: No conversation ID, creating new conversation")
                conversation_id = create_conversation_and_get_id()
                if conversation_id:
                    st.session_state.current_conversation_id = str(conversation_id)
                    logger.debug(f"DEBUG: Created conversation with ID: {conversation_id}")
                else:
                    logger.debug("DEBUG: Failed to create conversation")
            
            # Thêm tin nhắn user
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Lưu tin nhắn user vào database
            save_message_to_db("user", prompt)
            
            # Tạo phản hồi từ bot với lịch sử cuộc trò chuyện
            with st.spinner("Bot đang suy nghĩ..."):
                try:
                    # Gửi lịch sử cuộc trò chuyện (trừ tin nhắn user vừa thêm)
                    conversation_history = st.session_state.messages[:-1]  # Loại bỏ tin nhắn user vừa thêm
                    bot_response = ask_openai(prompt, conversation_history)
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