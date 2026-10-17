$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendLog = Join-Path $root 'backend.log'
$frontendLog = Join-Path $root 'frontend.log'

$backendArgs = @(
    '-m',
    'uvicorn',
    'backend.main:app',
    '--host',
    '0.0.0.0',
    '--port',
    '8000'
)

$frontendArgs = @(
    '-m',
    'http.server',
    '8001'
)

$venvPython = Join-Path $root 'venv\Scripts\python.exe'

if (-not (Test-Path $venvPython)) {
    Write-Error 'Virtual environment not found. Please create it first.'
    exit 1
}

Start-Process -FilePath $venvPython -ArgumentList $backendArgs -WorkingDirectory $root -RedirectStandardOutput $backendLog -RedirectStandardError $backendLog
Start-Process -FilePath $venvPython -ArgumentList $frontendArgs -WorkingDirectory (Join-Path $root 'frontend') -RedirectStandardOutput $frontendLog -RedirectStandardError $frontendLog

Write-Host 'Backend started on http://localhost:8000'
Write-Host 'Frontend started on http://localhost:8001'
Write-Host 'Logs:'
Write-Host "  Backend: $backendLog"
Write-Host "  Frontend: $frontendLog"
