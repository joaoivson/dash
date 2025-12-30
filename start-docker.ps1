# Script para iniciar Docker Desktop no Windows

Write-Host "🐳 Tentando iniciar Docker Desktop..." -ForegroundColor Cyan

# Verifica se Docker Desktop está instalado
$dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
if (Test-Path $dockerPath) {
    Write-Host "✅ Docker Desktop encontrado" -ForegroundColor Green
    Write-Host "🚀 Iniciando Docker Desktop..." -ForegroundColor Yellow
    
    Start-Process $dockerPath
    
    Write-Host ""
    Write-Host "⏳ Aguarde alguns segundos para o Docker Desktop iniciar..." -ForegroundColor Yellow
    Write-Host "   (O ícone na bandeja do sistema ficará verde quando estiver pronto)" -ForegroundColor Gray
    Write-Host ""
    
    # Aguarda até 60 segundos
    $timeout = 60
    $elapsed = 0
    $interval = 2
    
    while ($elapsed -lt $timeout) {
        Start-Sleep -Seconds $interval
        $elapsed += $interval
        
        try {
            docker info | Out-Null
            Write-Host "✅ Docker Desktop está rodando!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🚀 Agora você pode executar: docker compose up" -ForegroundColor Yellow
            exit 0
        } catch {
            Write-Host "   Aguardando... ($elapsed/$timeout segundos)" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    Write-Host "⚠️  Docker Desktop pode estar ainda iniciando..." -ForegroundColor Yellow
    Write-Host "   Verifique manualmente se o ícone está verde na bandeja do sistema" -ForegroundColor Gray
    Write-Host "   Depois execute: docker compose up" -ForegroundColor White
    
} else {
    Write-Host "❌ Docker Desktop não encontrado em: $dockerPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 Instale o Docker Desktop:" -ForegroundColor Yellow
    Write-Host "   https://www.docker.com/products/docker-desktop/" -ForegroundColor Cyan
}

