# 🔋 ESP32 Auto Power Switch System

Hệ thống chuyển đổi nguồn tự động giữa Pin và Adaptor 12V dựa trên SOC (State of Charge) của pin từ Home Assistant.

## ✨ Tính năng chính

- 🔄 **Chuyển nguồn tự động**: Dựa trên SOC từ Home Assistant
- ⚙️ **Cấu hình linh hoạt**: Điều chỉnh ngưỡng từ HA interface
- 🎛️ **3 chế độ hoạt động**:
  - `Auto`: Tự động theo SOC pin
  - `Force Pin`: Bắt buộc dùng Pin
  - `Force Adaptor`: Bắt buộc dùng Adaptor  
- 📊 **Monitoring realtime**: Hiển thị trạng thái và SOC
- 🛡️ **Hysteresis logic**: Tránh dao động nguồn

## ⚙️ Cấu hình mặc định

| Thông số | Giá trị mặc định | Điều chỉnh |
|----------|------------------|------------|
| 🔌 Chuyển sang Adaptor | SOC < 50% | ✅ Từ HA (20-60%) |
| 🔋 Chuyển về Pin | SOC > 70% | ✅ Từ HA (60-90%) |
| 📡 GPIO Relay | Pin 16 | ✅ Trong code |
| 📊 SOC Entity | `sensor.jk_remaining_capacity` | ✅ Trong code |

## 📡 Yêu cầu phần cứng

- **ESP32 Dev Board**
- **Relay Module** (kết nối GPIO16)
- **MOSFET Module D4184** (điều khiển coil relay chính)
- **Nguồn 12V**: Pin + Adaptor

## 📁 Cấu trúc file

```
esp32_chuyen_nguon_12v/
├── README.md                      # File này
├── esp32_chuyen_nguon_12v.yaml   # Code chính ESP32
├── base_setup.yaml               # Setup cơ bản (WiFi, sensors, etc.)
├── .gitignore                    # Loại trừ files không cần thiết
├── flash.bat                     # Script flash code
├── log.bat                       # Script xem log
└── esare.bat                     # Script erase flash
```

## 🚀 Hướng dẫn cài đặt

### 1️⃣ Chuẩn bị môi trường
```bash
# Cài đặt ESPHome
pip install esphome

# Clone repository
git clone https://github.com/ngoviet/esp32-chuyen-nguon-12v.git
cd esp32-chuyen-nguon-12v
```

### 2️⃣ Cấu hình WiFi và bảo mật
```bash
# Tạo file secrets từ template
cp secrets.yaml.example secrets.yaml
```

Sửa file `secrets.yaml`:
```yaml
# WiFi của bạn
wifi_ssid: "TEN_WIFI_CUA_BAN"
wifi_password: "MAT_KHAU_WIFI"

# Mật khẩu OTA
ota_password: "mat_khau_ota_tuy_chon"
```

> ⚠️ **Quan trọng**: File `secrets.yaml` chỉ tồn tại local, KHÔNG bao giờ được push lên GitHub!

### 3️⃣ Tùy chỉnh cấu hình
- **SOC Entity**: Sửa `battery_soc_entity` trong `substitutions` nếu khác `sensor.jk_remaining_capacity`
- **GPIO Pin**: Sửa `relay_pin` nếu khác GPIO16
- **Ngưỡng SOC**: Sửa `soc_switch_to_adapter_default` và `soc_switch_to_battery_default`

### 4️⃣ Flash firmware lên ESP32
```bash
# Cách 1: ESPHome CLI
esphome run esp32_chuyen_nguon_12v.yaml

# Cách 2: Script Windows
flash.bat

# Cách 3: ESPHome Dashboard
esphome dashboard esp32_chuyen_nguon_12v.yaml
```

## 🔄 Logic hoạt động

### Chế độ Auto
```
SOC < 50% → Chuyển sang Adaptor (sạc pin)
50% ≤ SOC ≤ 70% → Giữ nguyên trạng thái (hysteresis)
SOC > 70% → Chuyển về Pin (ưu tiên pin)
```

### Chế độ Manual
- **Force Pin**: Luôn dùng pin (bỏ qua SOC)
- **Force Adaptor**: Luôn dùng adaptor (bỏ qua SOC)

## 🏠 Home Assistant Integration

Sau khi flash thành công, ESP32 sẽ tự động xuất hiện trong HA với các entity:

### 🎛️ Điều khiển
- **`select.che_do_chuyen_nguon`**: Chọn Auto/Force Pin/Force Adaptor
- **`number.nguong_chuyen_sang_adaptor`**: Ngưỡng chuyển Adaptor (20-60%)  
- **`number.nguong_chuyen_ve_pin`**: Ngưỡng chuyển Pin (60-90%)

### 📊 Monitoring  
- **`sensor.battery_soc_tu_ha`**: SOC đồng bộ từ HA
- **`binary_sensor.dang_dung_adaptor`**: Trạng thái nguồn hiện tại
- **`sensor.trang_thai_soc`**: Mô tả chi tiết trạng thái SOC

## � Troubleshooting

### 🚫 Không nhận SOC từ HA
1. ✅ Kiểm tra entity `sensor.jk_remaining_capacity` tồn tại
2. ✅ ESP32 đã kết nối API với HA  
3. ✅ Xem log: `esphome logs esp32_chuyen_nguon_12v.yaml`

### ⚡ Relay không hoạt động
1. ✅ Kiểm tra kết nối GPIO16 → Relay IN
2. ✅ Kiểm tra nguồn 3.3V cho relay module
3. ✅ Test bằng chế độ "Force Manual"

### 📡 WiFi không kết nối  
1. ✅ Kiểm tra `secrets.yaml` - SSID/password đúng chưa
2. ✅ Đảm bảo ESP32 trong vùng phủ sóng WiFi
3. ✅ Xem log: `esphome logs esp32_chuyen_nguon_12v.yaml`

### 🔄 SOC không cập nhật
1. ✅ Entity `sensor.jk_remaining_capacity` có dữ liệu trong HA
2. ✅ ESP32 đã được add vào HA qua ESPHome integration  
3. ✅ Kiểm tra Home Assistant API token

## 📝 License

MIT License - Sử dụng tự do cho các dự án cá nhân và thương mại.

## 🤝 Contributing

Mọi đóng góp đều được chào đón! Vui lòng tạo Issue hoặc Pull Request.

## 📧 Support

Nếu gặp vấn đề, vui lòng tạo Issue trên GitHub repository này.

---

<!-- support:start -->
## Support the project

<p align="center">
  <img src="https://raw.githubusercontent.com/ngoviet/.github/main/assets/support/banner.svg" width="720" alt="Built and maintained by one person in Việt Nam">
</p>

<p align="center">
  <a href="https://buymeacoffee.com/ngoviet"><img src="https://raw.githubusercontent.com/ngoviet/.github/main/assets/support/btn-coffee.svg" height="56" alt="Buy me a coffee"></a>
  &nbsp;
  <a href="https://github.com/sponsors/ngoviet"><img src="https://raw.githubusercontent.com/ngoviet/.github/main/assets/support/btn-sponsors.svg" height="56" alt="GitHub Sponsors"></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/ngoviet/.github/main/assets/support/vietqr-card.svg" width="300" alt="VietQR — MB Bank — NGO DUC VIET — 911051212">
</p>

<p align="center"><sub>🇻🇳 VietQR: quét bằng app ngân hàng bất kỳ, nội dung <code>Ung ho esp32-auto-power-switch-12v</code>. Cảm ơn bạn! · Thank you for keeping this project alive.</sub></p>
<!-- support:end -->
