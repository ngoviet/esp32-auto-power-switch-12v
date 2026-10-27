# ESP32 Auto Power Switch 12V

<!-- readme-axi type=esp32 -->

**English** · [Tiếng Việt](README.vi.md)

An **ESPHome** firmware for an **ESP32 Dev Board** that switches a 12 V load automatically between
a **battery** and a **12 V adaptor**, based on the battery's **SOC (State of Charge)** read from
**Home Assistant**. A relay on GPIO16, driven through a D4184 MOSFET module, flips the main power
relay; thresholds and the operating mode are adjustable from Home Assistant.

> 🇻🇳 Built and maintained by one person in Việt Nam — if it saves you time, please
> [support the project](#support-the-project).

## Contents

- [Features](#features)
- [Hardware](#hardware)
- [Quick start](#quick-start)
- [Configuration](#configuration)
- [How it works](#how-it-works)
- [Home Assistant](#home-assistant)
- [Troubleshooting](#troubleshooting)
- [Project layout](#project-layout)
- [Development](#development)

## Features

- **Automatic power switching**: based on the SOC from Home Assistant
- **Flexible configuration**: adjust the thresholds from the HA interface
- **3 operating modes**:
  - `Auto`: follows the battery SOC automatically
  - `Force Pin`: always use the battery
  - `Force Adaptor`: always use the adaptor
- **Realtime monitoring**: shows the current state and SOC
- **Hysteresis logic**: prevents the power source from flapping

## Hardware

- **ESP32 Dev Board**
- **Relay Module** (connected to GPIO16)
- **MOSFET Module D4184** (drives the coil of the main relay)
- **12V power**: Battery + Adaptor

## Quick start

### 1. Prepare the environment

```bash
# Install ESPHome
pip install esphome

# Clone repository
git clone https://github.com/ngoviet/esp32-auto-power-switch-12v.git
cd esp32-auto-power-switch-12v
```

### 2. Configure WiFi and security

```bash
# Create the secrets file from the template
cp secrets.yaml.example secrets.yaml
```

Edit `secrets.yaml`:

```yaml
# Your WiFi
wifi_ssid: "TEN_WIFI_CUA_BAN"
wifi_password: "MAT_KHAU_WIFI"

# OTA password
ota_password: "mat_khau_ota_tuy_chon"
```

> ⚠️ **Important**: `secrets.yaml` exists only locally and must NEVER be pushed to GitHub!

### 3. Customise the configuration

- **SOC Entity**: change `battery_soc_entity` in `substitutions` if it is not `sensor.jk_remaining_capacity`
- **GPIO Pin**: change `relay_pin` if it is not GPIO16
- **SOC thresholds**: change `soc_switch_to_adapter_default` and `soc_switch_to_battery_default`

### 4. Flash the firmware to the ESP32

```bash
# Option 1: ESPHome CLI
esphome run esp32_chuyen_nguon_12v.yaml

# Option 2: Windows script
flash.bat

# Option 3: ESPHome Dashboard
esphome dashboard esp32_chuyen_nguon_12v.yaml
```

## Configuration

Default settings:

| Setting | Default value | Adjustable |
|----------|------------------|------------|
| Switch to Adaptor | SOC < 50% | ✅ From HA (20-60%) |
| Switch back to Battery | SOC > 70% | ✅ From HA (60-90%) |
| GPIO Relay | Pin 16 | ✅ In code |
| SOC Entity | `sensor.jk_remaining_capacity` | ✅ In code |

## How it works

### Auto mode

```
SOC < 50% → Switch to Adaptor (charge the battery)
50% ≤ SOC ≤ 70% → Keep the current state (hysteresis)
SOC > 70% → Switch back to Battery (battery preferred)
```

### Manual mode

- **Force Pin**: always use the battery (ignores SOC)
- **Force Adaptor**: always use the adaptor (ignores SOC)

## Home Assistant

After a successful flash, the ESP32 appears in HA automatically with these entities:

### Controls

- **`select.che_do_chuyen_nguon`**: choose Auto / Force Pin / Force Adaptor
- **`number.nguong_chuyen_sang_adaptor`**: threshold for switching to the Adaptor (20-60%)
- **`number.nguong_chuyen_ve_pin`**: threshold for switching back to the Battery (60-90%)

### Monitoring

- **`sensor.battery_soc_tu_ha`**: SOC synced from HA
- **`binary_sensor.dang_dung_adaptor`**: current power source
- **`sensor.trang_thai_soc`**: detailed description of the SOC state

## Troubleshooting

### No SOC received from HA

1. Check that the entity `sensor.jk_remaining_capacity` exists
2. Check that the ESP32 is connected to HA over the API
3. View the log: `esphome logs esp32_chuyen_nguon_12v.yaml`

### Relay does not work

1. Check the wiring GPIO16 → Relay IN
2. Check the 3.3V supply to the relay module
3. Test with the "Force Manual" mode

### WiFi does not connect

1. Check `secrets.yaml` — are the SSID/password correct?
2. Make sure the ESP32 is within WiFi range
3. View the log: `esphome logs esp32_chuyen_nguon_12v.yaml`

### SOC does not update

1. The entity `sensor.jk_remaining_capacity` has data in HA
2. The ESP32 has been added to HA through the ESPHome integration
3. Check the Home Assistant API token

### Getting help

If you run into a problem, please open an
[issue](https://github.com/ngoviet/esp32-auto-power-switch-12v/issues) on this GitHub repository.

## Project layout

```
esp32_chuyen_nguon_12v/
├── README.md                      # This file
├── esp32_chuyen_nguon_12v.yaml   # Main ESP32 code
├── base_setup.yaml               # Basic setup (WiFi, sensors, etc.)
├── .gitignore                    # Excludes unneeded files
├── flash.bat                     # Flash script
├── log.bat                       # Log viewer script
└── esare.bat                     # Flash erase script
```

## Development

### Contributing

All contributions are welcome! Please open an Issue or a Pull Request.

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

<p align="center"><sub>🇻🇳 VietQR: scan with any Vietnamese banking app, transfer note <code>Ung ho esp32-auto-power-switch-12v</code>. Thank you for keeping this project alive!</sub></p>
<p align="center"><sub>Crypto (BEP20 network): <code>0x57f07d44fb581cddc028a0c67d63a8cc05aa6caa</code> · USDT · USDC · BNB · ETH · BTC</sub></p>
<!-- support:end -->

## License

[MIT](LICENSE) © Ngô Đức Việt.
