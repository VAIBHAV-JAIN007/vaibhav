$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
function Say($Message) { Write-Host ""; Write-Host "== $Message ==" -ForegroundColor Cyan }
function Check($Name, $Ok, $Detail = "") {
  if ($Ok) { Write-Host "[PASS] $Name $Detail" -ForegroundColor Green }
  else { Write-Host "[FAIL] $Name $Detail" -ForegroundColor Red; $script:Failures++ }
}
$script:Failures = 0
$Warnings = 0
Say "Prerequisites"
foreach ($cmd in @("git","docker","node","npm","py")) {
  $found = Get-Command $cmd -ErrorAction SilentlyContinue
  Check "Command $cmd" ($null -ne $found)
}
if ($Failures -gt 0) { throw "Install Git, Docker Desktop, Node.js 20+, and Python 3.11+; then rerun." }
docker info *> $null
Check "Docker Engine running" ($LASTEXITCODE -eq 0)
if ($Failures -gt 0) { throw "Start Docker Desktop and rerun this script." }

Say "Create secure local environment"
if (!(Test-Path ".env")) {
  $bytes = New-Object byte[] 48
  $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create(); $rng.GetBytes($bytes)
  $jwt = [Convert]::ToBase64String($bytes).Replace("+","-").Replace("/","_").TrimEnd("=")
  $bytes2 = New-Object byte[] 32
  $rng.GetBytes($bytes2); $rng.Dispose()
  $db = [Convert]::ToBase64String($bytes2).Replace("+","-").Replace("/","_").TrimEnd("=")
  @("POSTGRES_PASSWORD=$db","JWT_SECRET=$jwt","CORS_ORIGINS=http://localhost:8000,http://localhost:8080,https://vaibhav-jain007.github.io") | Set-Content -Encoding ascii ".env"
  Write-Host "[PASS] Created .env with random local secrets" -ForegroundColor Green
} else {
  Write-Host "[INFO] Existing .env retained; verify secrets are not placeholders." -ForegroundColor Yellow
}

Say "Build and start PostgreSQL + FastAPI"
docker compose up --build -d
if ($LASTEXITCODE -ne 0) { throw "docker compose failed. Run: docker compose logs --tail=100" }
$apiReady = $false
for ($i=0; $i -lt 45; $i++) {
  try {
    $health = Invoke-RestMethod "http://localhost:8000/health" -TimeoutSec 3
    if ($health.status -eq "ok") { $apiReady = $true; break }
  } catch { Start-Sleep -Seconds 2 }
}
Check "FastAPI health endpoint" $apiReady
if (!$apiReady) { docker compose logs --tail=100; throw "API did not become healthy." }
try {
  $coverage = Invoke-RestMethod "http://localhost:8000/api/v1/market/coverage" -TimeoutSec 10
  Check "Market coverage endpoint" ($null -ne $coverage.crypto -and $null -ne $coverage.india_equities -and $null -ne $coverage.us_equities)
} catch { Check "Market coverage endpoint" $false $_.Exception.Message }

Say "Frontend unit tests"
npm test
Check "Frontend unit tests" ($LASTEXITCODE -eq 0)
npm run check
Check "Frontend JavaScript syntax checks" ($LASTEXITCODE -eq 0)

Say "Backend unit tests"
if (!(Test-Path ".venv")) { py -3 -m venv .venv }
$Py = Join-Path $Root ".venv\Scripts\python.exe"
& $Py -m pip install --disable-pip-version-check -r backend/requirements.txt
Check "Backend dependencies installed" ($LASTEXITCODE -eq 0)
if ($Failures -eq 0) {
  & $Py -m pytest backend/tests -q
  Check "Backend pytest suite" ($LASTEXITCODE -eq 0)
}

Say "Start frontend static server"
try {
  $front = Invoke-WebRequest "http://localhost:8080" -TimeoutSec 3 -UseBasicParsing
  Check "Frontend already responds on port 8080" ($front.StatusCode -eq 200)
} catch {
  $server = Start-Process -FilePath "py" -ArgumentList "-m","http.server","8080" -WorkingDirectory $Root -WindowStyle Hidden -PassThru
  Start-Sleep -Seconds 2
  try { $front = Invoke-WebRequest "http://localhost:8080" -TimeoutSec 5 -UseBasicParsing; Check "Frontend HTTP server" ($front.StatusCode -eq 200) }
  catch { Check "Frontend HTTP server" $false $_.Exception.Message }
}

Say "Live provider smoke tests (network/provider dependent)"
$checks = @(
  @{Name="Binance crypto candles"; Url="http://localhost:8000/api/v1/market/crypto/klines?symbol=BTCUSDT&interval=1h&limit=5"},
  @{Name="US equity chart adapter"; Url="http://localhost:8000/api/v1/market/equities/chart?market=US&symbol=AAPL&range=1mo&interval=1d"},
  @{Name="NSE equity chart adapter"; Url="http://localhost:8000/api/v1/market/equities/chart?market=NSE&symbol=RELIANCE&range=1mo&interval=1d"},
  @{Name="Experimental options endpoint"; Url="http://localhost:8000/api/v1/market/options/AAPL"}
)
foreach ($item in $checks) {
  try {
    $result = Invoke-RestMethod $item.Url -TimeoutSec 20
    Check $item.Name ($null -ne $result)
  } catch {
    $Warnings++
    Write-Host "[WARN] $($item.Name): provider/network returned no usable response: $($_.Exception.Message)" -ForegroundColor Yellow
  }
}

Say "Run summary"
docker compose ps
if ($Failures -gt 0) {
  Write-Host "$Failures check(s) failed; $Warnings provider warning(s)." -ForegroundColor Red
  exit 1
}
Write-Host "Local stack and automated tests passed. Provider warnings: $Warnings." -ForegroundColor Green
Write-Host "Frontend: http://localhost:8080"
Write-Host "API docs: http://localhost:8000/docs"
Write-Host "Health: http://localhost:8000/health"
Write-Host "To stop backend/database: docker compose down"
