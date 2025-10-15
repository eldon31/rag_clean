# Simple SSH key setup - connects and shows you what to paste
$pubKey = Get-Content "$env:USERPROFILE\.ssh\id_rsa.pub"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SSH Key Setup for DigitalOcean Droplet" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your public SSH key is:" -ForegroundColor Yellow
Write-Host $pubKey -ForegroundColor Green
Write-Host ""
Write-Host "Connecting to root@165.232.174.154..." -ForegroundColor Cyan
Write-Host "Password: 837829318aA!a" -ForegroundColor Yellow
Write-Host ""
Write-Host "Once connected, run these commands:" -ForegroundColor Yellow
Write-Host "  mkdir -p ~/.ssh && chmod 700 ~/.ssh" -ForegroundColor White
Write-Host "  echo '$pubKey' >> ~/.ssh/authorized_keys" -ForegroundColor White
Write-Host "  chmod 600 ~/.ssh/authorized_keys" -ForegroundColor White
Write-Host "  exit" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter to connect..."
Read-Host

ssh root@165.232.174.154
