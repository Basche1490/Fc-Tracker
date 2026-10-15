# EA Sports FC Live Telemetry Bridge (Native PowerShell - No Python Required)
param(
    [int]$Port = 5050
)

$ErrorActionPreference = "Continue"
$EventsFile = Join-Path $PSScriptRoot "telemetry_events.json"

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host " EA SPORTS FC TELEMETRY BRIDGE (Native PowerShell)" -ForegroundColor Yellow
Write-Host " Direct PC-to-Mobile Connection" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan

# Check network profiles
$profiles = Get-NetConnectionProfile -ErrorAction SilentlyContinue
foreach ($p in $profiles) {
    if ($p.NetworkCategory -eq "Private") {
        Write-Host "🟢 Network profile '$($p.Name)': Private (LAN traffic permitted)" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Network profile '$($p.Name)': $($p.NetworkCategory)" -ForegroundColor Yellow
        Write-Host "   (Note: Windows blocks phone traffic on Public networks. Switch to Private in Windows Settings if phone cannot connect)" -ForegroundColor DarkGray
    }
}

# Find local IP addresses, prioritizing real Wi-Fi & Ethernet
$allIpObjs = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { 
    $_.IPAddress -notlike "127.*" -and 
    $_.IPAddress -notlike "169.254.*" 
}

$wifiIps = @()
$otherIps = @()
foreach ($ipObj in $allIpObjs) {
    $ip = $ipObj.IPAddress
    $alias = $ipObj.InterfaceAlias
    if ($alias -match "WSL|vEthernet|VirtualBox|VMware|Docker|Tailscale") {
        # Virtual adapter
    } elseif ($ip -like "192.168.*" -or $ip -like "10.*" -or ($ip -like "172.*" -and $alias -match "Wi-Fi|Ethernet|WLAN")) {
        $wifiIps += $ip
    } else {
        $otherIps += $ip
    }
}

$primaryIp = if ($wifiIps.Count -gt 0) { $wifiIps[0] } elseif ($otherIps.Count -gt 0) { $otherIps[0] } else { "127.0.0.1" }
$displayIps = ($wifiIps + $otherIps) | Select-Object -Unique

Write-Host ""
Write-Host "⭐ ENTER THIS IN YOUR ANDROID APP:" -ForegroundColor Yellow
Write-Host "   http://${primaryIp}:${Port}" -ForegroundColor Green
if ($displayIps.Count -gt 1) {
    Write-Host "Other detected network interfaces:" -ForegroundColor DarkGray
    foreach ($ip in $displayIps) {
        if ($ip -ne $primaryIp) {
            Write-Host "   http://${ip}:${Port}" -ForegroundColor DarkGray
        }
    }
}

Write-Host ""
Write-Host "🌐 WEB DASHBOARD & MANUAL TESTING:" -ForegroundColor Yellow
Write-Host "   http://localhost:${Port}" -ForegroundColor White
Write-Host "===================================================" -ForegroundColor Cyan

# Initialize Events Cache
$global:EventList = [System.Collections.Generic.List[string]]::new()
if (Test-Path $EventsFile) {
    try {
        $existing = Get-Content $EventsFile -Raw | ConvertFrom-Json
        foreach ($e in $existing) {
            $global:EventList.Add(($e | ConvertTo-Json -Compress))
        }
        Write-Host "Loaded $($global:EventList.Count) historical events from cache." -ForegroundColor DarkGray
    } catch {}
}

# Function to add event
function Add-TelemetryEvent {
    param(
        [string]$Title,
        [string]$Message,
        [string]$RawPayload
    )
    $timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $formattedEvent = [PSCustomObject]@{
        event = "message"
        id = "ev-$timestamp-" + (Get-Random -Maximum 9999)
        time = $timestamp
        title = $Title
        message = if ($RawPayload) { $RawPayload } else { $Message }
    }
    $jsonStr = $formattedEvent | ConvertTo-Json -Compress
    $global:EventList.Add($jsonStr)

    # Keep last 100 events
    if ($global:EventList.Count -gt 100) {
        $global:EventList.RemoveAt(0)
    }

    # Save to file
    try {
        "[" + ($global:EventList -join ",") + "]" | Set-Content $EventsFile -Encoding UTF8
    } catch {}

    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] TELEMETRY SAVED: $Title" -ForegroundColor Green
}

function Create-SampleMatchJson {
    $today = (Get-Date -Format 'yyyy-MM-dd')
    return @"
{
    "dataType": "match",
    "title": "Live Match Final",
    "message": "Full Time: vs 3 - 1 Arsenal (Premier League)",
    "opponentName": "Arsenal",
    "isHome": true,
    "goalsFor": 3,
    "goalsAgainst": 1,
    "resultBadge": "W",
    "date": "$today",
    "competition": "Premier League",
    "shotsFor": 12,
    "shotsAgainst": 6,
    "possession": 56,
    "passingAccuracy": 88,
    "expectedGoals": 2.8,
    "expectedGoalsAgainst": 0.9,
    "playerPerformances": [
        {"playerName": "Bukayo Saka", "goals": 2, "assists": 1, "rating": 8.9, "yellowCard": false, "redCard": false},
        {"playerName": "Declan Rice", "goals": 1, "assists": 0, "rating": 7.8, "yellowCard": true, "redCard": false},
        {"playerName": "Martin Odegaard", "goals": 0, "assists": 2, "rating": 8.4, "yellowCard": false, "redCard": false}
    ],
    "goalDetails": [
        {"playerName": "Bukayo Saka", "isOpponent": false},
        {"playerName": "Declan Rice", "isOpponent": false},
        {"playerName": "Bukayo Saka", "isOpponent": false},
        {"playerName": "Kai Havertz (Opponent)", "isOpponent": true}
    ]
}
"@
}

