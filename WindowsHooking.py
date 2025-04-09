# -*- coding: utf-8 -*-
"""
File: vietnamese_input_hook.py
Chứa phần hook toàn cục bàn phím sử dụng thư viện keyboard và tích hợp logic bộ gõ từ file vietnamese_input_logic.
"""

import keyboard
import Logic_KiemThu

# Global buffer chứa phần soạn thảo hiện thời.
buffer = ""

def flush_buffer():
    """
    Khi hoàn thành một syllable (ví dụ: nhấn Space hoặc Enter), gửi nội dung buffer ra
    ứng dụng hiện thời và reset buffer.
    """
    global buffer
    if buffer:
        keyboard.write(buffer)
        buffer = ""

def on_key_event(event):
    """
    Callback cho hook toàn cục.
    - Với các phím 'space' hoặc 'enter', commit buffer và reset.
    - Với phím Backspace, xóa ký tự cuối trong buffer.
    - Còn lại, nếu là ký tự đơn (length == 1), xử lý qua process_key của logic bộ gõ.
    """
    global buffer
    if event.event_type != "down":
        return

    if event.name in ['space', 'enter']:
        flush_buffer()
        # Gửi phím commit (Space hay Enter) sang ứng dụng hiện thời.
        keyboard.write(" " if event.name == "space" else "\n")
    else:
        # Xử lý các phím có độ dài 1 (đại diện cho ký tự)
        if len(event.name) == 1:
            buffer = Logic_KiemThu.process_key(event.name, buffer)
            print("Đang soạn:", buffer)
        else:
            # Xử lý Backspace: xóa ký tự cuối trong buffer.
            if event.name == "backspace":
                buffer = buffer[:-1] if buffer else buffer
            else:
                # Với các phím khác, chuyển tiếp sang ứng dụng hiện thời.
                keyboard.write(event.name)

if __name__ == "__main__":
    # Đăng ký hook toàn cục với suppress=True để chặn phím gốc không được gửi sang ứng dụng khác.
    keyboard.hook(on_key_event, suppress=True)
    print("Bộ gõ đang chạy. Nhấn ESC để thoát.")
    keyboard.wait("esc")