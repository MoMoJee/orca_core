@echo off
echo 🔧 ORCA快速重置工具
echo ==================

echo 1. 关闭可能冲突的程序...
taskkill /f /im "DynamixelWizard2.exe" 2>nul
taskkill /f /im "python.exe" 2>nul

echo 2. 等待资源释放...
timeout /t 3 /nobreak >nul

echo 3. 重新插拔提示...
echo 💡 请重新插拔U2D2的USB线
echo 💡 等待3秒后按任意键继续...
pause

echo ✅ 重置完成！现在可以运行ORCA脚本了
