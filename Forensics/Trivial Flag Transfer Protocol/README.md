# Bài toán
- Description
    - Figure out how they moved the flag. tftp.pcapng

# Giải
- Mở file pcap thì thấy khá nhiều các protocal TFTP -> filter TFTP thì thấy có instructions.txt
- Export objects -> TFTP -> Save all thì thấy có 3 file .bmp, instructions.txt, plan (ASCII text), program.deb
- cat 2 file plan và instructions thì thấy các chuỗi in hoa nghi là mật mã ROT13 -> giải mã nó:
```
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Forensics/Trivial Flag Transfer Protocol]
└─$ cat instructions.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
TFTPDOESNTENCRYPTOURTRAFFICSOWEMUSTDISGUISEOURFLAGTRANSFER.FIGUREOUTAWAYTOHIDETHEFLAGANDIWILLCHECKBACKFORTHEPLAN
                        
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Forensics/Trivial Flag Transfer Protocol]
└─$ # Giải mã file plan
cat plan | tr 'A-Za-z' 'N-ZA-Mn-za-m'
IUSEDTHEPROGRAMANDHIDITWITH-DUEDILIGENCE.CHECKOUTTHEPHOTOS
```
- Như manh mối nó ghi là: mật khẩu để bóc tách flag là chuỗi DUEDILIGENCE và Chương trình được dùng để giấu tin nằm trong file program.deb
- Kiểm tra program.deb cài phần mềm gì vào máy:
```
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Forensics/Trivial Flag Transfer Protocol]
└─$ dpkg-deb -I program.deb
 new Debian package, version 2.0.
 size 138310 bytes: control archive=1250 bytes.
     826 bytes,    18 lines      control
    1184 bytes,    17 lines      md5sums
 Package: steghide
 Source: steghide (0.5.1-9.1)
 Version: 0.5.1-9.1+b1
 Architecture: amd64
 Maintainer: Ola Lundqvist <opal@debian.org>
 Installed-Size: 426
 Depends: libc6 (>= 2.2.5), libgcc1 (>= 1:4.1.1), libjpeg62-turbo (>= 1:1.3.1), libmcrypt4, libmhash2, libstdc++6 (>= 4.9), zlib1g (>= 1:1.1.4)
 Section: misc
 Priority: optional
 Description: A steganography hiding tool
  Steghide is steganography program which hides bits of a data file
  in some of the least significant bits of another file in such a way
  that the existence of the data file is not visible and cannot be proven.
  .
  Steghide is designed to be portable and configurable and features hiding
  data in bmp, wav and au files, blowfish encryption, MD5 hashing of
  passphrases to blowfish keys, and pseudo-random distribution of hidden bits
  in the container data.
```
- Dòng Package: steghide cho thấy dùng steghide để giấu flag
- Thử trích xuất dữ liệu ẩn từ 3 file ảnh cùng mật khẩu tìm được ở trên:
```   
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Forensics/Trivial Flag Transfer Protocol]
└─$ steghide extract -sf picture1.bmp -p DUEDILIGENCE
steghide extract -sf picture2.bmp -p DUEDILIGENCE
steghide extract -sf picture3.bmp -p DUEDILIGENCE
steghide: could not extract any data with that passphrase!
steghide: could not extract any data with that passphrase!
wrote extracted data to "flag.txt".
```
- Tìm thấy flag trong file txt

# Note
### 1. Kỹ thuật ẩn giấu: Steganography kết hợp Covert Network Transfer
- **Bản chất của TFTP:** Giao thức TFTP (Trivial File Transfer Protocol) chạy trên nền UDP cổng 69. Đây là giao thức truyền file cực kỳ thô sơ, không hề có cơ chế xác thực (Authentication) và không mã hóa dữ liệu (Clear-text). Bất kỳ ai bắt được gói tin mạng đều có thể dễ dàng dùng tính năng `Export Objects` để trích xuất nguyên vẹn file ra ngoài.
- **Chiến thuật cấu trúc (Multi-layered Obfuscation):** Nhận thức được điểm yếu của TFTP, kẻ tấn công đã dựng lên một cấu trúc ẩn giấu thông tin qua nhiều tầng lớp:
  1. *Tầng giao thức mạng:* Truyền file thô qua TFTP.
  2. *Tầng mật mã cơ bản:* Mã hóa cấu trúc kế hoạch (`plan`) và hướng dẫn (`instructions.txt`) bằng ROT13 để tránh việc đọc lướt qua (gây khó cho các bộ lọc từ khóa tự động).
  3. *Tầng giấu tin nâng cao:* Sử dụng phần mềm `steghide` áp dụng thuật toán LSB (Least Significant Bit) để nhét dữ liệu Flag vào cấu trúc pixel của file ảnh Bitmap (`.bmp`) mà không làm thay đổi bề ngoài của bức ảnh.

### 2. Ý nghĩa của các manh mối trong bài
- **Tại sao lại có file `program.deb`?** Trong môi trường thực tế hoặc các bài CTF Forensics chuyên sâu, kẻ tấn công thường để lại chính công cụ thực thi của chúng để tránh phụ thuộc vào môi trường máy nạn nhân. Việc check thông tin gói `.deb` bằng lệnh `dpkg-deb -I` là một tư duy Forensics rất tốt, giúp xác định chính xác chữ ký (signature) của công cụ giấu tin (`steghide`) thay vì phải đoán mò giữa hàng tá công cụ như *Outguess, Stegghide, OpenStego...*
- **Chuỗi mật khẩu ngầm (The Passphrase Hint):** Cụm từ `DUEDILIGENCE` chính là chìa khóa. Trong Steganography, các công cụ mạnh như `steghide` sẽ băm mật khẩu (MD5/SHA) để làm khóa mã hóa (Blowfish/AES) trước khi phân tán các bit dữ liệu vào ảnh. Nếu không giải mã được file `plan` để lấy chữ này, việc bẻ khóa (Brute-force) bit ẩn trong ảnh `.bmp` là bất khả thi.

### 3. Kinh nghiệm thực chiến Forensics rút ra
- **Phân tích cục bộ sau khi trích xuất:** Khi Wireshark bàn giao cho bạn một danh sách các file đã trích xuất (`Export Objects`), cuộc điều tra mạng kết thúc và cuộc điều tra trên máy (Host Forensics) bắt đầu. Hãy luôn ưu tiên mở các file văn bản cấu hình/nhật ký trước (`.txt`, `.log`, `.cfg`) để tìm kịch bản hành vi của kẻ tấn công.
- **Thử nghiệm tự động hóa hoặc duyệt chuỗi:** Ở bước cuối cùng, khi có nhiều file ảnh (`picture1`, `picture2`, `picture3`), việc chạy lệnh tuần tự từ trên xuống dưới cho thấy tính kiên trì cần có của một người làm bảo mật. Nếu số lượng ảnh lên đến hàng trăm tấm, ta có thể tối ưu bằng một vòng lặp Bash ngắn:
  ```bash
  for img in *.bmp; do steghide extract -sf "$img" -p DUEDILIGENCE 2>/dev/null && break; done
  ```