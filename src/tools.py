"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ và thông tin học vụ của sinh viên VinUni bằng mã sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
                }
            },
            "required": ["student_id"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string): Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')
    #    - datetime_str (string): Thời gian hẹn (ví dụ: '14:00 15/09/2026')
    #    - advisor_name (string): Tên cố vấn học tập
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn (ví dụ: '14:00 15/09/2026')"
                },
                "advisor_name": {
                    "type": "string",
                    "description": "Tên cố vấn học tập"
                }
            },
            "required": ["student_id", "datetime_str", "advisor_name"]
        }
    },
    {
        "name": "check_room_availability",
        "description": "Tra cứu các phòng họp còn trống theo thời gian, số người, tòa nhà và thiết bị yêu cầu.",
        "parameters": {
            "type": "object",
            "properties": {
                "datetime_str": {
                    "type": "string",
                    "description": "Khung thời gian họp, ví dụ '14:00 đến 15:30 ngày 20/09/2026'"
                },
                "attendee_count": {
                    "type": "integer",
                    "description": "Số người tham dự"
                },
                "building": {
                    "type": "string",
                    "description": "Tòa nhà hoặc cơ sở cần tìm phòng"
                },
                "required_equipment": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách thiết bị bắt buộc, ví dụ ['máy chiếu', 'bảng trắng']"
                }
            },
            "required": ["datetime_str", "attendee_count", "building", "required_equipment"]
        }
    },
    {
        "name": "create_room_booking",
        "description": "Đặt phòng họp đã chọn theo mã phòng, thời gian, số người, tòa nhà và thiết bị.",
        "parameters": {
            "type": "object",
            "properties": {
                "room_id": {
                    "type": "string",
                    "description": "Mã phòng được chọn từ kết quả tra cứu"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Khung thời gian họp"
                },
                "attendee_count": {
                    "type": "integer",
                    "description": "Số người tham dự"
                },
                "building": {
                    "type": "string",
                    "description": "Tòa nhà hoặc cơ sở của phòng"
                },
                "required_equipment": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách thiết bị cần sử dụng"
                }
            },
            "required": ["room_id", "datetime_str", "attendee_count", "building", "required_equipment"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    },
    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.60,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
    }
}

MOCK_ROOMS = [
    {
        "room_id": "C-A101",
        "building": "Cơ sở chính",
        "capacity": 10,
        "equipment": ["máy chiếu", "bảng trắng"]
    },
    {
        "room_id": "C-A202",
        "building": "Cơ sở chính",
        "capacity": 16,
        "equipment": ["máy chiếu", "bảng trắng", "hội nghị trực tuyến"]
    },
    {
        "room_id": "C-B301",
        "building": "Cơ sở chính",
        "capacity": 40,
        "equipment": ["máy chiếu", "hội nghị trực tuyến"]
    }
]


def execute_academic_query(student_id: str) -> str:
    """Thực thi tra cứu học vụ theo mã sinh viên"""
    student = MOCK_DATABASE.get(student_id.strip().upper())
    if student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": student_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(student_id: str, datetime_str: str, advisor_name: str = "PGS.TS Nguyễn Văn A") -> str:
    """Thực thi đặt lịch hẹn tư vấn học vụ"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{student_id}-99",
        "student_id": student_id,
        "datetime": datetime_str,
        "advisor": advisor_name,
        "message": f"Đặt lịch thành công cho sinh viên {student_id} với {advisor_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


def _has_required_equipment(room_equipment: list, required_equipment: list) -> bool:
    """Kiểm tra thiết bị yêu cầu có trong danh sách thiết bị của phòng."""
    available = {item.strip().lower() for item in room_equipment}
    return all(item.strip().lower() in available for item in required_equipment)


def execute_check_room_availability(
    datetime_str: str,
    attendee_count: int,
    building: str,
    required_equipment: list
) -> str:
    """Tra cứu phòng phù hợp theo sức chứa, tòa nhà và thiết bị."""
    rooms = [
        room for room in MOCK_ROOMS
        if room["building"].lower() == building.strip().lower()
        and room["capacity"] >= attendee_count
        and _has_required_equipment(room["equipment"], required_equipment)
    ]
    if not rooms:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": "Không tìm thấy phòng họp phù hợp với thời gian, số người, tòa nhà và thiết bị đã yêu cầu.",
            "datetime": datetime_str
        }, ensure_ascii=False)
    return json.dumps({
        "status": "SUCCESS",
        "datetime": datetime_str,
        "rooms": rooms
    }, ensure_ascii=False)


def execute_create_room_booking(
    room_id: str,
    datetime_str: str,
    attendee_count: int,
    building: str,
    required_equipment: list
) -> str:
    """Tạo booking cho phòng phù hợp đã được tra cứu."""
    room = next((item for item in MOCK_ROOMS if item["room_id"].lower() == room_id.strip().lower()), None)
    if room is None or room["building"].lower() != building.strip().lower():
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy phòng '{room_id}' tại '{building}'."
        }, ensure_ascii=False)
    if room["capacity"] < attendee_count or not _has_required_equipment(room["equipment"], required_equipment):
        return json.dumps({
            "status": "NOT_AVAILABLE",
            "message": f"Phòng {room_id} không đáp ứng đủ sức chứa hoặc thiết bị yêu cầu."
        }, ensure_ascii=False)
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"RB-{room_id}-99",
        "room_id": room_id,
        "building": building,
        "datetime": datetime_str,
        "attendee_count": attendee_count,
        "equipment": required_equipment,
        "message": f"Đặt phòng {room_id} thành công vào {datetime_str} cho {attendee_count} người."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "academic_query": execute_academic_query,
    "schedule_appointment": execute_schedule_appointment,
    "check_room_availability": execute_check_room_availability,
    "create_room_booking": execute_create_room_booking
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
