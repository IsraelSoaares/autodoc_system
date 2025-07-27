@echo off
cls
echo ==========================================
echo      FECHAR SERVIDOR - AutoDoc AI
echo ==========================================
echo.

echo 🔍 Procurando processos do Streamlit...
tasklist | findstr streamlit
tasklist | findstr python

echo.
echo 🛑 METODOS PARA FECHAR:
echo.
echo [1] Ctrl + C no terminal onde roda
echo [2] Fechar a janela do terminal  
echo [3] Matar processos automaticamente
echo.

set /p escolha="Escolha (1/2/3): "

if "%escolha%"=="3" goto matar

echo.
echo ✅ Use Ctrl+C no terminal ou feche a janela!
goto fim

:matar
echo.
echo 🛑 Matando processos do Streamlit...
taskkill /f /im streamlit.exe 2>nul
taskkill /f /im python.exe /fi "WINDOWTITLE eq *streamlit*" 2>nul

echo ✅ Processos encerrados!

:fim
pause
