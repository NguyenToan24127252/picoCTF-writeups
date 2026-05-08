import hashlib

# Phần đầu cố định
prefix = "picoCTF{br1ng_y0ur_0wn_k3y_"

# Tính MD5 của phần đầu (giống lệnh MD5(local_98...))
m = hashlib.md5()
m.update(prefix.encode())
md5_hex = m.hexdigest()

# Nhặt các ký tự theo đúng thứ tự logic trong Ghidra
# Lưu ý: Ghidra dùng offset để đặt tên, thứ tự bên dưới khớp với auStack_38
dynamic_part = ""
dynamic_part += md5_hex[13] # local_6b
dynamic_part += md5_hex[18] # local_66
dynamic_part += md5_hex[29] # local_5b
dynamic_part += md5_hex[1]  # local_78[1]
dynamic_part += md5_hex[14] # local_6a
dynamic_part += md5_hex[24] # local_60
dynamic_part += md5_hex[26] # local_5e
dynamic_part += md5_hex[29] # local_5b (biến này xuất hiện 2 lần ở dòng 47 & 52)

full_flag = prefix + dynamic_part + "}"
print(f"Flag tìm được: {full_flag}")