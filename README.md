# 🤖 AI Chatbot với Streamlit

Một chatbot đơn giản được xây dựng bằng Streamlit với bot giả định thông minh.

## ✨ Tính năng

- 💬 Chat interface đẹp mắt với Streamlit
- 🤖 Bot giả định thông minh với nhiều loại phản hồi
- 🎯 Nhận diện từ khóa và phản hồi phù hợp
- ⏰ Hiển thị thời gian hiện tại
- 😄 Kể chuyện cười
- 🔄 Bắt đầu cuộc trò chuyện mới

## 🚀 Cài đặt và chạy

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng
```bash
streamlit run app.py
```

### 3. Truy cập
Mở trình duyệt và truy cập: http://localhost:8501

## 🎮 Cách sử dụng

1. **Bắt đầu chat**: Click "🆕 Cuộc trò chuyện mới" trong sidebar
2. **Gửi tin nhắn**: Gõ tin nhắn và nhấn Enter
3. **Xem phản hồi**: Bot sẽ trả lời dựa trên nội dung tin nhắn của bạn

## 🤖 Tính năng Bot

Bot có thể nhận diện và phản hồi các loại tin nhắn:

- **Chào hỏi**: "xin chào", "hello", "hi"
- **Hỏi giúp đỡ**: "giúp", "help", "hỗ trợ"
- **Cảm ơn**: "cảm ơn", "thanks"
- **Hỏi tên**: "tên", "bạn tên gì"
- **Hỏi thời gian**: "thời gian", "mấy giờ"
- **Hỏi thời tiết**: "thời tiết"
- **Kể chuyện cười**: "joke", "đùa"

## 📁 Cấu trúc dự án

```
ai-chatbot/
├── app.py              # Ứng dụng chính
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

## 🔧 Tùy chỉnh

Bạn có thể dễ dàng tùy chỉnh bot bằng cách:

1. **Thêm phản hồi mới**: Chỉnh sửa `BOT_RESPONSES` trong `app.py`
2. **Thêm từ khóa mới**: Mở rộng logic trong hàm `get_bot_response()`
3. **Thay đổi giao diện**: Chỉnh sửa layout trong `main()`

## 🎯 Ví dụ sử dụng

```
User: "Xin chào"
Bot: "Xin chào! Tôi là AI Assistant, rất vui được gặp bạn! 😊"

User: "Bây giờ mấy giờ?"
Bot: "Bây giờ là 14:30:25. Thời gian bay nhanh quá! ⏰"

User: "Kể chuyện cười đi"
Bot: "Tại sao lập trình viên thích mùa đông? Vì có nhiều bug! 🐛"
```

## 📝 License

MIT License 