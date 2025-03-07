@echo off
echo Limpando arquivos .out...
del *.out /Q

echo Limpando arquivos .log...
del *.log /Q

echo Executando main.py...
python3 .\main.py

pause
