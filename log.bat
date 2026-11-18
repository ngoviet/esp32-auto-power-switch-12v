@echo off
REM Xem log. Mac dinh qua mang; qua USB:  log.bat COM12
cd /d "%~dp0"
set DEVICE=%1
if "%DEVICE%"=="" set DEVICE=192.168.20.171
esphome logs esp32_chuyen_nguon_12v.yaml --device %DEVICE%
pause
