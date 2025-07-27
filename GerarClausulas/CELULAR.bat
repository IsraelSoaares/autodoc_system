@echo off
cls
echo =================echo 🚀 Iniciando servidor...
start /B streamlit run app_interface.py --server.port 8501 --server.address 127.0.0.1
timeout /t 10 /nobreak >nul
echo.
echo 📱 COPIE O LINK QUE APARECER ABAIXO:
echo.

if "%senha%"=="" (
    npx localtunnel --port 8501
) else (
    npx localtunnel --port 8501 --subdomain %senha%
)================
echo       AutoDoc AI - SOLUCAO DEFINITIVA
echo =============================================
echo.

echo 🎯 ESCOLHA SEU METODO:
echo.
echo [1] LOCAL  - Mesma WiFi (192.168.0.34:8501)  
echo [2] GLOBAL - Link publico (funciona em qualquer lugar)
echo.

set /p escolha="Digite 1 ou 2: "

if "%escolha%"=="1" goto local
if "%escolha%"=="2" goto global

:local
cls
echo 📱 ACESSO LOCAL - MESMA WIFI
echo =============================
echo.
echo No celular digite: http://192.168.0.34:8501
echo.
streamlit run app_interface.py --server.address 0.0.0.0 --server.port 8501
goto fim

:global
cls
echo 🌍 ACESSO GLOBAL - QUALQUER LUGAR  
echo ===============================
echo.
echo ⚠️  Instale primeiro: npm install -g localtunnel
echo.
echo � Defina uma senha (ou Enter para sem senha):
set /p senha="Senha (opcional): "

echo �🚀 Iniciando...
start /B streamlit run app_interface.py --server.port 8501
timeout /t 8 /nobreak >nul
echo.
echo 📱 COPIE O LINK QUE APARECER ABAIXO:
echo.

if "%senha%"=="" (
    npx localtunnel --port 8501
) else (
    npx localtunnel --port 8501 --subdomain %senha%
)
goto fim

:fim
pause
