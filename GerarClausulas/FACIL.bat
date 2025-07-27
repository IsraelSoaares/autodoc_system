@echo off
cls
echo ==========================================
echo     AutoDoc AI - ACESSO SUPER FACIL
echo ==========================================
echo.

echo 🚀 Iniciando servidor...
start /B streamlit run app_interface.py --server.port 8501

echo ⏳ Aguardando 10 segundos...
timeout /t 10 /nobreak >nul

echo.
echo 🌐 Gerando link publico...
echo 📱 COPIE O LINK QUE APARECER:
echo.

lt --port 8501
