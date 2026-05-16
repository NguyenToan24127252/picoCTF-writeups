# Bài toán
- Description
    - Can you find the flag?
shark1.pcapng

# Giải
- Đầu tiên dùng statistic (di xuống mục http->requests trong statistics), ta thấy /flag và / trong địa chỉ 18.217.1.57 
![statistics](statistic.png)
- Dùng strings:
```
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Forensics/Wireshark twoo twooo two twoo]
└─$ strings shark2.pcapng | grep "pico"
picoCTF{bfe48e8500c454d647c55a4471985e776a07b26cba64526713f43758599aa98b}
picoCTF{bda69bdf8f570a9aaab0e4108a0fa5f64cb26ba7d2269bb63f68af5d98b98245}
picoCTF{fe83bcb6cfd43d3b79392f6a4232685f6ed4e7a789c2ce559cf3c1ab6adbe34b}
picoCTF{711d3893d90f100c15e10ef4842abeed3a830f8237c1257cd47389646da97810}
...
```
- Ta thấy toàn là fake flag
- filter dns thì thấy rất nhiều dns request đến {sub-domain}.reddshrimpandherring.com

- Nhìn vào thì maybe máy chủ nạn nhân là 192.168.38.104
- Tiếp tục filter http and ip.addr==18.217.1.57 and follow http stream

* Có vẻ là địa chỉ 18.217.1.57 là 1 gợi ý gì đó
- Filter dns and ip.dst==18.217.1.57

* Ta thấy cái sub-domain là một chuỗi base64 -> nối chúng =>Flag
```
┌──(kali㉿kali)-[/mnt/hgfs/picoCTF-writeups/Forensics/Wireshark twoo twooo two twoo]
└─$ tshark -r shark2.pcapng -Y "dns.flags.response == 0 and ip.dst == 18.217.1.57" -T fields -e dns.qry.name | cut -d'.' -f1 | awk '!x[$0]++' | tr -d '\n' | base64 -d
picoCTF{...}           
```
# Note
- Tìm stream chứa phản hồi HTTP 200 OK
- Dấu hiệu nhận biết ROT13: Khi thấy cụm cvpbPGS, hãy nhớ ngay nó là picoCTF. Chữ c cách p 13 vị trí, v cách i 13 vị trí... Đây là "mẹo" để nhận diện nhanh loại mã hóa này.
- Có thể dùng lệnh strings shark1.pcapng | grep "cvpbPGS" để tìm nhanh chuỗi mã hóa mà không cần mở giao diện đồ họa.