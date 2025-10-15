@echo off
REM Copy SSH public key to DigitalOcean Droplet
echo Copying SSH key to Droplet...
echo.

set /p pubkey=<C:\Users\raze0\.ssh\id_rsa.pub

echo mkdir -p ~/.ssh ^&^& chmod 700 ~/.ssh ^&^& echo "%pubkey%" ^>^> ~/.ssh/authorized_keys ^&^& chmod 600 ~/.ssh/authorized_keys | ssh root@165.232.174.154

echo.
echo SSH key has been copied!
echo Testing connection...
ssh root@165.232.174.154 "echo 'Connection successful!'"
