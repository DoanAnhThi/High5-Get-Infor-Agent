import streamlit as st
import random
from datetime import datetime
from openai_api import ask_openai

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



def start_new_conversation():
    """Bắt đầu cuộc trò chuyện mới"""
    st.session_state.messages = []
    st.session_state.conversation_started = True

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
            
            # Tạo phản hồi từ bot
            with st.spinner("Bot đang suy nghĩ..."):
                try:
                    bot_response = ask_openai(prompt)
                except Exception as e:
                    bot_response = f"Đã xảy ra lỗi khi gọi OpenAI: {e}"
            
            # Thêm phản hồi bot
            st.chat_message("assistant").markdown(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
            st.rerun()

if __name__ == "__main__":
    main() 