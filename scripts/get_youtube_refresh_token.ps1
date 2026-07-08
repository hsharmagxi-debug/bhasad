param(
  [Parameter(Mandatory = $true)]
  [string]$Credentials,

  [string]$Repo = "hsharmagxi-debug/bhasad",

  [switch]$SetGitHubSecrets
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $Credentials)) {
  throw "Credentials file not found: $Credentials"
}

$raw = Get-Content -LiteralPath $Credentials -Raw | ConvertFrom-Json
$client = if ($raw.installed) { $raw.installed } elseif ($raw.web) { $raw.web } else { $null }
if (-not $client) {
  throw "Expected OAuth client JSON with an installed or web object."
}

$clientId = [string]$client.client_id
$clientSecret = [string]$client.client_secret
if (-not $clientId -or -not $clientSecret) {
  throw "Credentials JSON is missing client_id or client_secret."
}

$port = Get-Random -Minimum 49152 -Maximum 65000
$redirectUri = "http://127.0.0.1:$port/"
$scope = "https://www.googleapis.com/auth/youtube"
$state = [guid]::NewGuid().ToString("N")

$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add($redirectUri)
$listener.Start()

$authParams = @{
  client_id = $clientId
  redirect_uri = $redirectUri
  response_type = "code"
  scope = $scope
  access_type = "offline"
  prompt = "consent"
  state = $state
}

$query = ($authParams.GetEnumerator() | ForEach-Object {
  "{0}={1}" -f [uri]::EscapeDataString($_.Key), [uri]::EscapeDataString([string]$_.Value)
}) -join "&"

$authUrl = "https://accounts.google.com/o/oauth2/v2/auth?$query"
Write-Output "Opening Google OAuth consent in your browser..."
Write-Output "If the browser does not open, paste this URL manually:"
Write-Output $authUrl
Start-Process $authUrl

try {
  $context = $listener.GetContext()
  $request = $context.Request
  $response = $context.Response

  $code = $request.QueryString["code"]
  $returnedState = $request.QueryString["state"]
  $errorValue = $request.QueryString["error"]

  $html = "<html><body><h1>Bhasad YouTube OAuth Complete</h1><p>You can close this tab and return to Codex.</p></body></html>"
  if ($errorValue) {
    $html = "<html><body><h1>OAuth Failed</h1><p>$errorValue</p></body></html>"
  }
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($html)
  $response.ContentType = "text/html"
  $response.ContentLength64 = $bytes.Length
  $response.OutputStream.Write($bytes, 0, $bytes.Length)
  $response.OutputStream.Close()

  if ($errorValue) {
    throw "OAuth failed: $errorValue"
  }
  if (-not $code) {
    throw "OAuth callback did not include a code."
  }
  if ($returnedState -ne $state) {
    throw "OAuth state mismatch."
  }
}
finally {
  $listener.Stop()
}

$tokenResponse = Invoke-RestMethod `
  -Method Post `
  -Uri "https://oauth2.googleapis.com/token" `
  -ContentType "application/x-www-form-urlencoded" `
  -Body @{
    code = $code
    client_id = $clientId
    client_secret = $clientSecret
    redirect_uri = $redirectUri
    grant_type = "authorization_code"
  }

$refreshToken = [string]$tokenResponse.refresh_token
if (-not $refreshToken) {
  throw "Google did not return a refresh token. Re-run with consent prompt, or revoke the old grant and try again."
}

if ($SetGitHubSecrets) {
  Write-Output "Setting GitHub Actions secrets on $Repo..."
  $clientId | gh secret set YT_CLIENT_ID --repo $Repo
  $clientSecret | gh secret set YT_CLIENT_SECRET --repo $Repo
  $refreshToken | gh secret set YT_REFRESH_TOKEN --repo $Repo
  Write-Output "GitHub Actions secrets set: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN"
}
else {
  Write-Output "OAuth succeeded. Re-run with -SetGitHubSecrets to store values directly in GitHub."
}
