#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: global_vietnamese_hook.py

Mục đích:
  - Hook toàn cục bàn phím trên Windows dùng Python để chuyển ký tự nhập theo kiểu Telex thành tiếng Việt Unicode,
    dựa trên logic chuyển đổi có trong Logic_Kiemthu.py.
  - Chỉ chặn (suppress) những phím chữ dùng để soạn Telex, trong khi các phím chức năng như space, enter, backspace, tab, …  
    vẫn được chuyển tới ứng dụng.
  
Lưu ý: Chạy file này với quyền Administrator.
"""

import keyboard
from Logic_Kiemthu import process_key

buffer = ""
current_output = ""
# Flag để đánh dấu khi đang gửi sự kiện từ script (để bỏ qua xử lý của hook)
is_synthesizing = False

def flush_buffer():
    global buffer, current_output
    buffer = ""
    current_output = ""

def update_output(new_text):
    global current_output, is_synthesizing
    if new_text == current_output:
        return
    # Xóa text hiện tại (chỉ xoá nếu có)
    if current_output:
        is_synthesizing = True
        # Gửi đủ backspace để xoá toàn bộ text hiện tại
        for _ in range(len(current_output)):
            keyboard.send('backspace')
        is_synthesizing = False
    # Viết text mới
    is_synthesizing = True
    keyboard.write(new_text)
    is_synthesizing = False
    current_output = new_text

def on_key_event(event):
    global buffer, is_synthesizing

    # Bỏ qua các sự kiện do script tự gửi ra
    if is_synthesizing:
        return True

    # Chỉ xử lý key down
    if event.event_type != 'down':
        return

    key = event.name

    # Nếu là phím chữ (dựa vào isalpha) và chỉ một ký tự
    if len(key) == 1 and key.isprintable() and key.isalpha():
        new_buffer = process_key(key, buffer)
        if new_buffer != buffer:
            buffer = new_buffer
            update_output(buffer)
        else:
            flush_buffer()
            is_synthesizing = True
            keyboard.write(key)
            is_synthesizing = False
        # Trả về False để chặn event gốc đi tới ứng dụng
        return False

    # Xử lý các phím chức năng
    if key == 'backspace':
        if buffer:
            buffer = buffer[:-1]
            update_output(buffer)
            return False  # Chặn event gốc
        else:
            return True
    elif key in ['space', 'enter', 'tab']:
        if buffer:
            flush_buffer()
            is_synthesizing = True
            keyboard.send(key)
            is_synthesizing = False
            return False
        else:
            return True
    else:
        if buffer:
            flush_buffer()
        return True

keyboard.hook(on_key_event, suppress=False)
print("Global Vietnamese Input Method đang chạy... (nhấn ESC để thoát)")
keyboard.wait('esc')
