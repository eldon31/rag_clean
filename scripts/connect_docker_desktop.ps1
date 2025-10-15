# Connect Docker Desktop to DigitalOcean
param([string]$DropletIP = "146.190.96.193", [string]$User = "root")
Write-Host "Connecting to DigitalOcean Docker..." -ForegroundColor Cyan
Write-Host "Step 1: Testing SSH..." -ForegroundColor Yellow
ssh "$User@$DropletIP" "docker --version"
Write-Host "Step 2: Creating SSH tunnel..." -ForegroundColor Yellow
Start-Job -ScriptBlock { param($u,$ip) & ssh -N -L 23750:/var/run/docker.sock "$u@$ip" } -ArgumentList $User,$DropletIP
Start-Sleep 3
Write-Host "Step 3: Creating Docker context..." -ForegroundColor Yellow
docker context ls --format "{{.Name}}" | Where-Object { $_ -eq "digitalocean" } | ForEach-Object { docker context rm digitalocean -f }
docker context create digitalocean --docker "host=tcp://localhost:23750"
Write-Host "Step 4: Switching to DigitalOcean..." -ForegroundColor Yellow
docker context use digitalocean
Write-Host ""
Write-Host "SUCCESS! Docker Desktop is now connected to DigitalOcean!" -ForegroundColor Green
Write-Host "Try: docker ps" -ForegroundColor Cyan
