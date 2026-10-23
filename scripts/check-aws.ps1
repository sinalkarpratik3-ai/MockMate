<#
.SYNOPSIS
    Validate MockMate AWS live deployment endpoints and authentication.
.PARAMETER BaseUrl
    Base URL of the MockMate Application Load Balancer (e.g. http://mockmate-alb-xxx.us-east-1.elb.amazonaws.com)
.PARAMETER StackName
    CloudFormation stack name (defaults to mockmate-prod). If BaseUrl is not provided, queries ALB DNS from CloudFormation.
.PARAMETER Region
    AWS region (defaults to us-east-1).
#>

[CmdletBinding()]
param(
    [string]$BaseUrl = "",
    [string]$StackName = "mockmate-prod",
    [string]$Region = "us-east-1"
)

$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " MockMate AWS Live Verification Script" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Resolve Base URL
if (-not $BaseUrl) {
    if (Get-Command aws -ErrorAction SilentlyContinue) {
        Write-Host "Querying ALB DNS from CloudFormation stack '$StackName'..." -ForegroundColor Yellow
        $AlbDns = aws cloudformation describe-stacks `
            --stack-name $StackName `
            --query "Stacks[0].Outputs[?OutputKey=='LoadBalancerDNS'].OutputValue" `
            --output text `
            --region $Region 2>$null

        if ($AlbDns -and $AlbDns -ne "None") {
            $BaseUrl = "http://$AlbDns"
            Write-Host "Resolved BaseUrl: $BaseUrl" -ForegroundColor Green
        }
    }
}

if (-not $BaseUrl) {
    Write-Error "Please specify -BaseUrl (e.g. http://mockmate-alb-12345.us-east-1.elb.amazonaws.com)"
    Exit 1
}

$BaseUrl = $BaseUrl.TrimEnd("/")
Write-Host "Testing MockMate endpoints at: $BaseUrl`n" -ForegroundColor Cyan

$Passed = 0
$Failed = 0

function Run-Check {
    param(
        [string]$Name,
        [scriptblock]$Action
    )
    Write-Host -NoNewline "[$Name] ... "
    try {
        & $Action
        Write-Host "PASS" -ForegroundColor Green
        $script:Passed++
    } catch {
        Write-Host "FAIL: $_" -ForegroundColor Red
        $script:Failed++
    }
}

# 1. Health check
Run-Check "GET /api/health" {
    $res = Invoke-RestMethod -Uri "$BaseUrl/api/health" -Method Get -TimeoutSec 15
    if ($res.status -ne "online") { throw "Status was not 'online': $($res | ConvertTo-Json)" }
    if ($res.database -notmatch "healthy") { throw "Database is unhealthy: $($res.database)" }
}

# 2. Frontend root
Run-Check "GET / (Frontend Root)" {
    $res = Invoke-WebRequest -Uri "$BaseUrl/" -Method Get -TimeoutSec 15
    if ($res.StatusCode -ne 200) { throw "HTTP Status $($res.StatusCode)" }
}

# 3. Swagger Docs
Run-Check "GET /api/docs (OpenAPI Documentation)" {
    $res = Invoke-WebRequest -Uri "$BaseUrl/api/docs" -Method Get -TimeoutSec 15
    if ($res.StatusCode -ne 200) { throw "HTTP Status $($res.StatusCode)" }
}

# 4. User Registration
$Timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$TestEmail = "aws_verifier_$Timestamp@mockmate.test"
$TestPassword = "TestPassword123!"
$TestToken = ""

Run-Check "POST /api/auth/register (User Registration)" {
    $body = @{
        email = $TestEmail
        password = $TestPassword
        full_name = "AWS Automated Verifier"
    } | ConvertTo-Json

    $res = Invoke-RestMethod -Uri "$BaseUrl/api/auth/register" -Method Post -ContentType "application/json" -Body $body -TimeoutSec 15
    if (-not $res.access_token) { throw "Response missing access_token" }
    if ($res.user.email -ne $TestEmail) { throw "Response email mismatch" }
    $script:TestToken = $res.access_token
}

# 5. User Login
Run-Check "POST /api/auth/login (User Authentication)" {
    $body = @{
        email = $TestEmail
        password = $TestPassword
    } | ConvertTo-Json

    $res = Invoke-RestMethod -Uri "$BaseUrl/api/auth/login" -Method Post -ContentType "application/json" -Body $body -TimeoutSec 15
    if (-not $res.access_token) { throw "Response missing access_token" }
}

# 6. Session Restoration / Current User
Run-Check "GET /api/auth/me (Session Verification)" {
    $headers = @{
        Authorization = "Bearer $script:TestToken"
    }
    $res = Invoke-RestMethod -Uri "$BaseUrl/api/auth/me" -Method Get -Headers $headers -TimeoutSec 15
    if ($res.email -ne $TestEmail) { throw "Session email mismatch: $($res.email)" }
}

# 7. Unauthenticated Rejection
Run-Check "GET /api/auth/me (Security: Unauthenticated 401)" {
    try {
        $res = Invoke-WebRequest -Uri "$BaseUrl/api/auth/me" -Method Get -TimeoutSec 15 2>&1
        throw "Expected 401 but request succeeded with status $($res.StatusCode)"
    } catch {
        if ($_.Exception.Response.StatusCode -eq 401 -or $_.ToString() -match "401") {
            # Expected 401
        } else {
            throw $_
        }
    }
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Verification Summary: $Passed Passed, $Failed Failed" -ForegroundColor $(if ($Failed -eq 0) { "Green" } else { "Red" })
Write-Host "==========================================================" -ForegroundColor Cyan
