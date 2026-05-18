# Bài toán
- Description
    - Do you recognize this cyberpunk baddie? We don't either. AI art generators are all the rage nowadays, which makes it hard to get a reliable known cover image. But we know you'll figure it out. The suspect is believed to be trafficking in classics. That probably won't help crack the stego, but we hope it will give motivation to bring this criminal to justice!
Download the image here

# Giải
## GIAI ĐOẠN 1
- Thử strings thử thì toàn ra rác và strings output.bmp | grep -i pico cũng không ra gì
- exiftool thử:
```
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Forensics/Invisible WORDs]
└─$ exiftool output.bmp
ExifTool Version Number         : 13.50
File Name                       : output.bmp
Directory                       : .
File Size                       : 2.1 MB
File Modification Date/Time     : 2026:05:18 04:43:34-04:00
File Access Date/Time           : 2026:05:18 04:45:35-04:00
File Inode Change Date/Time     : 2026:05:18 04:43:34-04:00
File Permissions                : -rwxrwxrwx
File Type                       : BMP
File Type Extension             : bmp
MIME Type                       : image/bmp
BMP Version                     : Windows V5
Image Width                     : 960
Image Height                    : 540
Planes                          : 1
Bit Depth                       : 32
Compression                     : Bitfields
Image Length                    : 2073600
Pixels Per Meter X              : 11811
Pixels Per Meter Y              : 11811
Num Colors                      : Use BitDepth
Num Important Colors            : All
Red Mask                        : 0x00007c00
Green Mask                      : 0x000003e0
Blue Mask                       : 0x0000001f
Alpha Mask                      : 0x00000000
Color Space                     : sRGB
Rendering Intent                : Proof (LCS_GM_GRAPHICS)
Image Size                      : 960x540
Megapixels                      : 0.518
```
- Kết quả `exiftool` cho thấy file này là một file ảnh BMP chuẩn, không có dấu hiệu nhét thêm dữ liệu lạ vào phần siêu dữ liệu (Metadata).

Tuy nhiên, có một chi tiết kỹ thuật cực kỳ quan trọng giúp thu hẹp phạm vi tìm kiếm:

* **Bit Depth: 32** (Mỗi pixel sử dụng 32 bit dữ liệu).
* **Compression: Bitfields** kết hợp với các giá trị Mask:
* `Red Mask: 0x00007c00`
* `Green Mask: 0x000003e0`
* `Blue Mask: 0x0000001f`
* `Alpha Mask: 0x00000000`

- Điều này có nghĩa là mặc dù file khai báo 32-bit cho mỗi pixel, nhưng thực tế các bit màu chỉ dùng định dạng **RGB555** (5 bit cho mỗi màu Red, Green, Blue, tổng cộng là 15 bit dữ liệu màu thực). Phần còn lại (đặc biệt là kênh Alpha hoặc các bit cao không được gán mask) hoàn toàn trống rỗng. Đây chính là "bãi đất trống" lý tưởng để người ta giấu toàn bộ một file hoặc một chuỗi văn bản vào đó mà không làm thay đổi màu sắc hiển thị của ảnh!

## GIAI ĐOẠN 2 - sử dụng stegsolve.jar
- `StegSolve` xử lý trích xuất bitfields của ảnh BMP V5 rất chuẩn và xuất thẳng ra file mà không bị dính lỗi độ dài block.

1. Chạy StegSolve bằng lệnh:
```bash
java -jar stegsolve.jar
```
2. Mở file ảnh `output.bmp` (hoặc `fixed_output.bmp`).
3. Trên thanh menu, chọn **Analyse** -> **Data Extract**.
4. Xem các bảng trích xuất dữ liệu thì thấy toàn rác 
- Có vẻ hướng đi này sai rồi có vẻ bài sẽ không xử lý theo bit

## GIAI ĐOẠN 3 - dùng stegoveritas
- Để không mất thời gian đoán mò cấu trúc bit nữa, chúng ta sẽ dùng một công cụ chuyên trị các bài toán giấu tin LSB/Bitfield trên ảnh BMP của giải **picoCTF**, đó là **`stegoveritas`**. Công cụ này tự động hơn `zsteg`, nó sẽ trích xuất *tất cả* các tổ hợp bit khả thi và tự động giải nén (giải zlib, giải mã...) rồi lưu thành các file kết quả rõ ràng cho ta.