function Create-SampleTransferJson {
    $today = (Get-Date -Format 'yyyy-MM-dd')
    return @"
{
    "dataType": "transfer",
    "title": "Transfer Finalized",
    "message": "Erling Haaland signed from Manchester City for €120.0M",
    "playerName": "Erling Haaland",
    "type": "Bought",
    "feeM": 120.0,
    "fromToClub": "Manchester City",
    "date": "$today"
}
"@
}

# Setup HttpListener supporting port 5050
$Listener = New-Object System.Net.HttpListener
$bound = $false

# Bind directly to strong wildcard '+' so it matches the URLACL created by netsh
try {
    $Listener.Prefixes.Add("http://+:$Port/")
    $bound = $true
    Write-Host "  -> Bound: http://+:$Port/ (Strong wildcard - accepts phone and PC connections)" -ForegroundColor Green
} catch {
    Write-Host "  -> Wildcard '+' failed on port $Port ($($_)). Falling back to explicit IP prefixes..." -ForegroundColor Yellow
}

if (-not $bound) {
    $tryList = @("http://localhost:$Port/", "http://127.0.0.1:$Port/") + ($displayIps | ForEach-Object { "http://${_}:$Port/" })
    foreach ($prefix in $tryList) {
        try {
            $Listener.Prefixes.Add($prefix)
            Write-Host "  -> Bound: $prefix" -ForegroundColor DarkGray
        } catch {}
    }
}

try {
    $Listener.Start()
    Write-Host ""
    Write-Host "===================================================" -ForegroundColor Green
    Write-Host " Bridge Server started successfully!" -ForegroundColor Green
    Write-Host " 🟢 Active listening on Port $Port." -ForegroundColor Green
    Write-Host " Keep this window open while playing EA FC. Press Ctrl+C to stop." -ForegroundColor White
    Write-Host "===================================================" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "===================================================" -ForegroundColor Red
    Write-Host " ERROR: Failed to bind to port ${Port}: $_" -ForegroundColor Red
    Write-Host " Please close any other app using that port." -ForegroundColor Yellow
    Write-Host "===================================================" -ForegroundColor Red
    pause
    exit 1
}


# =========================================================================
# PROJECT ATLAS & FC26 AUTO-CAPTURE HOT-FOLDER AUTO-INGESTER
# Automatically watches Documents\FC26 Export for newly published match exports
# =========================================================================
$global:ProcessedAtlasFolders = [System.Collections.Generic.HashSet[string]]::new()

