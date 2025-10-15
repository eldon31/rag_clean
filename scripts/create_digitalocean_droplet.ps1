# Create DigitalOcean Droplet with SSH Key
# Usage: Set $env:TOKEN to your DigitalOcean API token first
# Example: $env:TOKEN = "your_api_token_here"

param(
    [string]$Token = $env:TOKEN
)

if (-not $Token) {
    Write-Host "ERROR: DigitalOcean API token not found." -ForegroundColor Red
    Write-Host "Please set the TOKEN environment variable:" -ForegroundColor Yellow
    Write-Host '  $env:TOKEN = "your_digitalocean_api_token"' -ForegroundColor Cyan
    exit 1
}

Write-Host "Step 1: Fetching SSH key ID for 'digitalocean-raze0-key'..." -ForegroundColor Cyan

# Get SSH key ID
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $Token"
}

try {
    $sshKeysResponse = Invoke-RestMethod -Uri "https://api.digitalocean.com/v2/account/keys" -Headers $headers -Method Get
    $sshKey = $sshKeysResponse.ssh_keys | Where-Object { $_.name -eq "digitalocean-raze0-key" }
    
    if (-not $sshKey) {
        Write-Host "ERROR: SSH key 'digitalocean-raze0-key' not found in your DigitalOcean account." -ForegroundColor Red
        Write-Host "Available SSH keys:" -ForegroundColor Yellow
        $sshKeysResponse.ssh_keys | ForEach-Object { Write-Host "  - $($_.name) (ID: $($_.id))" }
        exit 1
    }
    
    $sshKeyId = $sshKey.id
    Write-Host "Found SSH key ID: $sshKeyId" -ForegroundColor Green
    
} catch {
    Write-Host "ERROR: Failed to fetch SSH keys: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`nStep 2: Creating droplet..." -ForegroundColor Cyan

# Create droplet with SSH key
$dropletData = @{
    name = "docker-ubuntu-s-2vcpu-8gb-160gb-intel-sgp1-01"
    size = "s-2vcpu-8gb-160gb-intel"
    region = "sgp1"
    image = "docker-20-04"
    vpc_uuid = "2ebf8441-63c8-4436-9e07-8b0efe750a5b"
    ssh_keys = @($sshKeyId)
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "https://api.digitalocean.com/v2/droplets" `
        -Headers $headers `
        -Method Post `
        -Body $dropletData
    
    Write-Host "`nDroplet created successfully!" -ForegroundColor Green
    Write-Host "Droplet ID: $($response.droplet.id)" -ForegroundColor Cyan
    Write-Host "Name: $($response.droplet.name)" -ForegroundColor Cyan
    Write-Host "Status: $($response.droplet.status)" -ForegroundColor Cyan
    Write-Host "`nWaiting for IP address assignment..." -ForegroundColor Yellow
    Write-Host "You can check the status with:" -ForegroundColor Yellow
    Write-Host "  Invoke-RestMethod -Uri 'https://api.digitalocean.com/v2/droplets/$($response.droplet.id)' -Headers @{'Authorization'='Bearer `$env:TOKEN'}" -ForegroundColor Cyan
    
    # Pretty print the full response
    Write-Host "`nFull Response:" -ForegroundColor Cyan
    $response.droplet | ConvertTo-Json -Depth 10
    
} catch {
    Write-Host "ERROR: Failed to create droplet: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
    exit 1
}
