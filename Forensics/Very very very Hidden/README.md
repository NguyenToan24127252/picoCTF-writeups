# Bài toán
- Description
    - Finding a flag may take many steps, but if you look diligently it won't be long until you find the light at the end of the tunnel. Just remember, sometimes you find the hidden treasure, but sometimes you find only a hidden map to the treasure. try_me.pcap
# Giải
- Thử các lệnh cơ bản :
```
# Tìm các chuỗi văn bản có độ dài từ 6 ký tự trở lên và lọc từ khóa HCMUS
strings try_me.pcap | grep -i "HCMUS"

# Tìm các từ khóa phổ biến trong CTF như flag, key, pass, secret
strings try_me.pcap | egrep -i "flag|key|pass|secret|map|treasure"

# Xem các dòng có chứa định dạng URL hoặc tên file
strings try_me.pcap | egrep -i "http|www|\.txt|\.zip|\.png|\.py"
```

* Này k ra gì quan trọng
```
# Kiểm tra xem bên trong PCAP có chứa các cấu trúc file ẩn khác không (như PNG, ZIP...)
binwalk try_me.pcap
```

* Thì thấy 2 file png trong .pcap 
- Ta dùng lệnh để xuất các file trong .pcap:
```
tshark -r try_me.pcap --export-objects http,extracted_files/
```
- Ta thấy có 2 file ảnh và 1 file txt (mở ra k có flag) , 1 file .ico (cũng rác)
- Ta nhận thấy 2 file ảnh thì 1 file evil_duck nó lớn hơn duck nhưng mà lại rỗ hơn có vẻ là bị dấu bởi gì rồi -> khả năng các pixel của ảnh đã bị sửa đổi để "gánh" thêm một lượng dữ liệu khổng lồ bên trong.
- Sử dụng zsteg, steghide đủ mọi cách nhưng toàn rác là rác



### 1. Bản chất "Cú lừa" của bài toán (Tại sao chúng ta bị kẹt?)

* **Tại sao `zsteg` và `steghide` thất bại?** Thông thường, các công cụ như `zsteg` chỉ quét bit cuối cùng (**1 bit LSB**). Nhưng ở bài này, tác giả đã sử dụng một công cụ steganography dành riêng cho PowerShell có tên là **`Invoke-PSImage`**. Công cụ này không giấu 1 bit, mà nó lấy tới **4 bit cuối (4 least significant bits)** của **2 kênh màu** trong mỗi pixel để nhét dữ liệu.
* Vì cấu trúc phân bổ bit lấy tới 4 bit (thay vì 1 bit), nên khi chúng ta dùng Python hay `zsteg` để ép đọc theo kiểu 1 bit, dữ liệu bóc ra hoàn toàn bị lệch lũy thừa và biến thành "rác nhị phân" (đống file `.dat` lỗi font mà bạn nhận được).

---

### 2. Giải thích chi tiết các bước trong Writeup

#### Bước 1 & 2: Bắt mạch gói tin (PCAP)

ta mở file `try_me.pcap` và thấy hầu hết traffic bị mã hóa HTTPS (TLS). Tuy nhiên, có 5 request chạy HTTP thuần (không mã hóa). Họ lọc ra và thấy nạn nhân đã tải 2 file ảnh từ một server AWS: `duck.png` và `evil_duck.png`. Họ xuất 2 file này ra (giống hệt cách bạn dùng `tshark` đã làm).

#### Bước 3: Nghi vấn ngoại hình

File `evil_duck.png` (vịt độc ác) có dung lượng **nặng hơn rất nhiều** so với `duck.png`, nhưng nhìn bằng mắt thường thì chất lượng ảnh lại **tệ hơn**. Điều này chứng tỏ các pixel của ảnh đã bị sửa đổi để "gánh" thêm một lượng dữ liệu khổng lồ bên trong.

#### Bước 4 & 5: L lần theo dấu vết lịch sử duyệt web (OSINT trong PCAP)

Đây là bước cực kỳ hay! Dù HTTPS mã hóa nội dung tải, nhưng nó **không mã hóa tên miền (Server Name Indication - SNI)**. ta đã soi dòng thời gian duyệt web của nạn nhân:

1. Nạn nhân lên Google tìm kiếm một thứ gì đó.
2. Nạn nhân vào GitHub xem mã nguồn.
3. Nạn nhân đọc tài liệu hướng dẫn trên `docs.microsoft.com`.
4. Nạn nhân tải file `evil_duck.png`.
5. Nạn nhân vào `powershell.org` (Cộng đồng script PowerShell).

#### Bước 6: Tìm ra "Vũ khí" của thủ phạm

