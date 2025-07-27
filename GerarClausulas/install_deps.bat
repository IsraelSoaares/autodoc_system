@echo off
echo 🤖 AutoDoc AI - Instalador de Dependências
echo ==========================================

echo.
echo Escolha o tipo de instalação:
echo.
echo 1. 🚀 Instalação Básica (Interface Desktop + API)
echo 2. 🌐 Instalação Web (+ Streamlit)
echo 3. 🎤 Instalação Completa (+ Whisper para transcrição)
echo 4. 📦 Instalação Mínima (apenas requests)
echo.

set /p choice="Digite sua escolha (1-4): "

if "%choice%"=="1" goto basic
if "%choice%"=="2" goto web
if "%choice%"=="3" goto complete
if "%choice%"=="4" goto minimal
goto invalid

:basic
echo.
echo 🚀 Instalando dependências básicas...
pip install -r requirements.txt
goto end

:web
echo.
echo 🌐 Instalando dependências básicas + web...
pip install -r requirements.txt
pip install streamlit plotly
goto end

:complete
echo.
echo 🎤 Instalação completa (pode demorar)...
pip install -r requirements_interface.txt
goto end

:minimal
echo.
echo 📦 Instalação mínima...
pip install requests python-dotenv
goto end

:invalid
echo ❌ Opção inválida!
goto end

:end
echo.
echo ✅ Instalação concluída!
echo.
echo 🚀 Para executar:
echo    python app_tkinter.py    (Interface Desktop)
echo    python main.py           (Menu Principal)
echo.
pause
