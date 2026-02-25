Practical CBC Malleability Attack & Secure Encrypt-then-MAC Design

A practical demonstration of CBC malleability, controlled bit-flipping attack, and a secure Encrypt-then-MAC mitigation.

1. Giới thiệu
Dự án này minh họa một vấn đề quan trọng trong mật mã ứng dụng:
AES-CBC cung cấp tính bảo mật (confidentiality), nhưng không đảm bảo tính toàn vẹn (integrity).
Điều đó có nghĩa là:
+ Dữ liệu có thể bị chỉnh sửa
+ Hệ thống vẫn giải mã thành công
+ Không có cơ chế phát hiện giả mạo
Dự án triển khai:
+ CBC encryption
+ Bit-flipping attack
+ Phân tích malleability
+ Giải pháp Encrypt-then-MAC (EtM)

2. Vì sao CBC bị malleable?
Trong CBC mode:
+ Mỗi block plaintext được tính từ block ciphertext trước đó
+ Nếu attacker thay đổi một block ciphertext
+ Block plaintext tương ứng sẽ thay đổi theo
+ Không có bước xác thực nào kiểm tra sự thay đổi này.
Kết luận: CBC không đảm bảo integrity.

3. Minh họa tấn công Bit-Flipping
Giả sử hệ thống mã hóa thông điệp:
AMOUNT=000100;
Kẻ tấn công:
+ Không biết khóa AES
+ Không giải mã được nội dung
+ Nhưng có thể sửa ciphertext
Bằng cách thay đổi một số byte trong ciphertext, plaintext sau khi decrypt có thể trở thành:
AMOUNT=999999;
Hệ thống CBC-only vẫn giải mã thành công.
Không phát hiện lỗi.

4. Giải pháp: Encrypt-then-MAC (EtM)
Để ngăn chặn giả mạo, ta thực hiện:
	1. CBC encrypt plaintext
	2. Tính HMAC trên toàn bộ IV và ciphertext
	3. Gửi IV + ciphertext + MAC tag
	4. Khi nhận: verify MAC trước khi decrypt
Nếu dữ liệu bị thay đổi:
ValueError: AUTHENTICATION FAILED
EtM đảm bảo:
+ Không decrypt dữ liệu chưa được xác thực
+ Ngăn chặn bit-flipping
+ Ngăn chặn padding oracle

5. Cấu trúc dự án
practical-cbc-malleability/
	+ src/cbc_malleability/core/
	CBC, HMAC và EtM implementation

	+ src/cbc_malleability/attacks/
	Bit-flipping attack

	+ scripts/
	Demo và kịch bản thực thi

	+ tests/
	Unit tests

	+ data/
	Keys và sample packets

	+ pyproject.toml
	Python packaging chuẩn
Dự án sử dụng src-layout và có thể cài đặt bằng:
python -m pip install -e .

6. Cách chạy demo
Cài đặt:
python -m pip install -e .
Chạy Encrypt-then-MAC:
python scripts/demo_etm.py
Kết quả mẫu:
=== Encrypting with Encrypt-then-MAC ===
Saved packet: data/packets/phase3_etm.bin

=== Attempting normal decrypt ===
Decryption succeeded.

7. So sánh CBC-only và EtM
CBC-only:
+ Có confidentiality
+ Không có integrity
+ Không phát hiện giả mạo

Encrypt-then-MAC:
+ Có confidentiality
+ Có integrity
+ Phát hiện thay đổi dữ liệu
+ Tuân thủ nguyên tắc verify-before-decrypt

8. Liên hệ thực tế
Trong lịch sử, một số hệ thống TLS từng sử dụng MAC-then-Encrypt, dẫn đến các lỗ hổng padding oracle.
Ngày nay, chuẩn khuyến nghị:
+ AES-GCM
+ ChaCha20-Poly1305
+ Hoặc Encrypt-then-MAC
Dự án này minh họa lý do tại sao.

9. Bài học thiết kế
Thuật toán mạnh không đủ để đảm bảo hệ thống an toàn.

AES mạnh.
CBC phổ biến.
Nhưng nếu không có xác thực, hệ thống vẫn dễ bị tấn công.

Security phụ thuộc vào cách kết hợp các thành phần, không chỉ vào thuật toán riêng lẻ.

10. Tác giả
Author: Topdinh
GitHub: https://github.com/Topdinh