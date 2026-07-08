param(
  [string]$Descriptions = "scripts\descriptions.json",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$argsList = @("--descriptions", $Descriptions)
if ($DryRun) {
  $argsList += "--dry-run"
}

python scripts\update_yt_desc.py @argsList
