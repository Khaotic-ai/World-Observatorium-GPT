<#  World Observatorium — Provenance Pack Generator (ASCII-safe)
    Creates SHA-256 hashes over key assets, logs git+env metadata,
    writes a TXT + JSON manifest, and zips the set.
#>

param(
  [string]$Root = ".",
  [string[]]$Include = @(
    "orchestrator",
    "engine",
    "schema",
    "adapters",
    "IP_CLAIM.md",
    "LICENSE",
    "README.md"
  ),
  [string[]]$Extra = @() # add any extra paths you want included
)

# --- Prep & metadata ---
$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path $Root)

$ts = (Get-Date).ToUniversalTime().ToString("yyyyMMdd_HHmmss'Z'")
$logName = "PROVENANCE_LOG_$ts.txt"
$jsonName = "PROVENANCE_MANIFEST_$ts.json"
$zipName = "WorldObservatorium-Provenance_$ts.zip"

# Git metadata (best-effort)
function Invoke-Git($gitArgs) {
  try { (& git @gitArgs) 2>$null } catch { $null }
}
$gitCommit = (Invoke-Git @("rev-parse","HEAD")) -replace '\s+$',''
$gitBranch = (Invoke-Git @("rev-parse","--abbrev-ref","HEAD")) -replace '\s+$',''
$gitRemote = ((Invoke-Git @("remote","get-url","origin")) -replace '\s+$','')

# Environment metadata
$meta = [ordered]@{
  project            = "World Observatorium"
  directive          = "Triadic Axis - IP Provenance"
  utc_generated_at   = (Get-Date).ToUniversalTime().ToString("o")
  machine            = $env:COMPUTERNAME
  user               = $env:USERNAME
  os                 = (Get-CimInstance Win32_OperatingSystem).Caption
  powershell_version = $PSVersionTable.PSVersion.ToString()
  git_commit         = $gitCommit
  git_branch         = $gitBranch
  git_remote         = $gitRemote
  repo_path          = (Get-Location).Path
  include_paths      = $Include
  extra_paths        = $Extra
  hash_algorithm     = "SHA-256"
}

# --- Build file list ---
$targets = @()
$want = $Include + $Extra | Where-Object { $_ -and (Test-Path $_) }

# Exclusions (regex)
$excludePatterns = @(
  '\.git[\\/]',
  '__pycache__',
  '\.mypy_cache',
  '\.pytest_cache',
  '\.ipynb_checkpoints',
  'node_modules',
  '\.DS_Store$',
  '\.zip$'
)

foreach ($p in $want) {
  $full = Resolve-Path $p
  if ((Get-Item $full).PSIsContainer) {
    $targets += Get-ChildItem $full -Recurse -File | ForEach-Object { $_.FullName }
  } else {
    $targets += (Get-Item $full).FullName
  }
}

# Filter exclusions
$targets = $targets | Where-Object {
  $f = $_
  -not ($excludePatterns | Where-Object { $f -match $_ })
}

# Deduplicate & sort
$targets = $targets | Sort-Object -Unique

# --- Hash & manifest ---
$entries = @()
Write-Host ("Hashing {0} files..." -f $targets.Count)

foreach ($f in $targets) {
  $rel = Resolve-Path -Relative $f
  $fi  = Get-Item $f
  $h   = Get-FileHash -Algorithm SHA256 -Path $f
  $entries += [ordered]@{
    path_relative  = $rel
    size_bytes     = $fi.Length
    last_write_utc = ($fi.LastWriteTimeUtc.ToString("o"))
    sha256         = $h.Hash
  }
}

# --- Write TXT log ---
$hdr = @"
World Observatorium - Provenance Log
Directive     : Triadic Axis - IP Provenance
Generated UTC : $($meta.utc_generated_at)
Host          : $($meta.machine) (PS $($meta.powershell_version))
OS            : $($meta.os)
Repo          : $($meta.repo_path)
Git Remote    : $($meta.git_remote)
Branch        : $($meta.git_branch)
Commit        : $($meta.git_commit)
Hash Alg      : $($meta.hash_algorithm)

Included paths:
  - $(($meta.include_paths + $meta.extra_paths) -join "`n  - ")

--------------------------------------------------------------------------------
SHA256                                       Size      LastWrite (UTC)                 Path
--------------------------------------------------------------------------------
"@

$lines = $entries | ForEach-Object {
  "{0}  {1,10}  {2}  {3}" -f $_.sha256, $_.size_bytes, $_.last_write_utc, $_.path_relative
}

$hdr   | Out-File -FilePath $logName -Encoding UTF8 -Force
$lines | Out-File -FilePath $logName -Encoding UTF8 -Append

# --- Write JSON manifest ---
$manifest = [ordered]@{
  metadata = $meta
  files    = $entries
}
$manifest | ConvertTo-Json -Depth 6 | Out-File -FilePath $jsonName -Encoding UTF8 -Force

# --- Package ZIP ---
$zipSet = $targets + @($logName, $jsonName)
if (Test-Path $zipName) { Remove-Item $zipName -Force }
Compress-Archive -Path $zipSet -DestinationPath $zipName

Write-Host ""
Write-Host "Provenance pack created:" -ForegroundColor Green
Write-Host "  Log     : $logName"
Write-Host "  Manifest: $jsonName"
Write-Host "  ZIP     : $zipName"
