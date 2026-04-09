$Source = "$env:USERPROFILE\Documents"
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$DestRoot = $ScriptPath  # C:\Backup
$LogFile = Join-Path $DestRoot "last_backup.txt"

New-Item -ItemType Directory -Path $DestRoot -Force | Out-Null

function SafeZipFromDirectory($src, $zip) {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    try {
        Remove-Item -Path $zip -ErrorAction SilentlyContinue
        [System.IO.Compression.ZipFile]::CreateFromDirectory($src, $zip)
        return $true
    } catch {
        return $false
    }
}

if (-Not (Test-Path $LogFile)) {
    $zipName = Join-Path $DestRoot ("backup_full_{0:yyyy-MM-dd_HH-mm-ss-fff}.zip" -f (Get-Date))
    if (-not (SafeZipFromDirectory $Source $zipName)) {
        $tempAll = Join-Path $env:TEMP ("doc_backup_full_{0:yyyyMMddHHmmssfff}" -f (Get-Date))
        New-Item -ItemType Directory -Path $tempAll | Out-Null
        Get-ChildItem -Path $Source -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
            try {
                $rel = $_.FullName.Substring($Source.Length).TrimStart('\')
                $dest = Join-Path $tempAll $rel
                $d = Split-Path $dest -Parent
                if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
                Copy-Item -Path $_.FullName -Destination $dest -Force -ErrorAction Stop
            } catch { }
        }
        Remove-Item -Path $zipName -ErrorAction SilentlyContinue
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::CreateFromDirectory($tempAll, $zipName)
        Remove-Item -Path $tempAll -Recurse -Force -ErrorAction SilentlyContinue
    }
    (Get-Date).ToUniversalTime().ToString("o") | Out-File -FilePath $LogFile -Encoding utf8
    exit 0
}

$last = Get-Content $LogFile | Select-Object -First 1
$lastTime = [DateTime]::Parse($last).ToUniversalTime()

$temp = Join-Path $env:TEMP ("doc_backup_{0:yyyyMMddHHmmssfff}" -f (Get-Date))
New-Item -ItemType Directory -Path $temp | Out-Null

Get-ChildItem -Path $Source -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
    $_.CreationTimeUtc -gt $lastTime
} | ForEach-Object {
    try {
        $relPath = $_.FullName.Substring($Source.Length).TrimStart('\')
        $destPath = Join-Path $temp $relPath
        $destDir = Split-Path $destPath -Parent
        if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
        Copy-Item -Path $_.FullName -Destination $destPath -Force -ErrorAction Stop
    } catch { }
}

if ((Get-ChildItem -Path $temp -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0) {
    $zipName = Join-Path $DestRoot ("backup_inc_{0:yyyy-MM-dd_HH-mm-ss-fff}.zip" -f (Get-Date))
    Remove-Item -Path $zipName -ErrorAction SilentlyContinue
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory($temp, $zipName)
}

Remove-Item -Path $temp -Recurse -Force -ErrorAction SilentlyContinue
(Get-Date).ToUniversalTime().ToString("o") | Out-File -FilePath $LogFile -Encoding utf8
