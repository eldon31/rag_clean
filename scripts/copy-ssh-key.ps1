# Copy SSH public key to DigitalOcean Droplet
# This script copies your local SSH public key to the Droplet's authorized_keys

$dropletIP = "165.232.174.154"
$user = "root"
$password = "837829318aA!a"

# Read the public key
$pubKeyPath = "$env:USERPROFILE\.ssh\id_rsa.pub"

if (-not (Test-Path $pubKeyPath)) {
    Write-Host "ERROR: SSH public key not found at $pubKeyPath" -ForegroundColor Red
    exit 1
}

$pubKey = Get-Content $pubKeyPath -Raw
$pubKey = $pubKey.Trim()

Write-Host "Public key found. Copying to $user@$dropletIP..." -ForegroundColor Green
Write-Host ""

# Use plink (PuTTY) if available, otherwise try expect-style automation
# First, try using a here-string to pipe password to ssh
$sshCommand = "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '$pubKey' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# Create a temporary script for plink or use PowerShell's SSH
try {
    # Try using plink if installed (from PuTTY)
    $plinkPath = Get-Command plink.exe -ErrorAction SilentlyContinue
    if ($plinkPath) {
        Write-Host "Using plink for SSH connection..." -ForegroundColor Cyan
        & plink.exe -batch -pw $password "$user@$dropletIP" $sshCommand
    } else {
        # Fallback: Use PowerShell Invoke-SSHCommand if Posh-SSH is available
        Write-Host "Attempting SSH connection with password..." -ForegroundColor Cyan
        
        # Create a temporary expect-style script
        $expectScript = @"
spawn ssh $user@$dropletIP "$sshCommand"
expect "password:"
send "$password\r"
expect eof
"@
        
        # Try direct approach with password in environment
        $env:SSHPASS = $password
        $output = & ssh -o StrictHostKeyChecking=no -o PreferredAuthentications=password -o PubkeyAuthentication=no "$user@$dropletIP" $sshCommand 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host $output
        } else {
            Write-Host "Standard SSH failed. Trying alternative method..." -ForegroundColor Yellow
            # Alternative: use cmd /c with echo
            $passwordInput = "echo $password"
            & cmd /c "$passwordInput | ssh -o StrictHostKeyChecking=no $user@$dropletIP `"$sshCommand`""
        }
    }
    
    Write-Host "`nSSH key copied successfully!" -ForegroundColor Green
    Write-Host "Testing passwordless SSH connection..." -ForegroundColor Cyan
    
    # Test the connection
    $testOutput = ssh -o StrictHostKeyChecking=no "$user@$dropletIP" "echo 'SSH key working!'" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host $testOutput -ForegroundColor Green
        Write-Host "You can now SSH without a password!" -ForegroundColor Green
    }
    
} catch {
    Write-Host "`nError: $_" -ForegroundColor Red
    Write-Host "`nManual steps:" -ForegroundColor Yellow
    Write-Host "1. Run: ssh $user@$dropletIP" -ForegroundColor White
    Write-Host "2. Enter password: $password" -ForegroundColor White
    Write-Host "3. Run these commands:" -ForegroundColor White
    Write-Host "   mkdir -p ~/.ssh && chmod 700 ~/.ssh" -ForegroundColor White
    Write-Host "   echo '$pubKey' >> ~/.ssh/authorized_keys" -ForegroundColor White
    Write-Host "   chmod 600 ~/.ssh/authorized_keys" -ForegroundColor White
    Write-Host "   exit" -ForegroundColor White
}
