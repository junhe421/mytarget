@echo off
echo 开始打包程序...

REM 清理旧文件
call clean.bat

REM 设置环境变量
set PYTHONOPTIMIZE=2
set PYTHONDONTWRITEBYTECODE=1

REM 使用cx_Freeze打包
python setup.py build

REM 复制文件到dist目录
if not exist dist mkdir dist
xcopy /y /e build\exe.win-amd64-3.10\* dist\
rmdir /s /q build

echo 打包完成！
pause 