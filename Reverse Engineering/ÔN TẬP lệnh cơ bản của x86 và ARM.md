# 📝 Ôn tập Tập lệnh Assembly cơ bản (x86 & ARM)

## 1. Tổng quan về Đăng ký (Registers)

Trước khi đi vào tập lệnh, cần nhớ rằng Assembly thao tác trực tiếp trên các ô nhớ đặc biệt của CPU gọi là thanh ghi.

* **x86_64:** `RAX`, `RBX`, `RCX`, `RDX`, `RSI`, `RDI`, `RBP`, `RSP`, `RIP`.
* **ARM:** `R0` đến `R15`. Trong đó `R13` là Stack Pointer (SP), `R14` là Link Register (LR), và `R15` là Program Counter (PC).

---

## 2. Các lệnh di chuyển dữ liệu (Data Movement)

### **MOV (Move)**

Sao chép dữ liệu từ nguồn sang đích.

* **x86:** `MOV destination, source`
* `MOV EAX, 1` (Gán EAX = 1)


* **ARM:** `MOV R0, #1` (Gán R0 = 1)
* **Lưu ý:** Lệnh này không di chuyển thực sự mà là **sao chép** (nguồn vẫn giữ nguyên giá trị).

### **PUSH & POP (Stack Operations)**

Thao tác với ngăn xếp (Stack) theo cơ chế LIFO (Vào sau ra trước).

* **PUSH:** Đẩy một giá trị vào đỉnh Stack. `RSP` (x86) hoặc `SP` (ARM) sẽ giảm xuống.
* **POP:** Lấy giá trị từ đỉnh Stack ra thanh ghi. `RSP`/`SP` sẽ tăng lên.

---

## 3. Các lệnh điều khiển luồng (Control Flow)

### **CMP (Compare)**

So sánh hai toán hạng bằng cách thực hiện phép trừ giả định (`đích - nguồn`) để thiết lập các cờ hiệu (Flags) như Zero Flag (ZF), Carry Flag (CF).

* **x86:** `CMP EAX, EBX`
* **ARM:** `CMP R0, R1`

### **JMP / B (Jump / Branch)**

Thay đổi luồng thực thi của chương trình bằng cách nhảy đến một địa chỉ khác.

* **x86:** `JMP <address>` (Nhảy không điều kiện).
* **ARM:** `B <address>` (Branch - Nhảy không điều kiện).

### **Nhảy có điều kiện (Conditional Jumps)**

Dựa trên kết quả của lệnh `CMP` trước đó:

* `JE` / `BEQ`: Nhảy nếu bằng nhau (Equal).
* `JNE` / `BNE`: Nhảy nếu không bằng nhau (Not Equal).
* `JG` / `BGT`: Nhảy nếu lớn hơn (Greater Than).
* `JL` / `BLT`: Nhảy nếu nhỏ hơn (Less Than).

---

## 4. Bảng so sánh nhanh x86 vs ARM

| Đặc điểm | x86 (CISC) | ARM (RISC) |
| --- | --- | --- |
| **Cú pháp** | `Opcode đích, nguồn` | `Opcode đích, nguồn 1, nguồn 2` |
| **Kích thước lệnh** | Thay đổi (1 - 15 bytes) | Cố định (thường 4 bytes) |
| **Thao tác bộ nhớ** | Có thể dùng `MOV` trực tiếp với bộ nhớ | Chỉ dùng `LDR` (Load) và `STR` (Store) |
| **Lệnh nhảy** | `JMP`, `CALL`, `RET` | `B`, `BL`, `BX` |

---

## 5. Mẹo ghi nhớ cho Reverse Engineering

> [!TIP]
> * **Tìm hàm main:** Hãy tìm các lệnh `PUSH RBP` hoặc `MOV RBP, RSP` (x86). Đây là thủ tục thiết lập khung hàm (Function Prologue).
> * **Giá trị trả về:** Trong x86, kết quả trả về của hàm hầu hết nằm ở thanh ghi `EAX`/`RAX`. Trong ARM, nó nằm ở `R0`.
> * **Hàm gọi (Call):** Khi thấy lệnh `CALL` (x86) hoặc `BL` (ARM), hãy chú ý các thanh ghi trước đó vì chúng đang nạp tham số cho hàm.
> 
> 

---

### Bài tập thực hành nhỏ:

Thử đọc đoạn code sau và đoán xem nó làm gì:

```nasm
MOV EAX, 10
MOV EBX, 20
CMP EAX, EBX
JL label_target

```

*Giải đáp: Nếu 10 < 20 (luôn đúng), chương trình sẽ nhảy đến địa chỉ `label_target`.*

---
