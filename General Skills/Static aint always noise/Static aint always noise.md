### Bài toán
- Description
    - Can you look at the data in this binary? The bash script might help!
static, ltdis.sh

### Giải
```
nguyentoan@nguyentoan-VMware-Virtual-Platform:~/Downloads$ ssh ctf-player@wily-courier.picoctf.net -p 50021
The authenticity of host '[wily-courier.picoctf.net]:50021 ([18.189.99.27]:50021)' can't be established.
ED25519 key fingerprint is SHA256:ErlUUvYlrAxfSW1tIdzfOnGTBSr5OFkZvz0nMN4Vodw.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[wily-courier.picoctf.net]:50021' (ED25519) to the list of known hosts.
ctf-player@wily-courier.picoctf.net's password: 
Welcome to Ubuntu 18.04.6 LTS (GNU/Linux 6.17.0-1010-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

ctf-player@pico-chall$ ls -la
total 8
drwxr-xr-x 1 ctf-player ctf-player 59 Sep 12  2025 .
drwxr-xr-x 1 ctf-player ctf-player 20 Apr 26 03:01 ..
-rw-r--r-- 1 ctf-player ctf-player 14 Aug 14  2025 1of3.flag.txt
-rw-r--r-- 1 ctf-player ctf-player 56 Aug 14  2025 instructions-to-2of3.txt
ctf-player@pico-chall$ grep "picoCTF" 1of3.flag.txt
picoCTF{xxsh_
ctf-player@pico-chall$ cat instructions-to-2of3.txt
Next, go to the root of all things, more succinctly `/`
ctf-player@pico-chall$ cd /
ctf-player@pico-chall$ ls
2of3.flag.txt  challenge  home			    lib64  opt	 run   sys  var
bin	       dev	  instructions-to-3of3.txt  media  proc  sbin  tmp
boot	       etc	  lib			    mnt    root  srv   usr
ctf-player@pico-chall$ grep "picoCTF" 2of3.flag.txt
ctf-player@pico-chall$ cat 2of3.flag.txt
0ut_0f_//4t3r_
ctf-player@pico-chall$ cat instructions-to-3of3.txt
Lastly, ctf-player, go home... more succinctly `~`
ctf-player@pico-chall$ cd ~
ctf-player@pico-chall$ ls
3of3.flag.txt  drop-in
ctf-player@pico-chall$ cat 3of3.flag.txt
0b24fc4f}ctf-player@pico-chall$ Connection to wily-courier.picoctf.net closed by remote host.
Connection to wily-courier.picoctf.net closed.
```
### Note
- Quy trình:
    - Thiết lập kết nối: Dùng ssh với port tùy chỉnh (-p 50021).
    - Xác thực Host: Chấp nhận fingerprint (dấu vân tay số) của server để thêm vào known_hosts.
    - Điều hướng (Navigation): Di chuyển giữa thư mục người dùng (~) và thư mục gốc của toàn hệ thống (/).
    - Trích xuất dữ liệu: Sử dụng cat để đọc file và grep để lọc chuỗi.
- SSH Fingerprint & Trust (Cơ chế tin cậy): Khi bạn thấy thông báo "The authenticity of host... can't be established", Linux đang hỏi bạn có tin tưởng server này không.
    - Lý thuyết: Đây là cơ chế chống tấn công Man-in-the-Middle (MitM). Nếu lần sau bạn kết nối mà Fingerprint này thay đổi, SSH sẽ cảnh báo ngay lập tức vì có thể ai đó đang giả mạo server.
- Linux Filesystem Hierarchy (Cấu trúc phân cấp): Bài Lab này minh họa hoàn hảo cấu trúc cây thư mục Linux:
    - / (Root): Điểm bắt đầu của mọi thứ. Chứa các thư mục quan trọng như /etc (cấu hình), /var (dữ liệu biến đổi/logs).
    - ~ (Home): Không gian riêng tư của User.
    - Mẹo SOC: Khi điều tra mã độc, bạn thường phải kiểm tra các file ẩn trong cả / và ~ vì mã độc thường giấu file cấu hình tại đây.
- SSH Port Security: Việc bài Lab dùng port 50021 thay vì 22 gọi là Security by Obscurity (Bảo mật bằng cách ẩn mình). Thực tế: Đổi port SSH mặc định giúp giảm tới 90% các cuộc tấn công tự động quét port trên internet.