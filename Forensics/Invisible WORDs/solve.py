with open("output.bmp", "rb") as f:
    bmp_data = f.read()

# Theo Exiftool, phần dữ liệu pixel (bits offset) bắt đầu từ byte thứ 138
pixel_start = 138
pixel_data = bmp_data[pixel_start:]

extracted_bytes = bytearray()

# Duyệt qua từng pixel (mỗi pixel chiếm 4 bytes)
for i in range(0, len(pixel_data), 4):
    if i + 4 <= len(pixel_data):
        pixel = pixel_data[i:i+4]
        # Pixel lưu dạng Little Endian: 2 bytes đầu là RGB555, 2 bytes sau là vùng trống (Alpha/Padding)
        # Chúng ta lấy 2 bytes trống này ra
        extracted_bytes.append(pixel[2])
        extracted_bytes.append(pixel[3])

# Ghi dữ liệu trích xuất được ra một file mới
with open("extracted_data.dat", "wb") as out:
    out.write(extracted_bytes)

print("Đã trích xuất xong vào file extracted_data.dat!")