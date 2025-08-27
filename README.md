# Marine NGL Tool

Công cụ spam NGL hiệu quả với giao diện web đẹp mắt và dễ sử dụng.

## Tính năng

- 🚀 Giao diện web hiện đại và thân thiện
- 📱 Responsive design - hoạt động tốt trên mobile
- ⚡ Tốc độ gửi tin nhắn nhanh
- 🎨 Giao diện đen trắng đẹp mắt
- 🌐 Hỗ trợ tiếng Việt
- 📊 Theo dõi tiến độ real-time
- 🛑 Dừng tấn công bất cứ lúc nào
- 🎭 Hỗ trợ emoji ngẫu nhiên
- 🔄 Tự động dừng khi hoàn thành

## Cài đặt

1. **Clone repository:**
```bash
git clone <repository-url>
cd NGL
```

2. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

3. **Chạy ứng dụng:**
```bash
python web_app.py
```

4. **Mở trình duyệt:**
```
http://localhost:5000
```

## Sử dụng

1. **Nhập username NGL** - Có thể nhập username hoặc link NGL
2. **Chọn số lượng tin nhắn** - Từ 1-500 tin nhắn
3. **Nhập nội dung tin nhắn** - Để trống sẽ sử dụng "Marine"
4. **Bật/tắt emoji** - Thêm emoji ngẫu nhiên vào tin nhắn
5. **Bắt đầu tấn công** - Nhấn nút "Bắt Đầu Tấn Công"

## Tính năng nâng cao

### Theo dõi tiến độ
- Xem số tin nhắn đã gửi real-time
- Theo dõi trạng thái từng cuộc tấn công
- Thống kê tổng quan

### Điều khiển
- Dừng tấn công bất cứ lúc nào
- Xóa các cuộc tấn công đã hoàn thành
- Làm mới dữ liệu

### Tối ưu hóa
- Tự động dừng khi đạt số lượng mục tiêu
- Xử lý lỗi thông minh
- Cache busting để tránh dữ liệu cũ

## Cấu trúc dự án

```
NGL/
├── main.py              # Core NGL tool
├── web_app.py           # Flask web application
├── requirements.txt     # Python dependencies
├── README.md           # Documentation
├── templates/
│   └── index.html      # Main HTML template
└── static/
    ├── css/
    │   └── style.css   # Custom styles
    └── js/
        └── app.js      # Frontend JavaScript
```

## Dependencies

- **Flask** - Web framework
- **requests** - HTTP requests
- **colorama** - Terminal colors
- **pystyle** - Styling utilities
- **tqdm** - Progress bars

## Lưu ý

- Tool chỉ dành cho mục đích giáo dục và thử nghiệm
- Sử dụng có trách nhiệm và tuân thủ ToS của NGL
- Không lạm dụng để spam quá mức

## Hỗ trợ

Nếu gặp vấn đề, hãy:
1. Kiểm tra console để xem lỗi
2. Đảm bảo đã cài đặt đúng dependencies
3. Kiểm tra kết nối internet
4. Thử reload trang

## License

MIT License - Sử dụng tự do cho mục đích giáo dục.
