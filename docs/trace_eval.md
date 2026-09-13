# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Dương Đức Vương  
> **Mã Sinh Viên / Mã Học viên:** 2A202602944  
> **Chủ đề Lựa chọn:** Trợ lý Đặt Phòng họp & Thiết bị (Facilities Agent)

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Agent cần xác định thời gian, số người, phòng phù hợp, thiết bị cần dùng và kiểm tra xung đột lịch trước khi đặt. |
| **2. Tool Interaction** | 5 / 5 | Agent cần gọi MCP Server để tra cứu phòng trống, thiết bị và thực hiện tạo booking. |
| **3. Dynamic Decision** | 5 / 5 | Quyết định đặt phòng hay đề xuất khung giờ/phòng khác phụ thuộc vào kết quả tra cứu và tình trạng thiết bị. |
| **4. Long Horizon Goal** | 3 / 5 | Agent cần duy trì mục tiêu đặt phòng qua nhiều lượt hỏi đáp, nhưng quy trình thường hoàn tất trong một phiên ngắn. |
| **TỔNG ĐIỂM AGENTIC FIT** | **17 / 20** | *Với tổng điểm 17/20, bài toán rất phù hợp để triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (LẦN CHẠY GẦN NHẤT)

> **Nguồn dữ liệu:** Đoạn log dưới đây được trích từ `docs/trace_waterfall.json` sau khi chạy đủ 5 test case bằng OpenAI/OpenRouter.

### Trace TC03: Tra cứu và đặt phòng họp

Agent gọi `check_room_availability`, chọn phòng `C-A101`, sau đó gọi `create_room_booking` để xác nhận đặt phòng.

```json
{
  "step": 1,
  "query": "Đặt phòng họp cho 8 người vào lúc 14:00 đến 15:30 ngày 20/09/2026 tại tòa nhà Cơ sở chính. Phòng cần có máy chiếu và bảng trắng.",
  "action_type": "TOOL_EXECUTION",
  "tool_name": "check_room_availability",
  "arguments": {
    "datetime_str": "14:00 đến 15:30 ngày 20/09/2026",
    "attendee_count": 8,
    "building": "Cơ sở chính",
    "required_equipment": ["máy chiếu", "bảng trắng"]
  },
  "observation": {
    "status": "SUCCESS",
    "datetime": "14:00 đến 15:30 ngày 20/09/2026",
    "rooms": [
      {"room_id": "C-A101", "building": "Cơ sở chính", "capacity": 10, "equipment": ["máy chiếu", "bảng trắng"]},
      {"room_id": "C-A202", "building": "Cơ sở chính", "capacity": 16, "equipment": ["máy chiếu", "bảng trắng", "hội nghị trực tuyến"]}
    ]
  },
  "latency_ms": 2208.94
}
```

Kết quả đặt phòng TC03:

```json
{
  "step": 2,
  "action_type": "TOOL_EXECUTION",
  "tool_name": "create_room_booking",
  "arguments": {
    "room_id": "C-A101",
    "datetime_str": "14:00 đến 15:30 ngày 20/09/2026",
    "attendee_count": 8,
    "building": "Cơ sở chính",
    "required_equipment": ["máy chiếu", "bảng trắng"]
  },
  "observation": {
    "status": "SUCCESS",
    "booking_id": "RB-C-A101-99",
    "room_id": "C-A101",
    "message": "Đặt phòng C-A101 thành công vào 14:00 đến 15:30 ngày 20/09/2026 cho 8 người."
  }
}
```

TC04 cũng hoàn tất chuỗi tương tự và đặt thành công phòng `C-A202` cho 12 người.

### Trace TC05: Không tìm thấy phòng phù hợp

Với yêu cầu 50 người, Tool trả về `NOT_FOUND`; Agent phản hồi đúng và không bịa tên phòng.

```json
{
  "step": 1,
  "query": "Hãy tìm và đặt một phòng họp cho 50 người vào lúc 18:00 đến 20:00 ngày 25/09/2026 tại tòa nhà Cơ sở chính, có máy chiếu và hệ thống hội nghị trực tuyến.",
  "action_type": "TOOL_EXECUTION",
  "tool_name": "check_room_availability",
  "arguments": {
    "datetime_str": "18:00 đến 20:00 ngày 25/09/2026",
    "attendee_count": 50,
    "building": "Cơ sở chính",
    "required_equipment": ["máy chiếu", "hệ thống hội nghị trực tuyến"]
  },
  "observation": {
    "status": "NOT_FOUND",
    "message": "Không tìm thấy phòng họp phù hợp với thời gian, số người, tòa nhà và thiết bị đã yêu cầu."
  }
}
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã xác nhận LLM OpenAI/OpenRouter phản hồi thành công; API key và `LLM_PROVIDER=openai` đã được cấu hình trong `.env`.
- **Tổng số Test Cases đã thực thi:** **5 / 5 test cases**.
- **Tổng số Test Cases đạt đúng kỳ vọng:** **5 / 5 test cases**.
- **Số lượt gọi Tool qua MCP Server:** **6 lượt** (`academic_query`, `check_room_availability` và `create_room_booking`).
- **Ghi chú nghiệm thu:** TC01 trả lời trực tiếp; TC02 tra cứu học vụ thành công; TC03 và TC04 thực hiện đầy đủ chuỗi tra cứu rồi đặt phòng; TC05 xử lý đúng trường hợp không tìm thấy phòng và không bịa đặt dữ liệu.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
