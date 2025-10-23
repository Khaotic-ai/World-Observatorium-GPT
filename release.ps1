<<<<<<< Updated upstream
<<<<<<< Updated upstream
param(
  [string]$Tag = $(Get-Date -Format "yyyyMMdd-HHmmss")
)

$ErrorActionPreference = "Stop"
Write-Host "Creating release for provenance pack..." -ForegroundColor Cyan

# Find latest provenance ZIP
$latest = Get-ChildItem -Filter "WorldObservatorium-Provenance_*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $latest) {
  Write-Host "No provenance pack found. Run provenance.ps1 first." -ForegroundColor Red
  exit 1
}

# Derive companion filenames
$base = $latest.BaseName
$log = $base -replace "WorldObservatorium-Provenance", "PROVENANCE_LOG"
$json = $base -replace "WorldObservatorium-Provenance", "PROVENANCE_MANIFEST"

# Tag + push
git add .
git commit -m "Add provenance pack $Tag" --allow-empty
git tag "prov-$Tag"
git push origin "prov-$Tag"

# GitHub CLI release
$title = "Provenance prov-$Tag"
$notes = "Triadic Axis - IP provenance snapshot for $Tag."
gh release create "prov-$Tag" `
  "$log.txt" `
  "$json.json" `
  "$latest.FullName" `
  --title "$title" `
  --notes "$notes"

Write-Host "Release prov-$Tag published successfully." -ForegroundColor Green
=======
=======
>>>>>>> Stashed changes
param(
  [string]$Tag = $(Get-Date -Format "yyyyMMdd-HHmmss")
)

$ErrorActionPreference = "Stop"

Write-Host "Creating release for provenance pack..." -ForegroundColor Cyan

# Find the latest provenance files
$latest = Get-ChildItem -Filter "WorldObservatorium-Provenance_*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$log = $latest.BaseName -replace 'WorldObservatorium-Provenance', 'PROVENANCE_LOG' + '_'
$json = $latest.BaseName -replace 'WorldObservatorium-Provenance', 'PROVENANCE_MANIFEST' + '_'

if (-not (Test-Path $latest.FullName)) {
  Write-Host "No provenance pack found. Run provenance.ps1 first." -ForegroundColor Red
  exit 1
}

# Tag and push
git add .
git commit -m "Add provenance pack $Tag" --allow-empty
git tag "prov-$Tag"
git push origin "prov-$Tag"

# GitHub CLI release
$releaseTitle = "Provenance prov-$Tag"
$releaseNotes = "Triadic Axis – IP provenance snapshot for $Tag."
gh release create "prov-$Tag" `
  "$log.txt" `
  "$json.json" `
  "$latest.FullName" `
  --title "$releaseTitle" `
  --notes "$releaseNotes"

Write-Host "Release prov-$Tag published successfully." -ForegroundColor Green
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
