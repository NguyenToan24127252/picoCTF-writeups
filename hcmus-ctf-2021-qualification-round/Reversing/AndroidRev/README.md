## AndroidRev (200 points)

#### Solved by nhanlun

```
I hope you are a good reverse engineer and you can reverse all the things. How about Android? I think it's much easier than the others =D Thanks my professor for this chall :)

https://drive.google.com/file/d/1VpA49XbgDeDJGM_h0UA3IE7lvk7mLX_I/view

author: pakkunandy
```

**Flag:** `HCMUS-CTF{peppa-9876543-BAAAM-A1z9-3133337}`

# Writeup của tôi
- Đầu tiên tôi dùng tool apktool để bung file APK ra xem cấu trúc và file XML
```
apktool d androidrev.apk -o output_folder
```
- grep tìm cờ thử coi có gì đáng nghi không, ta thấy:
```
grep -rni "HCMUS-CTF" output_folder/
```
- activity_main.xml: Đây chỉ là giao diện (UI) hiển thị ô nhập với gợi ý (hint) dạng HCMUS-CTF{...}.
- FlagChecker.smali: Đây mới là "long mạch" của bài toán. File này chứa toàn bộ logic kiểm tra xem flag ta nhập vào là đúng hay sai.
- Chạy jadx-gui xem thử hàm hoạt động sao

### Phân tích Tĩnh (Static Analysis) với JADX-GUI

Mở file `androidrev.apk` bằng công cụ **JADX-GUI**, ta tìm đến lớp `com.hcmusctf.androidrev.FlagChecker` để đọc hiểu mã nguồn Java đã được dịch ngược. Hàm xử lý chính là `checkFlag(Context ctx, String flag)`:

```java
public static boolean checkFlag(Context ctx, String flag) {
    if (!flag.startsWith("HCMUS-CTF{") || !flag.endsWith("}")) {
        return false;
    }
    String core = flag.substring(10, 42);
    if (core.length() != 32) {
        return false;
    }
    String[] ps = core.split(foo());
    if (ps.length != 5 || !bim(ps[0]) || !bum(ps[2]) || !bam(ps[4]) || !core.replaceAll("[A-Z]", "X").replaceAll("[a-z]", "x").replaceAll("[0-9]", " ").matches("[A-Za-z0-9]+.  .  .[A-Za-z0-9]+.[Xx ]+.[A-Za-z0-9 ]+")) {
        return false;
    }
    // ... [Đoạn sau thực hiện kiểm tra ký tự phân tách và so sánh Hash] ...
}

```

#### 1. Định dạng cấu trúc của Flag (Tokenize)

* Flag bắt đầu bằng cụm `HCMUS-CTF{` và kết thúc bằng `}`.
* Chuỗi con ở giữa (`core`) có độ dài bắt buộc là **32 ký tự**.
* Hàm `core.split(foo())` thực hiện băm chuỗi thành mảng `ps` gồm 5 phần tử. Khảo sát hàm `foo()`, ta thấy một chuỗi mã hóa được giải mã **Base64 liên tục 10 lần**, kết quả trả về là ký tự **`"-"`** (dấu gạch ngang).

$\rightarrow$ Chuỗi `core` sẽ có định dạng phân tách: `ps[0]-ps[1]-ps[2]-ps[3]-ps[4]`.

#### 2. Rà soát điều kiện các phân đoạn (Regex Validation)

Dựa vào các hàm kiểm tra điều kiện định dạng:

* `ps[0]`: Chỉ chứa chữ cái viết thường (`^[a-z]+$`).
* `ps[2]`: Chỉ chứa chữ cái viết hoa (`^[A-Z]+$`).
* `ps[4]`: Chỉ chứa chữ số (`^[0-9]+$`).

---

### "Cú lừa" từ cơ chế so sánh và Kỹ thuật Reflection

Nhìn vào đoạn cuối cùng của hàm kiểm tra, chương trình gọi hàm `me` để so sánh các phân đoạn:

```java
me(ctx, dh(gs(ctx.getString(R.string.ct1), ctx.getString(R.string.k1)), ps[0]), ctx.getString(R.string.t1))

```

Bóc tách các hàm bổ trợ:

* **Hàm `gs**`: Thực hiện phép toán **XOR** giữa các chuỗi `ct` và `k` lấy ra từ file cấu hình `strings.xml`. Thử tính toán nhanh các cặp này, kết quả đều trả về chuỗi `"MD5"` (Riêng cặp số 6 trả về `"SHA-256"`).
* **Hàm `dh**`: Nhận vào tên thuật toán mã hóa (MD5) để băm các phân đoạn input (`ps[0]` đến `ps[4]`).
* **Hàm `me**`: Sử dụng Java Reflection để gọi hàm lật ngược từ `slauqe` (chuỗi ẩn trong `R.string.m1`) $\rightarrow$ `"equals"`.

