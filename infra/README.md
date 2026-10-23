# MockMate — AWS Production Infrastructure Guide

This directory contains the production-ready AWS CloudFormation infrastructure template and configuration parameters for **MockMate**.

---

## 1. Selected Architecture & Design Decisions

MockMate is architected for reliable, cost-effective, and secure operation on AWS:

```
                                  [ Internet Traffic ]
                                           │
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │    Application Load Balancer (ALB)      │
                      │    - Port 80 (HTTP) & 443 (HTTPS)       │
                      └────────────────────┬────────────────────┘
                                           │
                     ┌─────────────────────┴─────────────────────┐
                     │ Path: /api/*                              │ Path: /*
                     ▼                                           ▼
       ┌───────────────────────────┐               ┌───────────────────────────┐
       │   ECS Fargate: Backend    │               │   ECS Fargate: Frontend   │
       │   FastAPI (Port 8000)     │               │   Next.js 16 (Port 3000)  │
       └─────────────┬─────────────┘               └───────────────────────────┘
                     │
                     │ Port 5432 (Private DB Subnet Only)
                     ▼
       ┌───────────────────────────┐
       │   Amazon RDS PostgreSQL   │
       │   (Single-AZ, Private)    │
       └───────────────────────────┘
```

### Key Decisions:

1. **Shared Application Load Balancer with Path-Based Routing**:
   - `/*` forwards to Next.js Frontend container (port 3000).
   - `/api/*` forwards to FastAPI Backend container (port 8000).
   - **Benefit**: Eliminates cross-origin CORS errors because both frontend and API share the exact same domain origin (`http://<ALB_DNS>/` and `http://<ALB_DNS>/api/...`).

2. **Next.js 16 Container Hosting on ECS Fargate vs. AWS Amplify**:
   - MockMate utilizes **Next.js 16.4.0 with React 19** and experimental caching features (`cacheComponents: true`, `partialPrefetching: true`).
   - Standard AWS Amplify SSR compute adapters natively target Next.js 13/14 and can encounter bundling incompatibilities with Next.js 16 canary/app router features.
   - Containerizing Next.js inside ECS Fargate ensures 100% runtime parity with local testing, predictable builds, and zero framework version limitations.

3. **Student Budget & Cost Optimization**:
   - **RDS**: Utilizes `db.t4g.micro` with 20 GB gp3 storage (eligible for AWS 12-Month Free Tier).
   - **ECS Fargate**: Tasks sized at 0.25 vCPU (256 units) and 0.5 GB RAM (512 MB).
   - **Networking**: Fargate tasks are assigned public IPs within public subnets, but **inbound traffic is strictly restricted by Security Groups to the ALB only**. This eliminates the need for an expensive AWS NAT Gateway (~$32.40/month per AZ, saving ~$65/month), keeping the entire infrastructure affordable for student projects.
   - **Database**: Strictly isolated in private database subnets with no public accessibility.

4. **Secrets Management**:
   - Database credentials and `SECRET_KEY` are stored in **AWS Secrets Manager** and injected into container environments securely via ECS Task Definition secrets integration.
   - Server secrets are never baked into container images or exposed to client JavaScript.

---

## 2. Directory Contents

- `template.yaml`: Complete AWS CloudFormation infrastructure template.
- `parameters.example.json`: Parameter values template for CloudFormation deployments.
- `README.md`: This architecture and deployment guide.

---

## 3. Deployment Guide (Step-by-Step)

### Prerequisites:
- AWS Account with administrative access.
- [AWS CLI](https://aws.amazon.com/cli/) installed and configured (`aws configure`).
- Docker installed and running locally (for building & pushing container images).

### Step 1: Create ECR Repositories & Deploy Stack Base

1. Copy and customize the parameters file:
   ```bash
   cp infra/parameters.example.json infra/parameters.json
   ```
   Edit `infra/parameters.json` and set your `DBPassword` and `JwtSecretKey`.

2. Deploy the CloudFormation stack:
   ```bash
   aws cloudformation create-stack \
     --stack-name mockmate-prod \
     --template-body file://infra/template.yaml \
     --parameters file://infra/parameters.json \
     --capabilities CAPABILITY_NAMED_IAM \
     --region us-east-1
   ```

3. Wait for the stack creation to complete:
   ```bash
   aws cloudformation wait stack-create-complete \
     --stack-name mockmate-prod \
     --region us-east-1
   ```

### Step 2: Build & Push Docker Images to Amazon ECR

1. Retrieve your AWS Account ID and authenticate Docker with ECR:
   ```bash
   AWS_REGION="us-east-1"
   AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
   aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
   ```

2. Build and push the Backend Docker image:
   ```bash
   docker build -t mockmate-prod-backend:latest ./backend
   docker tag mockmate-prod-backend:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/mockmate-prod-backend:latest
   docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/mockmate-prod-backend:latest
   ```

3. Build and push the Frontend Docker image:
   ```bash
   docker build -t mockmate-prod-frontend:latest ./frontend
   docker tag mockmate-prod-frontend:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/mockmate-prod-frontend:latest
   docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/mockmate-prod-frontend:latest
   ```

4. Force new deployment of ECS services to pick up latest images:
   ```bash
   aws ecs update-service --cluster mockmate-prod-cluster --service mockmate-prod-backend-service --force-new-deployment --region us-east-1
   aws ecs update-service --cluster mockmate-prod-cluster --service mockmate-prod-frontend-service --force-new-deployment --region us-east-1
   ```

---

## 4. Post-Deployment Verification

1. Get the Load Balancer DNS output:
   ```bash
   aws cloudformation describe-stacks \
     --stack-name mockmate-prod \
     --query "Stacks[0].Outputs[?OutputKey=='FrontendApplicationURL'].OutputValue" \
     --output text \
     --region us-east-1
   ```

2. Verify Health Check:
   ```bash
   curl http://<ALB-DNS-NAME>/api/health
   # Expected: {"status":"online","service":"MockMate API","database":"healthy"}
   ```

3. Verify OpenAPI Docs:
   - Open `http://<ALB-DNS-NAME>/api/docs` in your browser.

4. Verify User Registration & Login:
   - Visit `http://<ALB-DNS-NAME>/register` and register a new test user.
   - Verify immediate redirection to `http://<ALB-DNS-NAME>/dashboard`.
   - Refresh the page to verify session restoration.
   - Click "Sign Out" to verify logout and token invalidation.

---

## 5. Cost & Resource Review

| Resource | Configuration | AWS Monthly Estimate |
|---|---|---|
| Amazon RDS PostgreSQL | `db.t4g.micro`, 20GB gp3 storage | $0.00 (within 12-mo Free Tier) or ~$14.50/mo |
| AWS Fargate Backend | 0.25 vCPU, 0.5 GB RAM | ~$9.50/mo |
| AWS Fargate Frontend | 0.25 vCPU, 0.5 GB RAM | ~$9.50/mo |
| Application Load Balancer | 1 ALB, low traffic | ~$18.00/mo |
| Amazon ECR & CloudWatch | < 5 GB storage, 14-day log retention | < $1.00/mo |
| AWS Secrets Manager | 1 secret | ~$0.40/mo |
| **Total Estimated** | | **~$38 - $52 / month** |
