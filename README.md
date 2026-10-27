# TranQuangMinh-TH1-TN-KHKT2
Tổng hợp bài Thực hành 1 môn TNKHKT2
#Bài 1: Nút nhấn khi loop() bận

- Sơ đồ đấu nối (dùng chung Bài 1 + 2): [So do noi day.png](<Bài 2/So do noi day.png>)
- Video không ngắt (polling): [Khong ngat.mp4](<Bài 1/Khong ngat.mp4>)
- Video có ngắt: [Co ngat.mp4](<Bài 1/Co ngat.mp4>)

*Nhận xét:
- Không dùng ngắt (VD1): nút chỉ được đọc một lần mỗi vòng `for`, giữa hai lần đọc có `delay(10)`. Nếu nhấn nhanh hoặc `loop()` bận lâu, lần nhấn có thể rơi vào lúc CPU đang delay và bị bỏ lỡ.
- Có ngắt (VD2): cạnh xuống được bắt ngay bằng phần cứng, cờ `buttonPressed` được đặt tức thì và `loop()` xử lý sau, nên LED nháy phản hồi mọi lần nhấn, kể cả lúc `loop()` đang bận.
- Kết luận: ngắt phù hợp cho sự kiện ngắn, không đoán trước được thời điểm.
- Hạn chế: VD2 chưa chống dội, một lần nhấn có thể sinh nhiều cạnh xuống nên LED có thể nháy nhiều lần cho một lần nhấn. Vấn đề này được xử lý ở Bài 2.

#Bài 2: Chống dội nút nhấn

- Project: [Bài 2/Bai2](<Bài 2/Bai2>)
- Biểu đồ: [10 lần nhấn](<Bài 2/Chart 10 lan nhan.png>), [40 lần nhấn](<Bài 2/Chart 40 lan nhan.png>)
- Video: [debounce 60ms.mp4](<Bài 2/debounce 60ms.mp4>)

*Ngưỡng debounce chọn: 60 ms

*Giải thích: Tiếp điểm cơ học thường dội trong vài ms đến vài chục ms, nên 60 ms đủ dài để bỏ qua các cạnh dội mà vẫn ngắn hơn khoảng cách giữa hai lần nhấn thật của người dùng.

**So sánh có và không chống dội** (đếm số cạnh xuống thô `rawEdgeCount` so với số lần nhấn đã lọc `debouncedCount`):

| Lần thử | Không chống dội (raw) | Có chống dội 60 ms | Nhận xét |
|---|---|---|---|
| 10 lần nhấn | 10 | 10 | Lần thử này không xảy ra dội |
| 40 lần nhấn | 43 | 40 | Thừa 3 cạnh do dội, bộ lọc loại bỏ hết |

*Nhận xét:
- Không chống dội, số đếm có thể lớn hơn số lần nhấn thật (43 so với 40). Mỗi lần nhấn có thể sinh thêm cạnh xuống giả.
- Có chống dội 60 ms, số đếm khớp đúng số lần nhấn thật (40 so với 40).
- Dội là hiện tượng ngẫu nhiên, nên lần thử 10 nhấn không thấy dội, còn lần 40 nhấn thì thấy. Vì vậy cần thử nhiều lần nhấn mới đánh giá được.
- Đánh đổi: ngưỡng quá lớn sẽ bỏ sót các lần nhấn thật khi nhấn rất nhanh, quá nhỏ thì không lọc hết dội. 60 ms là mức cân bằng cho thao tác nhấn bằng tay.

#Bài 3: Lọc nhiễu ADC

- Project: [Bài 3/Bai3](<Bài 3/Bai3>)
- Sơ đồ đấu nối: [sơ đồ kết nối.png](<Bài 3/sơ đồ kết nối.png>)
- So sánh thô và đã lọc: [Biểu đồ so sánh lọc và thô.png](<Bài 3/Biểu đồ so sánh lọc và thô.png>)
- Thông số: bộ lọc trung bình trượt N = 8, chu kỳ lấy mẫu 20 ms (cửa sổ khoảng 160 ms), đọc ADC ở GPIO34 (ADC1_CH6)

| Chỉ số (50 mẫu cuối) | Thô | Đã lọc |
|---|---|---|
| Độ lệch chuẩn | 5.1 | 1.6 |

**Nhận xét:**
- Độ lệch chuẩn giảm từ 5.1 xuống 1.6 (khoảng 69%), nên số liệu đã lọc ổn định hơn nhiều. Tín hiệu quanh mức 2122, nhiễu thô dao động vài đơn vị.
- Số liệu thô có các gai nhiễu đột ngột, lệch tới khoảng 2176 (+54) và 2069 (-53). Sau lọc, gai lớn nhất chỉ còn khoảng 2131 (+9), tức biên độ gai giảm mạnh.
- Gai không bị xóa hẳn mà bị "pha loãng": mỗi gai nằm trong cửa sổ 8 mẫu nên đường đã lọc có một đoạn bậc kéo dài khoảng 160 ms. Muốn loại gai triệt để hơn thì dùng lọc trung vị (median).
- Đổi lại, trung bình trượt gây trễ cỡ vài mẫu khi tín hiệu thay đổi thật. N lớn thì mượt hơn nhưng trễ hơn, N = 8 là mức cân bằng.
- **Về ADC2 và chân strapping: ADC2 của ESP32 dùng chung với một số chân strapping (GPIO0, 2, 12, 15) và còn bị WiFi chiếm khi bật WiFi, nên đọc không ổn định. Vì vậy bài này dùng ADC1 (GPIO34, chân chỉ đọc) để lấy mẫu.
