## 🚀 Deployment

Stock Busters is deployed on **Google Kubernetes Engine (GKE)** using **Pulumi** for infrastructure-as-code.

### Architecture

- **Frontend**: Next.js application
- **API Service**: FastAPI backend with AI-powered stock analysis
- **Infrastructure**: GKE cluster with NGINX Ingress and Workload Identity
- **Cloud Services**: Google Cloud Storage, Vertex AI, Artifact Registry

### Quick Deployment

#### Prerequisites
- Docker Desktop
- Google Cloud SDK
- GCP project with billing enabled
- Service account with appropriate IAM roles

#### Deploy in 3 Steps

**1. Setup Deployment Container**
```bash
cd src/deployment
sh docker-shell.sh
```

**2. Build and Push Images (~15-20 min)**
```bash
cd /app/deploy_images
pulumi stack select dev
pulumi up
```

**3. Deploy to Kubernetes (~20-25 min)**
```bash
cd /app/deploy_k8s
pulumi stack select dev
pulumi up
```

**Access your application:**
```bash
pulumi stack output app_url
# Example: http://34.60.47.248.sslip.io
```

### Deployment Features

✅ **Autoscaling**: 1-3 nodes based on demand  
✅ **Zero-downtime updates**: Rolling deployments  
✅ **Secure authentication**: Workload Identity (no embedded keys)  
✅ **Load balancing**: NGINX Ingress Controller  
✅ **Infrastructure as Code**: Declarative Pulumi configuration  

### Quick Commands
```bash
# Check deployment status
kubectl get pods -n stockbusters-app-namespace

# View logs
kubectl logs -f deployment/api -n stockbusters-app-namespace

# Update application
kubectl rollout restart deployment/api -n stockbusters-app-namespace

# Cleanup
cd /app/deploy_k8s && pulumi destroy
```

### Cost Estimate
- **Monthly**: ~$116-166 (GKE cluster, nodes, load balancer)
- **Optimization**: Use preemptible nodes, smaller machine types, or GKE Autopilot

### Detailed Documentation

For complete deployment instructions, troubleshooting, and configuration details, see [src/deployment/README.md](src/deployment/README.md)

**Live Demo:** http://34.60.47.248.sslip.io
