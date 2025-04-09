# -*- coding: utf-8 -*-
"""
File: vietnamese_input_logic.py
Chứa toàn bộ logic chuyển đổi của bộ gõ tiếng Việt cũng như một số test đơn giản.
"""

# Bản đồ chuyển đổi tổ hợp hai ký tự Telex thành nguyên âm kép.
double_map = {
    "aa": "â",
    "aw": "ă",
    "dd": "đ",
    "ee": "ê",
    "oo": "ô",
    "ow": "ơ",
    "uw": "ư"
}

# Bản đồ chuyển dấu cho các nguyên âm.
accent_map = {
    "a":  {'s': "á", 'f': "à", 'r': "ả", 'x': "ã", 'j': "ạ"},
    "ă": {'s': "ắ", 'f': "ằ", 'r': "ẳ", 'x': "ẵ", 'j': "ặ"},
    "â": {'s': "ấ", 'f': "ầ", 'r': "ẩ", 'x': "ẫ", 'j': "ậ"},
    "e":  {'s': "é", 'f': "è", 'r': "ẻ", 'x': "ẽ", 'j': "ẹ"},
    "ê": {'s': "ế", 'f': "ề", 'r': "ể", 'x': "ễ", 'j': "ệ"},
    "i":  {'s': "í", 'f': "ì", 'r': "ỉ", 'x': "ĩ", 'j': "ị"},
    "o":  {'s': "ó", 'f': "ò", 'r': "ỏ", 'x': "õ", 'j': "ọ"},
    "ô": {'s': "ố", 'f': "ồ", 'r': "ổ", 'x': "ỗ", 'j': "ộ"},
    "ơ": {'s': "ớ", 'f': "ờ", 'r': "ở", 'x': "ỡ", 'j': "ợ"},
    "u":  {'s': "ú", 'f': "ù", 'r': "ủ", 'x': "ũ", 'j': "ụ"},
    "ư": {'s': "ứ", 'f': "ừ", 'r': "ử", 'x': "ữ", 'j': "ự"},
    "y":  {'s': "ý", 'f': "ỳ", 'r': "ỷ", 'x': "ỹ", 'j': "ỵ"}
}

# Tập các ký tự tone marker theo kiểu Telex.
tone_markers = set(['s', 'f', 'r', 'x', 'j'])

# Bản đồ chuyển đổi từ nguyên âm có dấu về dạng cơ bản.
accented_to_base = {
    "á": "a", "à": "a", "ả": "a", "ã": "a", "ạ": "a",
    "ắ": "ă", "ằ": "ă", "ẳ": "ă", "ẵ": "ă", "ặ": "ă",
    "ấ": "â", "ầ": "â", "ẩ": "â", "ẫ": "â", "ậ": "â",
    "é": "e", "è": "e", "ẻ": "e", "ẽ": "e", "ẹ": "e",
    "ế": "ê", "ề": "ê", "ể": "ê", "ễ": "ê", "ệ": "ê",
    "í": "i", "ì": "i", "ỉ": "i", "ĩ": "i", "ị": "i",
    "ó": "o", "ò": "o", "ỏ": "o", "õ": "o", "ọ": "o",
    "ố": "ô", "ồ": "ô", "ổ": "ô", "ỗ": "ô", "ộ": "ô",
    "ớ": "ơ", "ờ": "ơ", "ở": "ơ", "ỡ": "ơ", "ợ": "ơ",
    "ú": "u", "ù": "u", "ủ": "u", "ũ": "u", "ụ": "u",
    "ứ": "ư", "ừ": "ư", "ử": "ư", "ữ": "ư", "ự": "ư",
    "ý": "y", "ỳ": "y", "ỷ": "y", "ỹ": "y", "ỵ": "y"
}

def get_base(letter):
    """
    Trả về dạng cơ bản của một nguyên âm (loại bỏ dấu nếu có).
    """
    return accented_to_base.get(letter, letter)

# Tập các nguyên âm cơ bản tiếng Việt.
vowels = set("aăâeêiôơuưy")

def is_vietnamese_vowel(letter):
    """
    Kiểm tra xem ký tự (sau khi loại bỏ dấu) có phải là nguyên âm tiếng Việt.
    """
    return get_base(letter) in vowels

# Các tập nhóm quy tắc đặt dấu cho nguyên âm đôi.
accent_second = {"oa", "oe", "uy", "ue", "ia", "ie", "uo"}
accent_first  = {"ai", "ao", "au", "ay", "eo", "eu", "oi", "oo", "ui", "uu"}

def apply_tone(buffer, tone):
    """
    Áp dụng tone marker vào chuỗi buffer theo quy tắc:
      - Nếu chỉ có 1 nguyên âm, áp dụng luôn.
      - Nếu có 2 trở lên, dựa theo tổ hợp các nguyên âm (đã được chuyển về dạng cơ bản) để quyết định.
    Trả về tuple (buffer mới, True nếu áp dụng thành công, False nếu không).
    """
    vowel_indices = [i for i, ch in enumerate(buffer) if is_vietnamese_vowel(ch)]
    if not vowel_indices:
        return buffer, False

    if len(vowel_indices) == 1:
        target_index = vowel_indices[0]
    elif len(vowel_indices) >= 2:
        first = get_base(buffer[vowel_indices[0]])
        second = get_base(buffer[vowel_indices[1]])
        combo = first + second
        if combo == "ua":
            target_index = vowel_indices[0]
        elif combo == "oe":
            target_index = vowel_indices[1]
        elif combo in accent_second:
            target_index = vowel_indices[1]
        elif combo in accent_first:
            target_index = vowel_indices[0]
        else:
            target_index = vowel_indices[1]
    else:
        target_index = 0

    letter = buffer[target_index]
    base_letter = get_base(letter)
    if base_letter in accent_map and tone in accent_map[base_letter]:
        accented = accent_map[base_letter][tone]
        new_buffer = buffer[:target_index] + accented + buffer[target_index+1:]
        return new_buffer, True
    else:
        return buffer, False

def process_key(key, buffer):
    """
    Xử lý từng ký tự nhập vào:
      - Nếu key là tone marker ('s', 'f', 'r', 'x', 'j'), áp dụng dấu vào nguyên âm thích hợp.
      - Nếu là ký tự thông thường, thêm vào buffer và kiểm tra xem 2 ký tự cuối có tạo thành tổ hợp nguyên âm kép.
    Trả về buffer mới.
    """
    if key in tone_markers:
        new_buffer, applied = apply_tone(buffer, key)
        return new_buffer
    else:
        buffer += key
        # Kiểm tra chuyển đổi nguyên âm kép.
        if len(buffer) >= 2:
            combo = buffer[-2:]
            if combo in double_map:
                buffer = buffer[:-2] + double_map[combo]
        return buffer

def test_input(input_str):
    """
    Hàm kiểm thử quá trình nhập, in ra kết quả chuyển đổi.
    """
    buffer = ""
    for ch in input_str:
        buffer = process_key(ch, buffer)
    print(f"Input: {input_str} -> Output: {buffer}")

if __name__ == '__main__':
    # Một số test case mẫu
    test_input("aas")   # Ví dụ: nhập "a", "a", "s" -> mong đợi "ấ"
    test_input("awf")   # "a", "w" chuyển thành "ă", sau đó "f" -> mong đợi "ằ"
    test_input("dd")    # mong đợi "đ"
    test_input("oas")   # "o", "a" -> combo "oa", sau đó "s" -> mong đợi "oá"
    test_input("air")   # Với combo "ai" -> theo quy tắc -> mong đợi "ải"