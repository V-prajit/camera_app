# PowerShell Script

# Check if Python 3.9 is installed
$pythonInstalled = $False
try {
    $pythonInstalled = (python3.9 --version) -ne $null
} catch {}

if (-not $pythonInstalled) {
    # Check if Chocolatey is installed
    $chocoInstalled = $False
    try {
        $chocoInstalled = (choco -v) -ne $null
    } catch {}

    if (-not $chocoInstalled) {
        Write-Host "Chocolatey is not installed. Installing Chocolatey..."
        
        # Install Chocolatey
        Set-ExecutionPolicy Bypass -Scope Process -Force
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

        if (-not (choco -v)) {
            Write-Host "Failed to install Chocolatey."
            return
        }
    }

    # Install Python 3.9 using Chocolatey
    Write-Host "Installing Python 3.9 using Chocolatey..."
    choco install python --version=3.9 -y

    # Update the PATH environment variable temporarily for the current session
    $pythonPath = "C:\Python39"  # Replace with your Python installation path if different
    $Env:Path += ";$pythonPath"
    $Env:Path += ";$pythonPath\Scripts"
}

# Install additional Python packages
Write-Host "Installing additional Python packages..."
try {
    pip3.9 install opencv-python mediapipe Pillow numpy
    Write-Host "All required Python packages have been successfully installed."
} catch {
    Write-Host "Failed to install one or more Python packages."
    return
}

Write-Host "Try recording your first video by running 'python3.9 record_video.py'"