> **⚠️ Điểm mấu chốt (Anti-Analysis / Honeypot):**
> Thông thường, chương trình sẽ so sánh $\text{MD5}(\text{Input}) == \text{Hash Đích}$. Tuy nhiên, tác giả bài này đã **đảo ngược tư duy** bằng cách truyền tham số:
> `me(..., dh(..., ps[0]), ctx.getString(R.string.t1))`
> Điều này có nghĩa là: Ứng dụng lấy **Mã băm MD5 của chuỗi ta nhập vào** đem đi so sánh với **Một chuỗi văn bản thô (Plaintext) lưu trong `strings.xml**` (chứ các giá trị `t1` đến `t5` không phải là mã băm gốc của flag). Nếu lười đọc code mà mang các chuỗi `t1`, `t2` đi giải băm (Decrypt) trên các trang online, ta sẽ ăn phải "Flag giả" (`hello-and_wel...`).

---

### Khai thác và Tìm Flag thật (Exploitation)

Để tìm các phân đoạn đúng, ta truy cập vào file `output_folder/res/values/strings.xml` thu được từ bước `apktool` trước đó để lấy các chuỗi mục tiêu `t1` đến `t5`:

* `t1` = `6e9a4d130a9b316e9201238844dd5124`
* `t2` = `7c51a5e6ea3214af970a86df89793b19`
* `t3` = `e5f20324ae520a11a86c7602e29ecbb8`
* `t4` = `1885eca5a40bc32d5e1bca61fcd308a5`
* `t5` = `da5062d64347e5e020c5419cebd149a2`

Vì phép so sánh là $\text{MD5}(\text{ps[x]}) == \text{t[x]}$, công việc của ta bây giờ là đi tìm các từ khóa sao cho **khi băm MD5 sẽ cho ra đúng các chuỗi trên**. Viết script dịch ngược lại nó:

* `ps[0]` = `peppa` (Có MD5 là `6e9a4d13...`)
* `ps[1]` = `9876543` (Có MD5 là `7c51a5e6...`)
* `ps[2]` = `BAAAM` (Có MD5 là `e5f20324...`)
* `ps[3]` = `A1z9` (Có MD5 là `1885eca5...`)
* `ps[4]` = `3133337` (Có MD5 là `da5062d6...`)

Ráp các phân đoạn lại theo đúng cấu trúc định dạng phân tách bằng dấu gạch ngang (`-`), ta có được flag hoàn chỉnh.



```
<resources>
<string name="abc_action_bar_home_description">Navigate home</string>
<string name="abc_action_bar_up_description">Navigate up</string>
<string name="abc_action_menu_overflow_description">More options</string>
<string name="abc_action_mode_done">Done</string>
<string name="abc_activity_chooser_view_see_all">See all</string>
<string name="abc_activitychooserview_choose_application">Choose an app</string>
<string name="abc_capital_off">OFF</string>
<string name="abc_capital_on">ON</string>
<string name="abc_menu_alt_shortcut_label">Alt+</string>
<string name="abc_menu_ctrl_shortcut_label">Ctrl+</string>
<string name="abc_menu_delete_shortcut_label">delete</string>
<string name="abc_menu_enter_shortcut_label">enter</string>
<string name="abc_menu_function_shortcut_label">Function+</string>
<string name="abc_menu_meta_shortcut_label">Meta+</string>
<string name="abc_menu_shift_shortcut_label">Shift+</string>
<string name="abc_menu_space_shortcut_label">space</string>
<string name="abc_menu_sym_shortcut_label">Sym+</string>
<string name="abc_prepend_shortcut_label">Menu+</string>
<string name="abc_search_hint">Search…</string>
<string name="abc_searchview_description_clear">Clear query</string>
<string name="abc_searchview_description_query">Search query</string>
<string name="abc_searchview_description_search">Search</string>
<string name="abc_searchview_description_submit">Submit query</string>
<string name="abc_searchview_description_voice">Voice search</string>
<string name="abc_shareactionprovider_share_with">Share with</string>
<string name="abc_shareactionprovider_share_with_application">Share with %s</string>
<string name="abc_toolbar_collapse_description">Collapse</string>
<string name="app_name">androidrev</string>
<string name="ct1">xwe</string>
<string name="ct2">asd</string>
<string name="ct3">uyt</string>
<string name="ct4">42s</string>
<string name="ct5">p0X</string>
<string name="ct6">70 IJTR</string>
<string name="k1">53P</string>
<string name="k2">,7Q</string>
<string name="k3">8=A</string>
<string name="k4">yvF</string>
<string name="k5">=tm</string>
<string name="k6">dxa</string>
<string name="m1">slauqe</string>
<string name="search_menu_title">Search</string>
<string name="status_bar_notification_info_overflow">999+</string>
<string name="t1">6e9a4d130a9b316e9201238844dd5124</string>
<string name="t2">7c51a5e6ea3214af970a86df89793b19</string>
<string name="t3">e5f20324ae520a11a86c7602e29ecbb8</string>
<string name="t4">1885eca5a40bc32d5e1bca61fcd308a5</string>
<string name="t5">da5062d64347e5e020c5419cebd149a2</string>
<string name="t6">
58150e58ae8a7275fcce5aea7d983ab5654f549cbeecedec27c89fe8246937d5
</string>
</resources>
```