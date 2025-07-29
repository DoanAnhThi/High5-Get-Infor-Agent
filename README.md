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

### Cách 1: Chạy với Docker (Khuyến nghị)

#### 1. Cài đặt Docker và Docker Compose
Đảm bảo bạn đã cài đặt Docker và Docker Compose trên máy.

#### 2. Tạo file .env
```bash
# Tạo file .env với OpenAI API key
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

#### 3. Chạy với Docker Compose
```bash
# Build và chạy ứng dụng
docker-compose up --build

# Hoặc chạy ở background
docker-compose up -d --build
```

#### 4. Truy cập
Mở trình duyệt và truy cập: http://localhost:8501

### Cách 2: Chạy trực tiếp

#### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

#### 2. Tạo file .env
```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

#### 3. Chạy ứng dụng
```bash
streamlit run app.py
```

#### 4. Truy cập
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
├── app.py              # Ứng dụng Streamlit chính
├── openai_api.py       # Module gọi OpenAI API
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── .dockerignore       # Docker ignore file
├── static/             # Static files (images)
│   └── robot.png       # Robot image
└── README.md          # Documentation
```

## 🔧 Tùy chỉnh

Bạn có thể dễ dàng tùy chỉnh bot bằng cách:

1. **Thay đổi OpenAI model**: Chỉnh sửa tham số `model` trong `openai_api.py`
2. **Thay đổi system prompt**: Chỉnh sửa nội dung system message trong `openai_api.py`
3. **Thay đổi giao diện**: Chỉnh sửa layout trong `app.py`
4. **Thay đổi ảnh robot**: Thay thế file `static/robot.png`

## 🐳 Docker Commands

```bash
# Build image
docker build -t ai-chatbot .

# Run container
docker run -p 8501:8501 --env-file .env ai-chatbot

# Stop container
docker-compose down

# View logs
docker-compose logs -f
```

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