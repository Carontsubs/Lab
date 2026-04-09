function Invoke-ScriptElevated {
    param([string]$ScriptPath)

    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        $escaped = $ScriptPath.Replace("`","``").Replace('"','\"')
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = "powershell.exe"
        $psi.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$escaped`""
        $psi.Verb = "runas"
        $psi.UseShellExecute = $true
        try { [System.Diagnostics.Process]::Start($psi) | Out-Null } catch { throw "Cancel·lat o error d'elevació." }
        exit 0
    } else {
        & $ScriptPath
    }
}


# Configuració
$LogFile = "C:\Backup\last_backup.txt"
$BackupScriptPath = "C:\Backup\BackupDocuments.ps1"
$MonthsThreshold = 3

if (-not (Test-Path $LogFile)) {
    Write-Output "No hi ha fitxer de registre; executant backup..."
    Invoke-ScriptElevated -ScriptPath $BackupScriptPath
    exit 0
}

try {
    $raw = Get-Content $LogFile -ErrorAction Stop | Select-Object -First 1
    $lastTime = [DateTime]::Parse($raw).ToUniversalTime()
} catch {
    Write-Output "Error llegint o parsejant $LogFile. Executant backup per precaució..."
    Invoke-ScriptElevated -ScriptPath $BackupScriptPath
    exit 0
}

$thresholdDate = (Get-Date).ToUniversalTime().AddMonths(-$MonthsThreshold)
if ($lastTime -lt $thresholdDate) {
    Write-Output "Última execució: $lastTime — fa més de $MonthsThreshold mesos. Executant backup..."
    Invoke-ScriptElevated -ScriptPath $BackupScriptPath
} else {
    Write-Output "Última execució: $lastTime — no cal executar (menys de $MonthsThreshold mesos)."
}

