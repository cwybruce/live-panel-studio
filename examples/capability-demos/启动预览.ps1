$ErrorActionPreference = 'Stop'
$previewDir = $PSScriptRoot
$previewPort = 8779
$previewUrl = "http://127.0.0.1:$previewPort/index.html"
$previewHealthUrl = "http://127.0.0.1:$previewPort/api/health"
$previewServer = [IO.Path]::GetFullPath((Join-Path $previewDir '../../scripts/preview_server.py'))
try {
    $existing = Invoke-RestMethod -Uri $previewHealthUrl -TimeoutSec 2
    if ($existing.service -ne 'live-panel-preview' -or -not $existing.exports) { throw "端口 $previewPort 上的服务不支持视频导出。" }
} catch {
    if (Get-NetTCPConnection -LocalPort $previewPort -State Listen -ErrorAction SilentlyContinue) { throw }
    Start-Process -FilePath 'python' -ArgumentList @(('"' + $previewServer + '"'), '--port', "$previewPort", '--directory', ('"' + $previewDir + '"')) -WindowStyle Hidden
    Start-Sleep -Seconds 1
}
Start-Process $previewUrl
