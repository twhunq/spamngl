# 🚀 Marine NGL Tool

Công cụ Spam NGL hiệu quả với giao diện web đẹp mắt và dễ sử dụng.

## ⚡ Tối ưu hóa tốc độ (Speed Optimizations)

Tool đã được tối ưu hóa để đạt tốc độ spam cao nhất:

- **Timeout giảm**: Từ 15s xuống 8s
- **SSL Verification**: Tắt để tăng tốc độ kết nối
- **Connection Pooling**: Tái sử dụng connection
- **Thread Timeout**: Giảm xuống 2s
- **Request Delay**: Giảm xuống 0.05s
- **Status Updates**: Cập nhật nhanh hơn (1-1.5s)
- **Session Reuse**: Sử dụng requests.Session()
- **Batch Processing**: Xử lý theo batch để tăng hiệu suất

## ✨ Tính năng

- 🎯 **Giao diện web hiện đại**: Thiết kế đen trắng với hiệu ứng đẹp mắt
- ⚡ **Tự động dừng**: Dừng tự động khi đạt đủ số lượng tin nhắn
- 📊 **Theo dõi thời gian thực**: Hiển thị tiến độ và thống kê chi tiết
- 🎨 **Responsive design**: Tương thích với mọi thiết bị
- 🌐 **Đa luồng**: Hỗ trợ nhiều cuộc tấn công đồng thời
- 🔧 **Dễ sử dụng**: Giao diện thân thiện với người dùng

## 🛠️ Cài đặt

### Yêu cầu hệ thống
- Python 3.7+
- pip

### Bước 1: Clone repository
```bash
git clone <repository-url>
cd NGL
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy ứng dụng
```bash
python web_app.py
```

### Bước 4: Truy cập
Mở trình duyệt và truy cập: `http://localhost:5000`

## 📖 Hướng dẫn sử dụng

### 1. Cấu hình tấn công
- **Tên người dùng**: Nhập username NGL hoặc link đầy đủ
- **Số lượng tin nhắn**: Chọn số tin nhắn muốn gửi (1-500)
- **Tin nhắn**: Nhập nội dung tin nhắn (tùy chọn)
- **Emoji**: Bật/tắt emoji ngẫu nhiên

### 2. Bắt đầu tấn công
- Nhấn nút "Bắt Đầu Tấn Công"
- Hệ thống sẽ kiểm tra người dùng và bắt đầu gửi tin nhắn
- Theo dõi tiến độ trong thời gian thực

### 3. Quản lý tấn công
- **Dừng tấn công**: Nhấn nút "Dừng Tấn Công" để dừng thủ công
- **Xem thống kê**: Theo dõi tổng số cuộc tấn công và tin nhắn đã gửi
- **Thông báo**: Hệ thống sẽ thông báo khi hoàn thành

## 🏗️ Cấu trúc project

```
NGL/
├── main.py              # Core mNGL tool
├── web_app.py           # Flask web application
├── requirements.txt     # Python dependencies
├── vercel.json         # Vercel configuration
├── README.md           # Documentation
├── static/
│   ├── css/
│   │   └── style.css   # Custom styles
│   └── js/
│       └── app.js      # Frontend JavaScript
└── templates/
    └── index.html      # Main HTML template
```

## 🔧 Cấu hình

### Thay đổi port
Sửa file `web_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Thay đổi port ở đây
```

### Tùy chỉnh giao diện
- CSS: Chỉnh sửa `static/css/style.css`
- JavaScript: Chỉnh sửa `static/js/app.js`
- HTML: Chỉnh sửa `templates/index.html`

## 📊 API Endpoints

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/` | GET | Trang chủ |
| `/start` | POST | Bắt đầu tấn công |
| `/status/<id>` | GET | Lấy trạng thái tấn công |
| `/stop/<id>` | GET | Dừng tấn công |
| `/instances` | GET | Danh sách tất cả tấn công |

## 🚀 Deploy

### Vercel (Khuyến nghị)
```bash
# Cài đặt Vercel CLI
npm i -g vercel

# Login vào Vercel
vercel login

# Deploy
vercel

# Hoặc deploy production
vercel --prod
```

### Heroku
```bash
# Tạo Procfile
echo "web: python web_app.py" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
heroku create
git push heroku main
```

### VPS/Server
```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy với gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

## ⚠️ Lưu ý

- Sử dụng tool một cách có trách nhiệm
- Không spam quá nhiều để tránh bị chặn
- Tuân thủ điều khoản sử dụng của NGL
- Chỉ sử dụng cho mục đích giáo dục và thử nghiệm

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy:

1. Fork project
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

Project này được phát hành dưới MIT License.

## 📞 Liên hệ

- **Telegram**: Marine_devdev
- **Email**: hotromarineshop@gmail.comcom

---

**⚠️ Disclaimer**: Tool này chỉ dành cho mục đích giáo dục và thử nghiệm. Người dùng chịu trách nhiệm về việc sử dụng tool.
