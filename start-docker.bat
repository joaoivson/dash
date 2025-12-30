@echo off
echo 🐳 Iniciando Docker Desktop...
echo.

REM Verifica se Docker Desktop existe
if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
    echo ✅ Docker Desktop encontrado
    echo 🚀 Iniciando...
    echo.
    
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    echo ⏳ Aguarde alguns segundos para o Docker Desktop iniciar...
    echo    (O ícone na bandeja do sistema ficará verde quando estiver pronto)
    echo.
    echo 💡 Dica: Aguarde até o ícone do Docker ficar verde na bandeja do sistema
    echo    Depois execute: docker compose up
    echo.
    
    timeout /t 5 /nobreak >nul
    
    echo 🔍 Verificando status...
    docker info >nul 2>&1
    if %errorlevel% == 0 (
        echo ✅ Docker Desktop está rodando!
        echo.
        echo 🚀 Agora você pode executar: docker compose up
    ) else (
        echo ⚠️  Docker Desktop ainda está iniciando...
        echo    Aguarde mais alguns segundos e verifique o ícone na bandeja do sistema
    )
) else (
    echo ❌ Docker Desktop não encontrado!
    echo.
    echo 📥 Instale o Docker Desktop:
    echo    https://www.docker.com/products/docker-desktop/
)

pause