Từ chuỗi hành động trên: *GitHub + Microsoft Docs + PowerShell + Giấu tin vào ảnh PNG*, ta thực hiện một cú tìm kiếm với từ khóa `"powershell steganography"` và tìm ra ngay một tool nổi tiếng trên GitHub tên là [Invoke-PSImage](https://github.com/peewpw/Invoke-PSImage/tree/master). Tool này chuyên dùng để **giấu một đoạn script PowerShell vào trong các pixel của ảnh PNG**.

##### Cách 1: Sử dụng công cụ đồ họa `PowershellStegoDecode.exe` (Môi trường Windows)

* **Thao tác:** Nếu có sẵn môi trường Windows (yêu cầu cài đặt thêm .NET Framework 3.5), ta có thể sử dụng một chương trình được biên dịch sẵn trên mạng là `PowershellStegoDecode.exe`.
* **Kết quả:** Chỉ cần mở ảnh `evil_duck.png` trực tiếp bằng phần mềm này, chương trình sẽ tự động bóc các bit màu hệ thống và in ngay đoạn mã PowerShell ẩn ra màn hình giao diện trực quan.

##### Cách 2: Sử dụng bộ đôi Script Python tự chế (Môi trường Kali Linux)

Nếu không muốn phụ thuộc vào phần mềm Windows hoặc muốn tự động hóa hoàn toàn bằng dòng lệnh (CLI), ta sử dụng quy trình 2 bước bằng Python:

* **Bước 6.1: Trích xuất mã nguồn ẩn bằng `find_powershell_in_png.py**`
Ta chạy script Python `find_powershell_in_png.py` để duyệt qua cấu trúc pixel màu theo đúng thuật toán của `Invoke-PSImage` (trích xuất 4-bit thấp từ các kênh màu của ảnh).
```bash
python find_powershell_in_png.py
```

Lệnh này sẽ bóc tách và giải phóng hoàn toàn đoạn script PowerShell bị giấu, xuất thẳng kết quả ra một file văn bản sạch sẽ tên là **`extracted_script.ps1`**.
* **Bước 6.2: Giải mã phép toán mật mã XOR bằng `solve.py**`
Khi mở file `extracted_script.ps1` vừa tạo, ta sẽ thấy đoạn code chứa hai chuỗi dữ liệu đã bị mã hóa là `$string1` (Khóa) và `$string2`. Ta lấy hai chuỗi này nạp vào file script giải mã **`solve.py`** để chương trình tự động thực hiện phép toán đảo ngược XOR từng byte ký tự.
```bash
python solve.py
```

Kết quả cuối cùng sẽ khôi phục lại định dạng văn bản gốc và in ra Flag mục tiêu của bài toán.

---

### 3. Phân tích đoạn code PowerShell tìm thấy trong ảnh

Khi đưa ảnh `evil_duck.png` vào công cụ giải mã, nó không ra thẳng flag mà ra một đoạn mã PowerShell (Đúng như gợi ý của đề bài: *"Đôi khi bạn chỉ tìm thấy tấm bản đồ dẫn đến kho báu"*).

Đoạn code đó như sau:

```powershell
$out = "flag.txt"
$enc = [system.Text.Encoding]::UTF8
# Chuỗi mã hóa 1 (Chìa khóa XOR)
$string1 = "HEYWherE(IS_tNE)50uP?^DId_YOu(]E@t*mY_3RD()B2g3l?"
# Chuỗi mã hóa 2 (Dữ liệu đã bị XOR)
$string2 = "8,:8+14>Fx0l+$*KjVD>[o*.;+1|*[n&2G^201l&,Mv+_'T_B"

$data1 = $enc.GetBytes($string1)
$bytes = $enc.GetBytes($string2)

# Vòng lặp duyệt qua từng ký tự để thực hiện phép toán XOR (^_^)
for($i=0; $i -lt $bytes.count ; $i++)
{
    $bytes[$i] = $bytes[$i] -bxor $data1[$i] # Lấy từng byte của string2 XOR với string1
}
# Ghi kết quả sau khi XOR ra file flag.txt
[System.IO.File]::WriteAllBytes("$out", $bytes)

```

### Phép toán XOR hoạt động thế nào ở đây?

Trong mật mã học, phép toán **XOR (Exclusive OR)** có một tính chất đặc biệt: Nếu bạn lấy dữ liệu $A \oplus B = C$, thì khi bạn lấy $C \oplus A$, nó sẽ trả ngược lại về $B$.

* Tác giả đã lấy chuỗi Flag thật ($B$) đem XOR với một chuỗi rác `string1` ($A$) để tạo ra chuỗi ký tự kỳ dị `string2` ($C$).
* Đoạn script trên chỉ làm nhiệm vụ đảo ngược: Lấy `string2` XOR ngược lại với `string1` để khôi phục lại các byte ban đầu của Flag.

Khi chạy đoạn script này trong môi trường PowerShell, các byte được giải mã sẽ ráp lại thành chuỗi văn bản hoàn chỉnh và ghi vào file `flag.txt`:
**`picoCTF{.....}`**

---

### Tóm tắt lại luồng bài giải:

Phân tích PCAP $\rightarrow$ Trích xuất 2 ảnh Vịt $\rightarrow$ Theo dõi SNI phát hiện nạn nhân dùng PowerShell Steganography $\rightarrow$ Dùng tool giải mã 4-bit LSB của PowerShell thu được script mã hóa $\rightarrow$ Chạy script thực hiện phép tính XOR $\rightarrow$ **Ra Flag**. Một bài Forensics rất thực tế và cực kỳ thú vị!

# Note
### 1. Tư duy "Dòng thời gian" (OSINT trong Phân tích Mạng)

* **Bài học:** Đừng chỉ chăm chăm nhìn vào payload (dữ liệu thô) của gói tin khi bị kẹt. Hãy nhìn vào hành vi và lộ trình của đối tượng.
* **Áp dụng:** Việc TLS/HTTPS mã hóa nội dung không có nghĩa là nó vô dụng. Tiêu đề **SNI (Server Name Indication)** trong các gói tin Handshake luôn để lộ các tên miền (Google, GitHub, Microsoft Docs, Powershell.org). Xâu chuỗi lịch sử duyệt web này chính là chìa khóa vàng giúp thu hẹp phạm vi và đoán biết được thủ phạm đã dùng "vũ khí" (công cụ) gì.

### 2. Sự nguy hiểm của việc "Rập khuôn công cụ" (Tool Reliance)

* **Bài học:** Các công cụ tự động như `zsteg`, `steghide` hay `stegsolve` rất mạnh nhưng chúng hoạt động dựa trên các giả định tiêu chuẩn (ví dụ: chỉ quét 1 bit LSB, chỉ hỗ trợ định dạng ảnh nhất định). Khi gặp các kỹ thuật tùy biến (Custom Steganography), các công cụ này sẽ hoàn toàn bị mù và chỉ trả ra rác.
* **Áp dụng:** Luôn sẵn sàng đặt câu hỏi về thuật toán đứng sau. Khi thấy dung lượng ảnh lệch quá lớn nhưng `zsteg` ra rác, phải nghi ngờ ngay cấu trúc phân bổ bit màu đã bị thay đổi (như cách `Invoke-PSImage` lấy tới 4 bit thấp của cả 2 kênh màu R và G).

### 3. Nguyên lý Giấu tin trong PowerShell (`Invoke-PSImage`)

* **Bài học:** Hiểu thêm một kỹ thuật giấu tin nâng cao của các cuộc tấn công APT ngoài thực tế. Mã độc thường giấu các script độc hại (Payload) vào trong các file ảnh vô hại được lưu trữ trên các máy chủ public (như AWS) để vượt qua các hệ thống tường lửa (Firewall) hoặc Antivirus.
* **Cơ chế:** Kết hợp $4 \text{ bits}$ của kênh **Red** và $4 \text{ bits}$ của kênh **Green** trên mỗi pixel màu để tạo thành $8 \text{ bits}$ ($1 \text{ byte}$) dữ liệu script hoàn chỉnh.

### 4. Nhận diện "Cú lừa" và Tạp chất mạng trong Forensics

* **Bài học:** Không phải file nào trích xuất được từ PCAP (như `NothingSus`, `favicon.ico`) cũng chứa thông tin mật.
* **Áp dụng:** Đọc hiểu mã phản hồi mạng (như lỗi 404 trả về trang HTML rác có đuôi `.ico`) giúp ta nhanh chóng sàng lọc, loại bỏ các file gây nhiễu để tập trung thời gian vào mục tiêu khả nghi nhất (file ảnh bị rỗ, nặng bất thường).

### 5. Tư duy "Mở hộp" lồng nhau (Layered Challenge)

* **Bài học:** Các bài Forensics điểm cao của giải lớn như picoCTF hiếm khi cho ra ngay Flag sau một bước giải mã.
* **Áp dụng:** Luôn chuẩn bị tinh thần cho việc: Giải mã lớp mạng $\rightarrow$ Tìm ra file ảnh $\rightarrow$ Giải mã lớp ảnh $\rightarrow$ Tìm ra đoạn code script $\rightarrow$ Giải mã lớp mật mã (XOR) $\rightarrow$ Cuối cùng mới chạm tay vào Flag. Gợi ý *"Đôi khi bạn chỉ tìm thấy tấm bản đồ"* là dấu hiệu nhắc nhở phải tiếp tục kiên trì phân tích lớp tiếp theo.