@echo off
echo 清理临时文件...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
rmdir /s /q __pycache__ 2>nul
del /f /q *.pyc 2>nul
del /f /q *.pyo 2>nul
del /f /q *.pyd 2>nul
echo 清理完成！ 