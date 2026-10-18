# Crea roles, categorias y canales del servidor de Discord del equipo.
# Requiere las variables de entorno DISCORD_TOKEN (token del bot) y DISCORD_GUILD (ID del servidor).
# El bot necesita los permisos Manage Channels y Manage Roles. No guardar el token en ningun archivo.
$ErrorActionPreference = 'Stop'
if (-not $env:DISCORD_TOKEN -or -not $env:DISCORD_GUILD) { throw 'Faltan DISCORD_TOKEN y/o DISCORD_GUILD.' }
$g = $env:DISCORD_GUILD
$api = 'https://discord.com/api/v10'
$h = @{ Authorization = "Bot $($env:DISCORD_TOKEN)"; 'User-Agent' = 'DiscordBot (proyecto-gsi, 1.0)' }

function Call($method, $path, $body) {
    $args2 = @{ Method = $method; Uri = "$api$path"; Headers = $h }
    if ($body) { $args2.Body = [Text.Encoding]::UTF8.GetBytes(($body | ConvertTo-Json -Depth 6)); $args2.ContentType = 'application/json; charset=utf-8' }
    for ($i = 0; $i -lt 3; $i++) {
        try { $r = Invoke-RestMethod @args2; Start-Sleep -Milliseconds 500; return $r }
        catch { if ($_.Exception.Response -and [int]$_.Exception.Response.StatusCode -eq 429) { Start-Sleep -Seconds 3 } else { throw } }
    }
}

$roles = @(Call 'GET' "/guilds/$g/roles")
$chans = @(Call 'GET' "/guilds/$g/channels")

function Role($name, $color) {
    $r = $roles | Where-Object { $_.name -eq $name } | Select-Object -First 1
    if ($r) { return $r }
    Write-Host "rol: $name"
    return Call 'POST' "/guilds/$g/roles" @{ name = $name; color = $color; mentionable = $true }
}
function Chan($name, $type, $parent, $topic, $overwrites) {
    $c = $chans | Where-Object { $_.name -eq $name -and $_.type -eq $type } | Select-Object -First 1
    if ($c) { return $c }
    Write-Host "canal: $name"
    $b = @{ name = $name; type = $type }
    if ($parent) { $b.parent_id = $parent }
    if ($topic) { $b.topic = $topic }
    if ($overwrites) { $b.permission_overwrites = $overwrites }
    $new = Call 'POST' "/guilds/$g/channels" $b
    $script:chans += $new
    return $new
}

$po = Role 'Product Owner' 15105570
$sm = Role 'Scrum Master' 3447003
$eq = Role 'Equipo' 3066993

# #anuncios: lee todo el mundo, escribe solo el Product Owner
$soloPO = @(
    @{ id = $g; type = 0; deny = '2048'; allow = '0' },
    @{ id = $po.id; type = 0; allow = '2048'; deny = '0' }
)

$info = Chan 'INFO' 4 $null $null $null
Chan 'anuncios' 0 $info.id 'Avisos de entregas y sprints (solo Product Owner)' $soloPO | Out-Null
Chan 'entorno' 0 $info.id 'Tailscale, URL del servidor y guia del entorno de trabajo' $null | Out-Null
Chan 'recursos' 0 $info.id 'Enlaces: repositorio, backlog, CADUS.rem, maquetas' $null | Out-Null

$scrum = Chan 'SCRUM' 4 $null $null $null
Chan 'daily' 0 $scrum.id 'Que hice, que hare y que me bloquea' $null | Out-Null
Chan 'sprint-review' 0 $scrum.id 'Acuerdos y evidencias del sprint' $null | Out-Null
Chan 'retrospectiva' 0 $scrum.id 'Que fue bien y que mejorar' $null | Out-Null

$dev = Chan 'DESARROLLO' 4 $null $null $null
foreach ($n in 'infra-y-bd', 'portada', 'institucional-y-normativa', 'delegaciones', 'buzon-y-faq', 'github', 'avisos-servidor') {
    Chan $n 0 $dev.id $null $null | Out-Null
}

$voz = Chan 'VOZ' 4 $null $null $null
Chan 'Sala de trabajo' 2 $voz.id $null $null | Out-Null
Chan 'Daily' 2 $voz.id $null $null | Out-Null

Write-Host 'Listo. Asigna los roles a cada miembro desde Discord.'
