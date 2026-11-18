"""Tạo secrets.yaml giả cho CI từ đúng danh sách khoá trong secrets.yaml.example.

YAML dùng một !secret mà mẫu chưa có thì `esphome config` báo thiếu khoá:
CI bắt được việc quên cập nhật secrets.yaml.example.

Dùng: python .github/scripts/secrets_gia.py <đường dẫn ra>
Không ghi đè tệp đã có, để không xoá nhầm secrets.yaml thật trên máy.
"""

import base64
import os
import pathlib
import re
import sys

if len(sys.argv) != 2:
    print("dung: secrets_gia.py <duong dan ra>", file=sys.stderr)
    sys.exit(2)

src = pathlib.Path(__file__).resolve().parents[2] / "secrets.yaml.example"
dst = pathlib.Path(sys.argv[1])
if dst.exists():
    print(f"loi: {dst} da ton tai, khong ghi de", file=sys.stderr)
    sys.exit(1)

keys = [m.group(1) for line in src.read_text(encoding="utf-8").splitlines() if (m := re.match(r"^(\w+):", line))]
if not keys:
    print(f"loi: {src} khong co khoa nao", file=sys.stderr)
    sys.exit(1)

lines = []
for key in keys:
    # Khoá API phải là 32 byte base64; các khoá khác chỉ cần đủ 8 ký tự.
    value = base64.b64encode(os.urandom(32)).decode() if key == "api_encryption_key" else f"ci-placeholder-{key}"
    lines.append(f'{key}: "{value}"')
dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"secrets gia: {len(keys)} khoa ({', '.join(keys)})")
