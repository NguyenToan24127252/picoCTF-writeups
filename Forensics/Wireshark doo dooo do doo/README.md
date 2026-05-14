# Bài toán
- Description
    - Can you find the flag?
shark1.pcapng

# Giải
- Dùng bộ lọc tcp.stream eq -> lọc sơ từng stream nhìn nhanh thì thấy stream 5 có chứa phản hồi HTTP 200 OK 
- Chuột phải vào bất kỳ gói tin nào hiện ra sau khi lọc -> Chọn Follow -> TCP Stream -> một cửa sổ mới sẽ hiện ra hiển thị toàn bộ nội dung trao đổi giữa Client và Server.
- Thấy Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}
- Chuỗi trên sử dụng mã hóa ROT13 -> decode => FLAG
# Note
- Tìm stream chứa phản hồi HTTP 200 OK
- Dấu hiệu nhận biết ROT13: Khi thấy cụm cvpbPGS, hãy nhớ ngay nó là picoCTF. Chữ c cách p 13 vị trí, v cách i 13 vị trí... Đây là "mẹo" để nhận diện nhanh loại mã hóa này.
- Có thể dùng lệnh strings shark1.pcapng | grep "cvpbPGS" để tìm nhanh chuỗi mã hóa mà không cần mở giao diện đồ họa.