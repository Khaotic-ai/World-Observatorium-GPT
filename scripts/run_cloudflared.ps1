param([string]$LocalUrl = "http://127.0.0.1:8787")
cloudflared tunnel --url $LocalUrl