function Check-AtlasExportFolder {
    try {
        $docs = [Environment]::GetFolderPath("MyDocuments")
        $atlasRoot = Join-Path $docs "FC26 Export"
        if (-not (Test-Path $atlasRoot)) { return }

        $matchStatsReady = Join-Path $atlasRoot "MatchStats\ready"
        $snapshotsReady = Join-Path $atlasRoot "Snapshots\ready"

        if (Test-Path $matchStatsReady) {
            $folders = @(Get-ChildItem -Path $matchStatsReady -Directory -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending)
            foreach ($folder in $folders) {
                $folderId = $folder.Name
                if ($global:ProcessedAtlasFolders.Contains($folderId)) { continue }

                $readyMarker = Join-Path $folder.FullName "MATCH_READY"
                $altMarker = Join-Path $folder.FullName "READY_FOR_MANUAL_ZIP_AND_UPLOAD.txt"
                $participantsCsv = Join-Path $folder.FullName "16_match_participants_wide.csv"
                $teamsCsv = Join-Path $folder.FullName "18_match_teams_wide.csv"

                if ((Test-Path $readyMarker -or Test-Path $altMarker) -and (Test-Path $participantsCsv) -and (Test-Path $teamsCsv)) {
                    Write-Host ""
                    Write-Host "[PROJECT ATLAS] 🎯 New MatchStats export detected: $folderId" -ForegroundColor Cyan

                    # Match context from Snapshots
                    $oppName = "Opponent"
                    $managedClubName = "My Club"
                    $managedTeamId = 0
                    $currentLeagueName = "League"
                    $compName = "League Match"
                    $isHome = $true
                    $managedScore = 0
                    $opponentScore = 0
                    $resultBadge = "W"
                    $matchDate = (Get-Date -Format "yyyy-MM-dd")
                    $currentTablePos = 0
                    $completedMatches = @()
                    $homePen = 0
                    $awayPen = 0
                    $isExtraTime = $false
                    $managedSquadPlayerIds = [System.Collections.Generic.HashSet[int]]::new()

                    if (Test-Path $snapshotsReady) {
                        $snapFolders = @(Get-ChildItem -Path $snapshotsReady -Directory -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending)
                        if ($snapFolders.Count -gt 0) {
                            $latestSnap = $snapFolders[0].FullName
                            $managedMatchesFile = Join-Path $latestSnap "managed_team_matches.csv"
                            $teamLeaguesFile = Join-Path $latestSnap "team_leagues.csv"
                            $metaFile = Join-Path $latestSnap "career_metadata.csv"
                            $rostersFile = Join-Path $latestSnap "rosters.csv"

                            if (Test-Path $metaFile) {
                                $metaRows = @(Import-Csv -Path $metaFile -ErrorAction SilentlyContinue)
                                foreach ($m in $metaRows) {
                                    if ($m.key -eq "managed_team_id" -and $m.value) { $managedTeamId = [int]$m.value }
                                    if ($m.key -eq "managed_team_name" -and $m.value) { $managedClubName = $m.value }
                                }
                            }

                            if (Test-Path $managedMatchesFile) {
                                $snapMatches = @(Import-Csv -Path $managedMatchesFile -ErrorAction SilentlyContinue)
                                $completedMatches = @($snapMatches | Where-Object { $_.is_completed -eq "1" -or $_.is_completed -eq 1 })
                                if ($completedMatches.Count -gt 0) {
                                    $latest = $completedMatches[-1]
                                    if ($latest.managed_team_id) { $managedTeamId = [int]$latest.managed_team_id }
                                    if ($latest.managed_team_name) { $managedClubName = $latest.managed_team_name }
                                    if ($latest.opponent_team_name) { $oppName = $latest.opponent_team_name }
                                    $isHome = ($latest.side -eq "HOME" -or $latest.managed_team_side -eq "HOME")
                                    $managedScore = [int]($latest.managed_score)
                                    $opponentScore = [int]($latest.opponent_score)
                                    $resultBadge = if ($latest.result) { $latest.result } elseif ($latest.managed_team_result) { $latest.managed_team_result } else { if ($managedScore -gt $opponentScore) { "W" } elseif ($managedScore -eq $opponentScore) { "D" } else { "L" } }
                                    if ($latest.date) { $matchDate = $latest.date }
                                }
                            }

                            # Extract Primary Domestic League from team_leagues.csv (highest matches_played)
                            if (Test-Path $teamLeaguesFile) {
                                $tlRows = @(Import-Csv -Path $teamLeaguesFile -ErrorAction SilentlyContinue)
                                $bestPld = -1
                                foreach ($tl in $tlRows) {
                                    $tlTid = if ($tl.team_id) { [int]$tl.team_id } else { 0 }
                                    $tlTname = if ($tl.team_name) { $tl.team_name } else { "" }
                                    if ($tlTid -eq $managedTeamId -or ($managedClubName -and $tlTname -like "*$managedClubName*")) {
                                        $pld = if ($tl.matches_played) { [int]$tl.matches_played } else { 0 }
                                        $pos = if ($tl.current_table_position) { [int]$tl.current_table_position } else { 0 }
                                        if ($pld -gt $bestPld -and $pos -gt 0) {
                                            $bestPld = $pld
                                            $currentTablePos = $pos
                                            if ($tl.league_name) { $currentLeagueName = $tl.league_name }
                                        } elseif ($bestPld -eq -1 -and $pos -gt 0) {
                                            $currentTablePos = $pos
                                            if ($tl.league_name) { $currentLeagueName = $tl.league_name }
                                        }
                                    }
                                }
                            }

                            # Cache Managed Squad Player IDs to robustly match participant team index
                            if (Test-Path $rostersFile) {
                                $rosterRows = @(Import-Csv -Path $rostersFile -ErrorAction SilentlyContinue)
                                foreach ($r in $rosterRows) {
                                    if ($r.team_id -and [int]$r.team_id -eq $managedTeamId) {
                                        $managedSquadPlayerIds.Add([int]$r.player_id) | Out-Null
                                    }
                                }
                            }
                        }
                    }

                    # Determine Competition & Stage logic
                    $rawComp = if ($latest -and $latest.competition_name) { $latest.competition_name } else { $currentLeagueName }
                    $isPlayoff = ($rawComp -like "*Play-off*" -or $rawComp -like "*Playoff*" -or $rawComp -like "*Promotion*")
                    $isRegularLeague = (-not $isPlayoff) -and (
                        $rawComp -like "*$currentLeagueName*" -or
                        $rawComp -like "*League*" -or
                        $rawComp -like "*Championship*" -or
                        $rawComp -like "*Division*" -or
                        $rawComp -like "*Premier*"
                    ) -and ($rawComp -notlike "*Cup*") -and ($rawComp -notlike "*FA*") -and ($rawComp -notlike "*Carabao*") -and ($rawComp -notlike "*Trophy*")

                    $stageVal = "Matchday 1"
                    if ($isPlayoff) {
                        # The competition should STILL be the league the team is currently in, and the stage should be Playoff
                        $compName = $currentLeagueName
                        $playoffMatches = @($completedMatches | Where-Object { $_.competition_name -like "*Play-off*" -or $_.competition_name -like "*Playoff*" -or $_.competition_name -like "*Promotion*" })
                        $pCount = [Math]::Max(1, $playoffMatches.Count)
                        if ($pCount -ge 3) {
                            $stageVal = "Play-off Final"
                        } elseif ($pCount -eq 2) {
                            $stageVal = "Play-off Semi-Final (Leg 2)"
                        } else {
                            $stageVal = "Play-off Semi-Final (Leg 1)"
                        }
                    } elseif ($isRegularLeague) {
                        $compName = $currentLeagueName
                        $leagueMatches = @($completedMatches | Where-Object {
                            $c = $_.competition_name
                            ($c -like "*$currentLeagueName*" -or $c -like "*League*" -or $c -like "*Championship*" -or $c -like "*Division*" -or $c -like "*Premier*") -and
                            ($c -notlike "*Play-off*") -and ($c -notlike "*Playoff*") -and ($c -notlike "*Cup*") -and ($c -notlike "*FA*") -and ($c -notlike "*Carabao*") -and ($c -notlike "*Trophy*")
                        })
                        $count = [Math]::Max(1, $leagueMatches.Count)
                        $stageVal = "Matchday $count"
                        $homePen = 0
                        $awayPen = 0
                        $isExtraTime = $false
                    } else {
                        # Cup Match (FA Cup, Carabao Cup, etc.)
                        $compName = $rawComp
                        $cupMatches = @($completedMatches | Where-Object { $_.competition_name -eq $rawComp })
                        $cCount = [Math]::Max(1, $cupMatches.Count)
                        if ($rawComp -like "*FA Cup*" -or $rawComp -like "*Emirates*") {
                            if ($cCount -ge 6) { $stageVal = "Final" }
                            elseif ($cCount -eq 5) { $stageVal = "Semi-Final" }
                            elseif ($cCount -eq 4) { $stageVal = "Quarter-Final" }
                            elseif ($cCount -eq 3) { $stageVal = "Round 5" }
                            elseif ($cCount -eq 2) { $stageVal = "Round 4" }
                            else { $stageVal = "Round 3" }
                        } elseif ($rawComp -like "*Carabao*" -or $rawComp -like "*EFL Cup*") {
                            if ($cCount -ge 6) { $stageVal = "Final" }
                            elseif ($cCount -eq 5) { $stageVal = "Semi-Final" }
                            elseif ($cCount -eq 4) { $stageVal = "Quarter-Final" }
                            else { $stageVal = "Round $cCount" }
                        } else {
                            $stageVal = "Round $cCount"
                        }
                    }

                    # Parse participants and identify which team index (0 or 1) belongs to the managed squad
                    $participants = @(Import-Csv -Path $participantsCsv -ErrorAction SilentlyContinue)
                    $count0 = 0
                    $count1 = 0
                    $maxMinutes = 0
                    foreach ($p in $participants) {
                        $pId = if ($p.player_id) { [int]$p.player_id } else { 0 }
                        $pTeam = if ($p.team_index) { [int]$p.team_index } else { 0 }
                        $pMins = if ($p.minutes_played) { [int]$p.minutes_played } else { 0 }
                        if ($pMins -gt $maxMinutes) { $maxMinutes = $pMins }
                        if ($managedSquadPlayerIds.Contains($pId)) {
                            if ($pTeam -eq 0) { $count0++ } else { $count1++ }
                        }
                    }

                    if ($count0 -gt $count1) {
                        $managedTeamIndex = 0
                        $oppTeamIndex = 1
                    } elseif ($count1 -gt $count0) {
                        $managedTeamIndex = 1
                        $oppTeamIndex = 0
                    } else {
                        $managedTeamIndex = if ($isHome) { 0 } else { 1 }
                        $oppTeamIndex = if ($managedTeamIndex -eq 0) { 1 } else { 0 }
                    }

                    # Parse real team totals from 18_match_teams_wide.csv
                    $teamRows = @(Import-Csv -Path $teamsCsv -ErrorAction SilentlyContinue)
                    $managedTeamRow = if ($teamRows.Count -gt $managedTeamIndex) { $teamRows[$managedTeamIndex] } else { $teamRows[0] }
                    $opponentTeamRow = if ($teamRows.Count -gt $oppTeamIndex) { $teamRows[$oppTeamIndex] } else { $teamRows[1] }

                    # Real Extra Time & Penalties extraction
                    $isPlayoffLeg1 = $isPlayoff -and ($stageVal -like "*Leg 1*")
                    if ($isRegularLeague -or $isPlayoffLeg1) {
                        $isExtraTime = $false
                        $homePen = 0
                        $awayPen = 0
                    } else {
                        $mShootout = if ($managedTeamRow -and $managedTeamRow.shootout_goals) { [int]$managedTeamRow.shootout_goals } else { 0 }
                        $oShootout = if ($opponentTeamRow -and $opponentTeamRow.shootout_goals) { [int]$opponentTeamRow.shootout_goals } else { 0 }
                        if ($mShootout -ge 255 -or $mShootout -lt 0) { $mShootout = 0 }
                        if ($oShootout -ge 255 -or $oShootout -lt 0) { $oShootout = 0 }
                        # In cups / playoffs: Extra time occurred ONLY if players logged >= 115 minutes or penalty shootout took place
                        $isExtraTime = ($maxMinutes -ge 115) -or ($mShootout -gt 0 -or $oShootout -gt 0)
                        if ($isHome) {
                            $homePen = $mShootout
                            $awayPen = $oShootout
                        } else {
                            $homePen = $oShootout
                            $awayPen = $mShootout
                        }
                    }
                    if ($homePen -ge 255 -or $homePen -lt 0) { $homePen = 0 }
                    if ($awayPen -ge 255 -or $awayPen -lt 0) { $awayPen = 0 }

                    # Determine Real Man of the Match directly from the engine flag
                    $topPlayer = ""
                    $highestRating = -1.0
                    foreach ($p in $participants) {
                        $pRating = if ($p.game_rating) { [double]$p.game_rating } else { 6.0 }
                        $isOfficialMotm = ($p.man_of_the_match -eq "true" -or $p.man_of_the_match -eq 1 -or $p.man_of_the_match -eq "1")
                        if ($isOfficialMotm -and $p.player_name) {
                            $topPlayer = $p.player_name
                            break
                        }
                        if ($pRating -gt $highestRating -and $p.player_name) {
                            $highestRating = $pRating
                            $topPlayer = $p.player_name
                        }
                    }

                    $shotsFor = if ($managedTeamRow -and $managedTeamRow.shots) { [int]$managedTeamRow.shots } else { [int]$managedScore }
                    $shotsAgainst = if ($opponentTeamRow -and $opponentTeamRow.shots) { [int]$opponentTeamRow.shots } else { [int]$opponentScore }
                    $xGF = if ($managedTeamRow -and $managedTeamRow.npk_expected_goals) { [double]$managedTeamRow.npk_expected_goals } else { 0.0 }
                    $xGA = if ($opponentTeamRow -and $opponentTeamRow.npk_expected_goals) { [double]$opponentTeamRow.npk_expected_goals } else { 0.0 }
                    $passesFor = if ($managedTeamRow -and $managedTeamRow.passes) { [int]$managedTeamRow.passes } else { 0 }
                    $passesAgainst = if ($opponentTeamRow -and $opponentTeamRow.passes) { [int]$opponentTeamRow.passes } else { 0 }
                    $passAcc = if ($managedTeamRow -and $managedTeamRow.pass_accuracy_pct_derived) { [int][double]$managedTeamRow.pass_accuracy_pct_derived } else { 0 }
                    $possession = if ($managedTeamRow -and $managedTeamRow.possession) { [int][double]$managedTeamRow.possession } `
                                  elseif ($managedTeamRow -and $managedTeamRow.possession_pct) { [int][double]$managedTeamRow.possession_pct } `
                                  elseif (($passesFor + $passesAgainst) -gt 0) { [int](($passesFor / ($passesFor + $passesAgainst)) * 100) } `
                                  else { 50 }

                    # Parse real player performances from 16_match_participants_wide.csv
                    $playerPerfs = @()
                    $goalDetails = @()

                    foreach ($p in $participants) {
                        $pTeam = [int]$p.team_index
                        if ($pTeam -eq $managedTeamIndex) {
                            $pName = $p.player_name
                            $pId = $p.player_id
                            $pGoals = if ($p.goals_derived) { [int]$p.goals_derived } elseif ($p.npk_goals) { [int]$p.npk_goals } else { 0 }
                            $pAssists = if ($p.assists) { [int]$p.assists } else { 0 }
                            $pRating = if ($p.game_rating) { [double]$p.game_rating } else { 6.5 }
                            $pPasses = if ($p.passes) { [int]$p.passes } else { 0 }
                            $pPassAcc = if ($p.pass_accuracy_pct_derived) { [int][double]$p.pass_accuracy_pct_derived } else { 0 }
                            $pShots = if ($p.shots) { [int]$p.shots } else { $pGoals }
                            $pShotAcc = if ($pShots -gt 0 -and $p.shots_on_target) { [int](([int]$p.shots_on_target / $pShots) * 100) } else { 0 }
                            $pTackles = if ($p.tackles) { [int]$p.tackles } else { 0 }
                            $pTacklesComp = if ($p.stand_tackles_won) { [int]$p.stand_tackles_won } elseif ($p.tackles_completed) { [int]$p.tackles_completed } else { $pTackles }
                            $pTacklePct = if ($p.stand_tackles -and [int]$p.stand_tackles -gt 0) { [int][double]$p.stand_tackle_success_pct_derived } elseif ($pTackles -gt 0) { [int](($pTacklesComp / $pTackles) * 100) } else { 80 }
                            $pInterceptions = if ($p.interceptions) { [int]$p.interceptions } else { 0 }
                            $pCleanSheet = ($opponentScore -eq 0)
                            $isMotm = ($p.player_name -eq $topPlayer -or $p.man_of_the_match -eq "true" -or $p.man_of_the_match -eq 1)

                            $playerPerfs += [PSCustomObject]@{
                                playerId = $pId
                                playerName = $pName
                                rating = $pRating
                                goals = $pGoals
                                assists = $pAssists
                                passes = $pPasses
                                passAccuracy = $pPassAcc
                                shots = $pShots
                                shotAccuracy = $pShotAcc
                                tackles = $pTackles
                                tacklePercentage = $pTacklePct
                                interceptions = $pInterceptions
                                cleanSheet = $pCleanSheet
                                yellowCard = ($p.yellow_card_events -and [int]$p.yellow_card_events -gt 0)
                                redCard = ($p.red_dismissals -and [int]$p.red_dismissals -gt 0)
                                isMotm = $isMotm
                            }

                            if ($pGoals -gt 0) {
                                for ($g = 1; $g -le $pGoals; $g++) {
                                    $goalDetails += [PSCustomObject]@{
                                        playerName = $pName
                                        minute = 15 + ($g * 22)
                                        isOpponent = $false
                                    }
                                }
                            }
                        }
                    }

                    # Add opponent goals
                    if ($opponentScore -gt 0) {
                        for ($og = 1; $og -le $opponentScore; $og++) {
                            $goalDetails += [PSCustomObject]@{
                                playerName = "$oppName Goal"
                                minute = 18 + ($og * 20)
                                isOpponent = $true
                            }
                        }
                    }

                    $etStr = if ($homePen -gt 0 -or $awayPen -gt 0) { " (Pens: $homePen-$awayPen)" } elseif ($isExtraTime) { " (A.E.T.)" } else { "" }
                    $msg = "Full Time: $managedClubName $(if ($isHome) { 'vs' } else { '@' }) $managedScore - $opponentScore $oppName ($compName - $stageVal)$etStr"
                    $matchPayload = [PSCustomObject]@{
                        dataType = "match"
                        title = "Live Match Final"
                        message = $msg
                        opponentName = $oppName
                        isHome = $isHome
                        goalsFor = $managedScore
                        goalsAgainst = $opponentScore
                        resultBadge = $resultBadge
                        date = $matchDate
                        competition = $compName
                        stage = $stageVal
                        isExtraTime = $isExtraTime
                        homePenalties = $homePen
                        awayPenalties = $awayPen
                        shotsFor = $shotsFor
                        shotsAgainst = $shotsAgainst
                        possession = $possession
                        passingAccuracy = $passAcc
                        expectedGoals = [Math]::Round($xGF, 2)
                        expectedGoalsAgainst = [Math]::Round($xGA, 2)
                        motmName = $topPlayer
                        leaguePosition = $(if ($currentTablePos -gt 0) { $currentTablePos } else { $null })
                        playerPerformances = $playerPerfs
                        goalDetails = $goalDetails
                    }

                    $jsonPayload = $matchPayload | ConvertTo-Json -Depth 6 -Compress
                    Add-TelemetryEvent -Title "Live Match Final" -Message $msg -RawPayload $jsonPayload

                    Write-Host "  -> ⚽ Imported Match: $msg" -ForegroundColor Green
                    Write-Host "     xG: $([Math]::Round($xGF, 2)) - $([Math]::Round($xGA, 2)) | MOTM: $topPlayer | Squad: $($playerPerfs.Count) players" -ForegroundColor Yellow

                    $global:ProcessedAtlasFolders.Add($folderId) | Out-Null
                }
            }
        }
    } catch {}
}

$asyncResult = $Listener.BeginGetContext($null, $null)
$lastAtlasCheck = [DateTime]::MinValue

while ($Listener.IsListening) {
    try {
        $now = [DateTime]::UtcNow
        if (($now - $lastAtlasCheck).TotalSeconds -ge 2) {
            $lastAtlasCheck = $now
            Check-AtlasExportFolder
        }

        if ($asyncResult.AsyncWaitHandle.WaitOne(800)) {
            $Context = $Listener.EndGetContext($asyncResult)
            $asyncResult = $Listener.BeginGetContext($null, $null)

            $Request = $Context.Request
            $Response = $Context.Response

        $clientIp = if ($Request.RemoteEndPoint) { $Request.RemoteEndPoint.Address.ToString() } else { "client" }
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Request from $clientIp : $($Request.HttpMethod) $($Request.Url.AbsolutePath)" -ForegroundColor DarkCyan

        # Add CORS Headers so web dashboard, curl, and Android app can connect freely
        $Response.Headers.Add("Access-Control-Allow-Origin", "*")
        $Response.Headers.Add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        $Response.Headers.Add("Access-Control-Allow-Headers", "*")

        if ($Request.HttpMethod -eq "OPTIONS") {
            $Response.StatusCode = 200
            $Response.Close()
            continue
        }

        $rawPath = $Request.Url.AbsolutePath.ToLower()

        if ($rawPath -eq "/test-match") {
            # Direct endpoint for generating a test match (GET or POST)
            $matchJson = Create-SampleMatchJson
            Add-TelemetryEvent -Title "Live Match Final" -Message "Full Time: vs 3 - 1 Arsenal (Premier League)" -RawPayload $matchJson
            Write-Host "  -> Queued sample match: Richmond 3 - 1 Arsenal" -ForegroundColor Yellow

            if ($Request.HttpMethod -eq "GET") {
                # Display friendly HTML redirect page
                $Response.StatusCode = 200
                $Response.ContentType = "text/html; charset=utf-8"
                $html = @"
<!DOCTYPE html>
<html>
<head><meta http-equiv="refresh" content="2;url=/" /><style>body{background:#0f172a;color:#f8fafc;font-family:sans-serif;padding:40px;text-align:center;}</style></head>
<body>
    <h2 style="color:#10b981;">✅ Test Match Sent! (Richmond 3 - 1 Arsenal)</h2>
    <p>Check your Android mobile app. Redirecting to dashboard in 2 seconds...</p>
    <p><a href="/" style="color:#38bdf8;">Click here if not redirected</a></p>
</body>
</html>
"@
                $buf = [System.Text.Encoding]::UTF8.GetBytes($html)
                $Response.ContentLength64 = $buf.Length
                $Response.OutputStream.Write($buf, 0, $buf.Length)
                $Response.Close()
            } else {
                $Response.StatusCode = 200
                $Response.ContentType = "application/json"
                $buf = [System.Text.Encoding]::UTF8.GetBytes('{"status":"ok","message":"Test match sent successfully!"}')
                $Response.ContentLength64 = $buf.Length
                $Response.OutputStream.Write($buf, 0, $buf.Length)
                $Response.Close()
            }
            continue
        }

        if ($rawPath -eq "/test-transfer") {
            # Direct endpoint for generating a test transfer (GET or POST)
            $transferJson = Create-SampleTransferJson
            Add-TelemetryEvent -Title "Transfer Finalized" -Message "Erling Haaland signed from Manchester City for €120.0M" -RawPayload $transferJson
            Write-Host "  -> Queued sample transfer: Erling Haaland €120.0M" -ForegroundColor Cyan

            if ($Request.HttpMethod -eq "GET") {
                $Response.StatusCode = 200
                $Response.ContentType = "text/html; charset=utf-8"
                $html = @"
<!DOCTYPE html>
<html>
<head><meta http-equiv="refresh" content="2;url=/" /><style>body{background:#0f172a;color:#f8fafc;font-family:sans-serif;padding:40px;text-align:center;}</style></head>
<body>
    <h2 style="color:#10b981;">✅ Test Transfer Sent! (€120M Haaland)</h2>
    <p>Check your Android mobile app. Redirecting to dashboard in 2 seconds...</p>
    <p><a href="/" style="color:#38bdf8;">Click here if not redirected</a></p>
</body>
</html>
"@
                $buf = [System.Text.Encoding]::UTF8.GetBytes($html)
                $Response.ContentLength64 = $buf.Length
                $Response.OutputStream.Write($buf, 0, $buf.Length)
                $Response.Close()
            } else {
                $Response.StatusCode = 200
                $Response.ContentType = "application/json"
                $buf = [System.Text.Encoding]::UTF8.GetBytes('{"status":"ok","message":"Test transfer sent successfully!"}')
                $Response.ContentLength64 = $buf.Length
                $Response.OutputStream.Write($buf, 0, $buf.Length)
                $Response.Close()
            }
            continue
        }

        if ($rawPath -eq "/clear" -or ($rawPath -eq "/events" -and $Request.HttpMethod -eq "DELETE")) {
            $global:EventList.Clear()
            try { "[]" | Set-Content $EventsFile -Encoding UTF8 } catch {}
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Cleared all telemetry events." -ForegroundColor Magenta
            if ($Request.HttpMethod -eq "GET") {
                $Response.Redirect("/")
                $Response.Close()
            } else {
                $Response.StatusCode = 200
                $Response.ContentType = "application/json"
                $buf = [System.Text.Encoding]::UTF8.GetBytes('{"status":"cleared"}')
                $Response.ContentLength64 = $buf.Length
                $Response.OutputStream.Write($buf, 0, $buf.Length)
                $Response.Close()
            }
            continue
        }

        if ($Request.HttpMethod -eq "POST") {
            $encoding = [System.Text.Encoding]::UTF8
            if ($Request.ContentEncoding) {
                $encoding = $Request.ContentEncoding
            }
            $Reader = New-Object System.IO.StreamReader($Request.InputStream, $encoding)
            $Body = $Reader.ReadToEnd()
            $Reader.Dispose()

            if (-not [string]::IsNullOrWhiteSpace($Body)) {
                $jsonObj = $null
                try {
                    $jsonObj = $Body | ConvertFrom-Json
                } catch {}

                $title = "Match Update"
                $msg = $Body
                if ($jsonObj -and $jsonObj.title) { $title = $jsonObj.title }
                if ($jsonObj -and $jsonObj.message) { $msg = $jsonObj.message }

                Add-TelemetryEvent -Title $title -Message $msg -RawPayload $Body
                if ($jsonObj -and $jsonObj.opponentName) {
                    Write-Host "  -> Result: $($jsonObj.goalsFor) - $($jsonObj.goalsAgainst) vs $($jsonObj.opponentName)" -ForegroundColor Yellow
                } elseif ($jsonObj -and $jsonObj.playerName) {
                    Write-Host "  -> Transfer: $($jsonObj.playerName) ($($jsonObj.type))" -ForegroundColor Cyan
                }
            }

            $Response.StatusCode = 200
            $Response.ContentType = "application/json"
            $buffer = [System.Text.Encoding]::UTF8.GetBytes('{"status":"ok"}')
            $Response.ContentLength64 = $buffer.Length
            $Response.OutputStream.Write($buffer, 0, $buffer.Length)
            $Response.Close()
        } elseif ($Request.HttpMethod -eq "GET") {
            if ($rawPath -eq "/events" -or $rawPath -eq "/json" -or $rawPath -eq "/api/telemetry") {
                $Response.StatusCode = 200
                $Response.ContentType = "application/json"
                $jsonArray = "[" + ($global:EventList -join ",") + "]"
                $buffer = [System.Text.Encoding]::UTF8.GetBytes($jsonArray)
                $Response.ContentLength64 = $buffer.Length
                $Response.OutputStream.Write($buffer, 0, $buffer.Length)
                $Response.Close()
            } else {
                # Return Web UI Status Dashboard
                $Response.StatusCode = 200
                $Response.ContentType = "text/html; charset=utf-8"
                $eventCount = $global:EventList.Count
                $html = @"
<!DOCTYPE html>
<html>
<head>
    <title>EA FC Telemetry Bridge</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 24px; margin: 0; }
        .card { background: #1e293b; border-radius: 14px; padding: 24px; max-width: 680px; margin: 0 auto; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); }
        h1 { color: #38bdf8; margin-top: 0; font-size: 22px; display: flex; align-items: center; gap: 8px; }
        .status { display: inline-block; background: #059669; color: white; padding: 4px 12px; border-radius: 9999px; font-weight: bold; font-size: 13px; margin-bottom: 16px; }
        .info { background: #0f172a; padding: 14px; border-radius: 8px; font-family: monospace; margin: 14px 0; border: 1px solid #334155; line-height: 1.6; }
        .btn-group { display: flex; gap: 10px; margin: 16px 0; flex-wrap: wrap; }
        button, a.btn { background: #0284c7; color: white; border: none; padding: 10px 16px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 13px; transition: background 0.2s; text-decoration: none; display: inline-block; }
        button:hover, a.btn:hover { background: #0369a1; }
        button.btn-green, a.btn-green { background: #10b981; }
        button.btn-green:hover, a.btn-green:hover { background: #059669; }
        button.btn-danger, a.btn-danger { background: #ef4444; }
        button.btn-danger:hover, a.btn-danger:hover { background: #dc2626; }
        .events-box { max-height: 320px; overflow-y: auto; background: #0f172a; border-radius: 8px; padding: 12px; border: 1px solid #334155; margin-top: 14px; }
        .event-item { border-bottom: 1px solid #1e293b; padding: 8px 0; font-size: 13px; }
        .event-item:last-child { border-bottom: none; }
        .event-time { color: #94a3b8; font-size: 11px; font-family: monospace; }
        .status-msg { margin: 10px 0; padding: 8px 12px; border-radius: 6px; font-size: 13px; min-height: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>⚽ EA Sports FC Telemetry Bridge</h1>
        <div class="status">🟢 Bridge Active (Listening on Port $Port)</div>

        <div class="info">
            <strong>📱 IP Address for Android App:</strong><br>
            <span style="color:#10b981;font-size:16px;font-weight:bold;">http://${primaryIp}:${Port}</span><br>
        </div>

        <div id="statusMsg" class="status-msg"></div>

        <h3>⚡ Quick Transmission Testing</h3>
        <p style="font-size:12px;color:#94a3b8;margin-top:-6px;">Click either button to immediately send a match or transfer to your phone.</p>
        <div class="btn-group">
            <button class="btn-green" onclick="sendTestMatch()">⚡ Send Test Match (3 - 1 vs Arsenal)</button>
            <button onclick="sendTestTransfer()">⚡ Send Test Transfer (€120M Haaland)</button>
            <button class="btn-danger" onclick="clearEvents()">🗑️ Clear Events</button>
        </div>

        <p style="font-size:11px;color:#64748b;">
            Direct links: 
            <a href="/test-match" style="color:#38bdf8;">[Send Match]</a> | 
            <a href="/test-transfer" style="color:#38bdf8;">[Send Transfer]</a> | 
            <a href="/events" target="_blank" style="color:#38bdf8;">[View Raw JSON]</a>
        </p>

        <h3>📡 Live Events Stream (<span id="eventCount">$eventCount</span> queued)</h3>
        <div class="events-box" id="eventsList">
            <div style="color:#64748b;text-align:center;padding:20px;">Loading events...</div>
        </div>
    </div>

    <script>
        function sendTestMatch() {
            const msg = document.getElementById('statusMsg');
            msg.innerHTML = '<span style="color:#38bdf8;">Sending test match...</span>';
            fetch('/test-match', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    msg.innerHTML = '<span style="color:#10b981;font-weight:bold;">✅ Test match sent successfully! Check your phone.</span>';
                    setTimeout(updateEvents, 300);
                })
                .catch(err => {
                    msg.innerHTML = '<span style="color:#ef4444;font-weight:bold;">❌ Error: ' + err + ' (Trying direct redirect...)</span>';
                    window.location.href = '/test-match';
                });
        }

        function sendTestTransfer() {
            const msg = document.getElementById('statusMsg');
            msg.innerHTML = '<span style="color:#38bdf8;">Sending test transfer...</span>';
            fetch('/test-transfer', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    msg.innerHTML = '<span style="color:#10b981;font-weight:bold;">✅ Test transfer sent successfully! Check your phone.</span>';
                    setTimeout(updateEvents, 300);
                })
                .catch(err => {
                    msg.innerHTML = '<span style="color:#ef4444;font-weight:bold;">❌ Error: ' + err + ' (Trying direct redirect...)</span>';
                    window.location.href = '/test-transfer';
                });
        }

        function clearEvents() {
            if (confirm("Clear all recorded telemetry events?")) {
                fetch('/clear', { method: 'POST' })
                    .then(() => location.reload())
                    .catch(() => { window.location.href = '/clear'; });
            }
        }

        function updateEvents() {
            fetch('/events')
                .then(r => r.json())
                .then(events => {
                    document.getElementById('eventCount').innerText = events.length;
                    const container = document.getElementById('eventsList');
                    if (events.length === 0) {
                        container.innerHTML = '<div style="color:#64748b;text-align:center;padding:20px;">No events recorded yet. Play a match in EA FC or click a test button above.</div>';
                        return;
                    }
                    container.innerHTML = events.slice().reverse().map(ev => {
                        const dateStr = new Date(ev.time * 1000).toLocaleTimeString();
                        let summary = ev.title;
                        try {
                            const parsed = JSON.parse(ev.message);
                            if (parsed.message) summary = parsed.message;
                        } catch {}
                        return '<div class="event-item">' +
                            '<span class="event-time">[' + dateStr + ']</span> ' +
                            '<strong>' + (ev.title || 'Update') + '</strong><br>' +
                            '<span style="color:#cbd5e1;">' + summary + '</span>' +
                        '</div>';
                    }).join('');
                })
                .catch(err => {
                    document.getElementById('eventsList').innerHTML = '<div style="color:#ef4444;text-align:center;">Failed to load events: ' + err + '</div>';
                });
        }

        updateEvents();
        setInterval(updateEvents, 4000);
    </script>
</body>
</html>
"@
                $buffer = [System.Text.Encoding]::UTF8.GetBytes($html)
                $Response.ContentLength64 = $buffer.Length
                $Response.OutputStream.Write($buffer, 0, $buffer.Length)
                $Response.Close()
            }
        }
        }
    } catch {
        try {
            $Response.StatusCode = 500
            $Response.Close()
        } catch {}
        Start-Sleep -Milliseconds 50
    }
}
