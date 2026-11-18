@echo off
REM Nap firmware. Mac dinh qua mang (OTA) toi IP ben duoi.
REM Nap lan dau hoac khi OTA loi: cam USB roi chay  flash.bat COM12
cd /d "%~dp0"
set DEVICE=%1
if "%DEVICE%"=="" set DEVICE=192.168.20.171
esphome run esp32_chuyen_nguon_12v.yaml --device %DEVICE%
pause
