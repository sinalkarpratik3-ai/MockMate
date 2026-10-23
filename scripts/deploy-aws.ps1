<#
.SYNOPSIS
    Deploy MockMate infrastructure and container applications to AWS.
.DESCRIPTION
    Automates CloudFormation stack deployment, Docker builds, ECR pushes, and ECS service updates.
.PARAMETER Region
    AWS region (defaults to us-east-1).
.PARAMETER StackName
    CloudFormation stack name (defaults to mockmate-prod).
.PARAMETER ParametersFile
    Path to JSON parameters file (defaults to infra/parameters.json).
#>

[CmdletBinding()]
param(
    [string]$Region = "us-east-1",
    [string]$StackName = "mockmate-prod",
    [string]$ParametersFile = "infra/parameters.json",
    [switch]$SkipImageBuild
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " MockMate AWS Deployment Script" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Prerequisite verification
Write-Host "[1/6] Verifying prerequisites..." -ForegroundColor Yellow
if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    Write-Error "AWS CLI is not installed or not in PATH. Please install it from https://aws.amazon.com/cli/."
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue) -and -not $SkipImageBuild) {
    Write-Error "Docker is not installed or not in PATH. Please install Docker Desktop or run with -SkipImageBuild."
}

# 2. Check AWS credentials
Write-Host "[2/6] Verifying AWS credentials in region $Region..." -ForegroundColor Yellow
$CallerIdentity = aws sts get-caller-identity --output json | ConvertFrom-Json
$AccountId = $CallerIdentity.Account
Write-Host "      Authenticated as AWS Account: $AccountId" -ForegroundColor Green

# 3. Parameters file check
if (-not (Test-Path $ParametersFile)) {
    if (Test-Path "infra/parameters.example.json") {
        Write-Warning "Parameters file '$ParametersFile' not found. Creating from 'infra/parameters.example.json'..."
        Copy-Item "infra/parameters.example.json" $ParametersFile
        Write-Warning "Please review and customize '$ParametersFile' (especially DBPassword and JwtSecretKey) before continuing."
        Exit 1
    } else {
        Write-Error "Parameters file not found at $ParametersFile."
    }
}

# 4. Validate CloudFormation Template
Write-Host "[3/6] Validating CloudFormation template..." -ForegroundColor Yellow
aws cloudformation validate-template --template-body file://infra/template.yaml --region $Region | Out-Null
Write-Host "      Template syntax is valid." -ForegroundColor Green

# 5. Deploy / Update CloudFormation Stack
Write-Host "[4/6] Deploying CloudFormation stack '$StackName'..." -ForegroundColor Yellow
$StackExists = $false
try {
    $describe = aws cloudformation describe-stacks --stack-name $StackName --region $Region 2>&1
    if ($LASTEXITCODE -eq 0) { $StackExists = $true }
} catch {
    $StackExists = $false
}

if ($StackExists) {
    Write-Host "      Stack exists. Executing stack update..." -ForegroundColor Cyan
    aws cloudformation update-stack `
        --stack-name $StackName `
        --template-body file://infra/template.yaml `
        --parameters file://$ParametersFile `
        --capabilities CAPABILITY_NAMED_IAM `
        --region $Region
    Write-Host "      Waiting for stack update to complete..." -ForegroundColor Cyan
    aws cloudformation wait stack-update-complete --stack-name $StackName --region $Region
} else {
    Write-Host "      Creating fresh stack '$StackName'..." -ForegroundColor Cyan
    aws cloudformation create-stack `
        --stack-name $StackName `
        --template-body file://infra/template.yaml `
        --parameters file://$ParametersFile `
        --capabilities CAPABILITY_NAMED_IAM `
        --region $Region
    Write-Host "      Waiting for stack creation to complete (this may take ~8-12 minutes for RDS)..." -ForegroundColor Cyan
    aws cloudformation wait stack-create-complete --stack-name $StackName --region $Region
}

# Retrieve Stack Outputs
$Outputs = aws cloudformation describe-stacks --stack-name $StackName --region $Region --query "Stacks[0].Outputs" --output json | ConvertFrom-Json
$AlbDns = ($Outputs | Where-Object { $_.OutputKey -eq "LoadBalancerDNS" }).OutputValue
$BackendEcr = ($Outputs | Where-Object { $_.OutputKey -eq "BackendECRRepositoryURI" }).OutputValue
$FrontendEcr = ($Outputs | Where-Object { $_.OutputKey -eq "FrontendECRRepositoryURI" }).OutputValue

Write-Host "      ALB DNS Endpoint: $AlbDns" -ForegroundColor Green

# 6. Build and Push Container Images (if not skipped)
if (-not $SkipImageBuild) {
    Write-Host "[5/6] Authenticating Docker with ECR..." -ForegroundColor Yellow
    aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin "$AccountId.dkr.ecr.$Region.amazonaws.com"

    Write-Host "      Building and pushing Backend image to $BackendEcr..." -ForegroundColor Yellow
    docker build -t "$BackendEcr:latest" ./backend
    docker push "$BackendEcr:latest"

    Write-Host "      Building and pushing Frontend image to $FrontendEcr..." -ForegroundColor Yellow
    docker build --build-arg NEXT_PUBLIC_API_URL="/api" -t "$FrontendEcr:latest" ./frontend
    docker push "$FrontendEcr:latest"

    Write-Host "[6/6] Triggering ECS service updates..." -ForegroundColor Yellow
    aws ecs update-service --cluster "$StackName-cluster" --service "$StackName-backend-service" --force-new-deployment --region $Region | Out-Null
    aws ecs update-service --cluster "$StackName-cluster" --service "$StackName-frontend-service" --force-new-deployment --region $Region | Out-Null
    Write-Host "      ECS deployments initiated." -ForegroundColor Green
} else {
    Write-Host "[5/6] Skipping image build as requested." -ForegroundColor Yellow
    Write-Host "[6/6] Skipped ECS deployment update." -ForegroundColor Yellow
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " Deployment Complete!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host " Frontend URL:    http://$AlbDns" -ForegroundColor Cyan
Write-Host " Backend API:     http://$AlbDns/api" -ForegroundColor Cyan
Write-Host " Health Check:    http://$AlbDns/api/health" -ForegroundColor Cyan
Write-Host " API Docs:        http://$AlbDns/api/docs" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Green
