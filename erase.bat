@echo off
REM Xoa sach flash ESP32 qua USB (mat ca trang thai da luu). Cong khac:  erase.bat COM5
set PORT=%1
if "%PORT%"=="" set PORT=COM12
esptool --chip esp32 --port %PORT% erase-flash
pause
