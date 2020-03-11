@echo off
set var = 0
rem ** 该代码由【kangour Aronld】贡献，并授予网友使用和传播的权利，但请保留此部分内容声明。
rem ** 使用本代码前，请确保.py文件与.bat文件的命名一致。
rem ** 例如，我们用【love】给文件命名，那么只有当bat文件名为【love.bat】py文件为【love.py】时，双击love.bat文件，才能准确执行到love.py程序。
rem ** kangour Aronld 写于2017年12月4日
rem **
cls
rem ** 打印提示信息
@echo --- Runner %date% %time% the python result %~dp0 ---
@echo.
rem ** 获取当前目录路径
cd %~dp0
rem ** 获取当前bat文件名（前缀部分）
for /f "delims=" %%i in ("%0") do set aa=%%~ni
set "aa=%aa%.py"
rem ** 调用Python解释器执行
python %aa%
echo.
echo.
echo.
pause