- chạy `stegoveritas` trực tiếp trên file ảnh gốc `output.bmp` (hoặc file `fixed_output.bmp` đều được):

```bash
stegoveritas output.bmp
```

- Sau khi chạy xong, `stegoveritas` sẽ tạo ra một thư mục mới có tên là **`results/`** ngay tại thư mục hiện hành của ta.

- Nó đã tự động làm hộ ta những việc sau:

1. Trích xuất tất cả các bit plane (từ bit 0 đến bit 7 của các kênh R, G, B, Alpha, RGB).
2. Tự động quét xem bit nào chứa file nén, file zlib, file text... rồi **tự giải nén luôn**.

- đi vào thư mục kết quả và dùng lệnh `grep` để tìm flag:

```bash
cd results
grep -r -i "pico" .
```
- Vẫn không ra gì hết hướng này lại sai

## GIAI ĐOẠN 4 
- Kết quả `grep` cho thấy `stegoveritas` vẫn chưa tìm ra chuỗi trực tiếp chứa chữ `pico` trong các file đã bóc tách tự động.
- nhìn lại vào thông số cấu trúc byte của pixel:

* **BitDepth:** 32 (Mỗi pixel chiếm 4 bytes = 32 bits trong bộ nhớ).
* **RedMask:** `0x00007c00`
* **GreenMask:** `0x000003e0`
* **BlueMask:** `0x0000001f`
* **AlphaMask:** `0x00000000`

- Tổng số bits thực sự được dùng để hiển thị màu sắc chỉ là $5 + 5 + 5 = 15$ bits (định dạng RGB555).
- Trong 32 bits của một pixel, các bit từ số 16 đến 31 (2 bytes cao còn lại) hoàn toàn **không được gán vào đâu cả** (AlphaMask bằng 0). Người làm đề có thể đã lợi dụng 2 bytes trống này trên mỗi pixel để ghi đè dữ liệu của một file văn bản vào đó. Vì các bit này không ảnh hưởng đến màu hiển thị, nên file ảnh nhìn hoàn toàn bình thường.

- Bây giờ, chúng ta sẽ tự viết một script Python ngắn để gom toàn bộ các byte trống này lại và lưu thành một file.

- Sau khi chạy script và mở file .dat và find pico thì ta thấy FLAG
# Note
* **Kỹ thuật giấu tin:** Ghi đè dữ liệu vào vùng đệm không sử dụng (Padding/Alpha bits) của cấu hình màu `Bitfields` trên ảnh 32-bit BMP.
* **Dấu hiệu nhận biết (qua `exiftool`):**
* `Bit Depth: 32` (Mỗi pixel chiếm 4 bytes trong bộ nhớ).
* `Red/Green/Blue Mask` chỉ chiếm tổng cộng 15 bits (định dạng màu RGB555).
* `Alpha Mask: 0x00000000` (Kênh Alpha bằng 0, nghĩa là 2 bytes cao của mỗi pixel hoàn toàn trống).


* **Lý do công cụ tự động (`zsteg`, `stegoveritas`, `StegSolve`) thất bại:** Các công cụ này mặc định chỉ quét qua các bit thấp (LSB) của từng kênh màu đơn lẻ, không tự động gộp các byte trống ở phân vùng cao của cấu trúc pixel 32-bit.

---

## Cấu trúc Pixel & Giải pháp lập trình

Do ảnh BMP lưu dữ liệu theo cơ chế **Little Endian**, cấu trúc 4 bytes của một pixel trong bộ nhớ được sắp xếp như sau:

| Byte 0 (Màu) | Byte 1 (Màu) | Byte 2 (Trống/Giấu tin) | Byte 3 (Trống/Giấu tin) |
| --- | --- | --- | --- |
| RGB555 (Low) | RGB555 (High) | **Dữ liệu ẩn 1** | **Dữ liệu ẩn 2** |
