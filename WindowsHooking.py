#!/usr/bin/env python
# -*- coding: utf-8 -*-
import keyboard
from Logic_KiemThu import process_key # Đảm bảo file này tồn tại và không có lỗi import
import time
import sys
import ctypes # Để kiểm tra admin

buffer = ""
current_output = ""
is_synthesizing = False

def flush_buffer():
    global buffer, current_output
    # print("DEBUG flush_buffer: Called.") # Thêm nếu cần debug cả hàm này
    buffer = ""
    current_output = ""

def update_output(new_text):
    global current_output, is_synthesizing
    # --- DEBUG: Theo dõi đầu vào và trạng thái ---
    print(f"DEBUG update_output: Called with new_text='{new_text}'. current_output='{current_output}'")
    if new_text == current_output:
        print("DEBUG update_output: Skipping (new_text == current_output).")
        return

    print("DEBUG update_output: Setting is_synthesizing = True")
    is_synthesizing = True
    try:
        if current_output:
            num_backspaces = len(current_output)
            # --- DEBUG: Theo dõi backspace ---
            print(f"DEBUG update_output: Sending {num_backspaces} backspaces to delete '{current_output}'.")
            for _ in range(num_backspaces):
                keyboard.send('backspace')
                # time.sleep(0.005)

        if new_text:
            # --- DEBUG: Theo dõi việc viết text mới ---
            print(f"DEBUG update_output: Writing '{new_text}'.")
            keyboard.write(new_text)
            # time.sleep(0.005)

        # --- DEBUG: Theo dõi cập nhật trạng thái ---
        print(f"DEBUG update_output: Updating current_output to '{new_text}'.")
        current_output = new_text
    except Exception as e:
         # --- DEBUG: Bắt lỗi nếu có trong quá trình mô phỏng ---
         print(f"!!!!!!!! ERROR inside update_output: {e}")
    finally:
        print("DEBUG update_output: Setting is_synthesizing = False")
        is_synthesizing = False

def on_key_event(event):
    global buffer, current_output, is_synthesizing

    if is_synthesizing:
        # --- DEBUG: Xem event nào xảy ra trong lúc đang mô phỏng ---
        print(f"DEBUG: Event during synthesis: {event.name}, type: {event.event_type}. ALLOWING.")
        return True

    if event.event_type != 'down':
        return True

    key = event.name
    # print(f"DEBUG: Hook Received Key Down: '{key}', Buffer: '{buffer}'") # Bớt debug nếu quá nhiều

    if len(key) == 1 and key.isalpha():
        # --- DEBUG: Kiểm tra kết quả từ process_key ---
        print(f"DEBUG: Calling process_key('{key}', '{buffer}')")
        new_buffer = process_key(key, buffer)
        print(f"DEBUG: process_key returned: '{new_buffer}'") # !!! QUAN TRỌNG !!!

        if new_buffer != buffer:
            # --- DEBUG: Kiểm tra xem nhánh này có được thực thi không ---
            print(f"DEBUG: Buffer CHANGED! -> Calling update_output('{new_buffer}')")
            buffer = new_buffer
            update_output(buffer)
            return # Chặn phím gốc
        else:
            # print(f"DEBUG: Buffer unchanged. Allowing '{key}'.") # Bớt debug
            if buffer:
                flush_buffer()
            return True # Cho phép phím gốc

    if key == 'backspace':
        if buffer:
            print("DEBUG: Processing backspace internally.") # DEBUG
            buffer = buffer[:-1]
            update_output(buffer)
            return # Chặn phím gốc
        else:
            print("DEBUG: Allowing native backspace (buffer empty).") # DEBUG
            return True

    if key in ['space', 'enter', 'tab']:
        if buffer:
            print(f"DEBUG: Terminator '{key}' detected, flushing buffer.") # DEBUG
            flush_buffer()
        # else:
            # print(f"DEBUG: Terminator '{key}' detected (buffer empty).") # DEBUG
        return True # Luôn cho phép terminator gốc

    # Xử lý các phím khác
    if buffer:
         print(f"DEBUG: Other key '{key}' detected, flushing buffer.") # DEBUG
         flush_buffer()
    return True # Luôn cho phép các phím khác

# --- Kiểm tra quyền Admin ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("LỖI: Vui lòng chạy script với quyền Administrator!")
    input("Nhấn Enter để thoát...")
    sys.exit()

# --- Đăng ký Hook ---
try:
    print("Đang đăng ký hook bàn phím với suppress=True...")
    keyboard.hook(on_key_event, suppress=True)
    print("Đăng ký hook thành công.")
    print("Bộ gõ tiếng Việt Global Hook đang chạy...")
    print("Nhấn ESC để thoát.")
    keyboard.wait('esc')
except Exception as e:
    print(f"\nLỖI KHÔNG MONG MUỐN KHI HOOK: {e}")
    input("Nhấn Enter để thoát...")
finally:
    print("\nĐã thoát hook.")
