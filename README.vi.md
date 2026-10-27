# ESP32 chuyển nguồn tự động 12V

<!-- readme-axi type=esp32 -->

[English](README.md) · **Tiếng Việt**

Firmware **ESPHome** cho **ESP32 Dev Board**, tự động chuyển nguồn 12V cho tải giữa **Pin** và
**Adaptor 12V** dựa trên **SOC (State of Charge)** của pin lấy từ **Home Assistant**. Relay ở
GPIO16, qua module MOSFET D4184, đóng/ngắt relay nguồn chính; ngưỡng và chế độ hoạt động chỉnh
được ngay trên Home Assistant.

> 🇻🇳 Dự án do một người Việt tự xây dựng và duy trì — nếu nó giúp ích cho bạn, hãy
> [ủng hộ dự án](#ủng-hộ-dự-án).

## Mục lục

- [Tính năng](#tính-năng)
- [Phần cứng](#phần-cứng)
- [Bắt đầu nhanh](#bắt-đầu-nhanh)
- [Cấu hình](#cấu-hình)
- [Cách hoạt động](#cách-hoạt-động)
- [Home Assistant](#home-assistant)
- [Xử lý sự cố](#xử-lý-sự-cố)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Phát triển](#phát-triển)

## Tính năng

- **Chuyển nguồn tự động**: Dựa trên SOC từ Home Assistant
- **Cấu hình linh hoạt**: Điều chỉnh ngưỡng từ HA interface
- **3 chế độ hoạt động**:
  - `Auto`: Tự động theo SOC pin
  - `Force Pin`: Bắt buộc dùng Pin
  - `Force Adaptor`: Bắt buộc dùng Adaptor
- **Monitoring realtime**: Hiển thị trạng thái và SOC
- **Hysteresis logic**: Tránh dao động nguồn

## Phần cứng

- **ESP32 Dev Board**
- **Relay Module** (kết nối GPIO16)
- **MOSFET Module D4184** (điều khiển coil relay chính)
- **Nguồn 12V**: Pin + Adaptor

## Bắt đầu nhanh

### 1. Chuẩn bị môi trường

```bash
# Cài đặt ESPHome
pip install esphome

# Clone repository
git clone https://github.com/ngoviet/esp32-auto-power-switch-12v.git
cd esp32-auto-power-switch-12v
```

### 2. Cấu hình WiFi và bảo mật

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

### 3. Tùy chỉnh cấu hình

- **SOC Entity**: Sửa `battery_soc_entity` trong `substitutions` nếu khác `sensor.jk_remaining_capacity`
- **GPIO Pin**: Sửa `relay_pin` nếu khác GPIO16
- **Ngưỡng SOC**: Sửa `soc_switch_to_adapter_default` và `soc_switch_to_battery_default`

### 4. Flash firmware lên ESP32

```bash
# Cách 1: ESPHome CLI
esphome run esp32_chuyen_nguon_12v.yaml

# Cách 2: Script Windows
flash.bat

# Cách 3: ESPHome Dashboard
esphome dashboard esp32_chuyen_nguon_12v.yaml
```

## Cấu hình

Cấu hình mặc định:

| Thông số | Giá trị mặc định | Điều chỉnh |
|----------|------------------|------------|
| Chuyển sang Adaptor | SOC < 50% | ✅ Từ HA (20-60%) |
| Chuyển về Pin | SOC > 70% | ✅ Từ HA (60-90%) |
| GPIO Relay | Pin 16 | ✅ Trong code |
| SOC Entity | `sensor.jk_remaining_capacity` | ✅ Trong code |

## Cách hoạt động

### Chế độ Auto

```
SOC < 50% → Chuyển sang Adaptor (sạc pin)
50% ≤ SOC ≤ 70% → Giữ nguyên trạng thái (hysteresis)
SOC > 70% → Chuyển về Pin (ưu tiên pin)
```

### Chế độ Manual

- **Force Pin**: Luôn dùng pin (bỏ qua SOC)
- **Force Adaptor**: Luôn dùng adaptor (bỏ qua SOC)

## Home Assistant

Sau khi flash thành công, ESP32 sẽ tự động xuất hiện trong HA với các entity:

### Điều khiển

- **`select.che_do_chuyen_nguon`**: Chọn Auto/Force Pin/Force Adaptor
- **`number.nguong_chuyen_sang_adaptor`**: Ngưỡng chuyển Adaptor (20-60%)
- **`number.nguong_chuyen_ve_pin`**: Ngưỡng chuyển Pin (60-90%)

### Giám sát

- **`sensor.battery_soc_tu_ha`**: SOC đồng bộ từ HA
- **`binary_sensor.dang_dung_adaptor`**: Trạng thái nguồn hiện tại
- **`sensor.trang_thai_soc`**: Mô tả chi tiết trạng thái SOC

## Xử lý sự cố

### Không nhận SOC từ HA

1. Kiểm tra entity `sensor.jk_remaining_capacity` tồn tại
2. ESP32 đã kết nối API với HA
3. Xem log: `esphome logs esp32_chuyen_nguon_12v.yaml`

### Relay không hoạt động

1. Kiểm tra kết nối GPIO16 → Relay IN
2. Kiểm tra nguồn 3.3V cho relay module
3. Test bằng chế độ "Force Manual"

### WiFi không kết nối

1. Kiểm tra `secrets.yaml` - SSID/password đúng chưa
2. Đảm bảo ESP32 trong vùng phủ sóng WiFi
3. Xem log: `esphome logs esp32_chuyen_nguon_12v.yaml`

### SOC không cập nhật

1. Entity `sensor.jk_remaining_capacity` có dữ liệu trong HA
2. ESP32 đã được add vào HA qua ESPHome integration
3. Kiểm tra Home Assistant API token

### Cần hỗ trợ

Nếu gặp vấn đề, vui lòng tạo
[Issue](https://github.com/ngoviet/esp32-auto-power-switch-12v/issues) trên GitHub repository này.

## Cấu trúc dự án

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

## Phát triển

### Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng tạo Issue hoặc Pull Request.

<!-- support:start -->
## Ủng hộ dự án

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

<p align="center"><sub>🇻🇳 VietQR: quét bằng app ngân hàng bất kỳ, nội dung <code>Ung ho esp32-auto-power-switch-12v</code>. Cảm ơn bạn đã giúp dự án tiếp tục phát triển!</sub></p>
<p align="center"><sub>Tiền mã hoá (mạng BEP20): <code>0xcbf0402b232cb24b4d998f09a4884f87b5f74750</code> · USDT · USDC · BNB · ETH · BTC</sub></p>
<!-- support:end -->

## Giấy phép

[MIT](LICENSE) © Ngô Đức Việt.
