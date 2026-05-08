import hashlib

username = b"BENNETT"
# Tính mã băm SHA-256 của username
hash_str = hashlib.sha256(username).hexdigest()

# Trích xuất các ký tự theo đúng thứ tự trong hàm check_key
dynamic_part = ""
dynamic_part += hash_str[4]
dynamic_part += hash_str[5]
dynamic_part += hash_str[3]
dynamic_part += hash_str[6]
dynamic_part += hash_str[2]
dynamic_part += hash_str[7]
dynamic_part += hash_str[1]
dynamic_part += hash_str[8]

# Ghép lại thành key hoàn chỉnh
prefix = "picoCTF{1n_7h3_kk3y_of_"
suffix = "}"
full_key = prefix + dynamic_part + suffix

print(f"License Key của bạn là: {full_key}")