import ctypes
import glob
import os

# Định nghĩa cấu trúc dữ liệu FILETIME của Windows trong Python
class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", ctypes.c_uint), 
                ("ftHighDateTime", ctypes.c_uint)]

# Định nghĩa cấu trúc WIN32_FILE_ATTRIBUTE_DATA để chứa mốc thời gian thô 64-bit từ NTFS
class WIN32_FILE_ATTRIBUTE_DATA(ctypes.Structure):
    _fields_ = [("dwFileAttributes", ctypes.c_uint),
                ("ftCreationTime", FILETIME),
                ("ftLastAccessTime", FILETIME),
                ("ftLastWriteTime", FILETIME), # Mtime (Modification Time)
                ("nFileSizeHigh", ctypes.c_uint),
                ("nFileSizeLow", ctypes.c_uint)]

def get_ntfs_mtime(filepath):
    wfad = WIN32_FILE_ATTRIBUTE_DATA()
    GetFileExInfoStandard = 0
    # Gọi WinAPI từ kernel32.dll để lấy mốc thời gian chính xác đến 100-nanosecond
    ctypes.windll.kernel32.GetFileAttributesExW(ctypes.c_wchar_p(filepath), GetFileExInfoStandard, ctypes.byref(wfad))
    
    # Trả về 32-bit thấp chứa dữ liệu ẩn
    return wfad.ftLastWriteTime.dwLowDateTime

# ... (Giữ nguyên phần định nghĩa cấu trúc dữ liệu ở trên)

print("[*] Đang trích xuất Flag theo đúng trình tự ẩn giấu của NTFS...")

ordered_items = [
    'test/Item01 - Copy.bmp',
    'test/Item02 - Copy.bmp',
    'test/Item03 - Copy.bmp',
    'test/Item04 - Copy.bmp',
    'test/Item05 - Copy.bmp',
    'test/Item06 - Copy.bmp',
    'test/Item07 - Copy.bmp',
    'test/Item08 - Copy.bmp',
    'test/ItemTest - Copy.bmp'
]

flag = ""
for path in ordered_items:
    if os.path.exists(path):
        low_time = get_ntfs_mtime(path)
        
        byte1 = (low_time >> 8) & 0xFF
        byte2 = low_time & 0xFF
        
        if 32 <= byte1 <= 126: flag += chr(byte1)
        if 32 <= byte2 <= 126: flag += chr(byte2)
    else:
        # Lệnh in debug để phát hiện xem script có bị lỗi đường dẫn không
        print(f"[!] LỖI: Không tìm thấy file tại đường dẫn: {path}")

print("\n" + "="*45)
print(f"FLAG XỊN TRÍCH XUẤT THÀNH CÔNG: {flag}")
print("="*45)