# Deploying Stock Busters: Container to Kubernetes with Pulumi

## Introduction

We deployed **Stock Busters**, an AI-powered financial investment platform, using **Pulumi** for infrastructure-as-code and **Google Kubernetes Engine (GKE)** for orchestration. Our stack includes a Next.js frontend and FastAPI backend, all containerized and managed through declarative infrastructure.

---

## Architecture Overview

**Components:**
- **Frontend**: Next.js application (port 3000)
- **API Service**: FastAPI backend with AI recommendations (port 9000)
- **Infrastructure**: GKE cluster with NGINX Ingress and Workload Identity

**Tech Stack:** Pulumi (Python), Docker, Kubernetes, GCP, Artifact Registry

---

## Deployment with Pulumi

We organized our deployment into two Pulumi projects:

### 1. Image Building (`deploy_images`)

Builds Docker images and pushes them to Google Artifact Registry:
```python
# Build and push API image
api_image = docker_build.Image(
    "stockbusters-api-service",
    tags=[f"{registry_url}/api:{timestamp}"],
    context=docker_build.BuildContextArgs(location="../api-service"),
    push=True
)

# Build and push frontend
frontend_image = docker_build.Image(
    "stockbusters-frontend",
    tags=[f"{registry_url}/frontend:{timestamp}"],
    context=docker_build.BuildContextArgs(location="../frontend"),
    push=True
)
```

**Running the deployment:**
```bash
cd deploy_images
pulumi up
```

**Duration:** ~15-20 minutes (first run)

### 2. Kubernetes Deployment (`deploy_k8s`)

Provisions complete GKE infrastructure:

**Key Steps:**
1. **Create VPC Network** - Subnet, router, and Cloud NAT
2. **Provision GKE Cluster** - With Workload Identity enabled
3. **Deploy Node Pool** - Autoscaling from 1-3 nodes (e2-medium)
4. **Deploy Applications** - Frontend and API as Kubernetes deployments
5. **Install NGINX Ingress** - External load balancer
6. **Configure Routing** - Ingress rules for traffic management
```python
# Create GKE cluster with autoscaling
cluster = container.Cluster(
    "stockbusters-app-cluster",
    location="us-central1",
    initial_node_count=1,
    workload_identity_config=container.ClusterWorkloadIdentityConfigArgs(
        workload_pool=f"{project}.svc.id.goog"
    )
)

node_pool = container.NodePool(
    "stockbusters-app-pool",
    cluster=cluster.name,
    autoscaling=container.NodePoolAutoscalingArgs(
        min_node_count=1,
        max_node_count=3
    )
)
```

**Running the deployment:**
```bash
cd deploy_k8s
pulumi up
```

**Duration:** ~20-25 minutes

---

## Deployment Process

### Step 1: Setup Deployment Container
```bash
cd src/deployment
sh docker-shell.sh  # Includes Pulumi, kubectl, gcloud CLI
```

### Step 2: Build Images
```bash
cd /app/deploy_images
pulumi stack select dev
pulumi up
```
Creates Artifact Registry repository, builds images, and pushes with timestamp tags.

### Step 3: Deploy to Kubernetes
```bash
cd /app/deploy_k8s
pulumi stack select dev
pulumi up
```
Provisions entire infrastructure and deploys application.

### Step 4: Access Application
```
http://<EXTERNAL-IP>.sslip.io
```
Example: `http://34.60.47.248.sslip.io`

---

## Demonstrating Scalability and Load Balancing

One of the key advantages of Kubernetes is its ability to scale applications seamlessly. We conducted live tests to demonstrate both horizontal pod scaling and load balancing capabilities.

### Initial State

Before scaling, our application ran with minimal resources:
```
NAME                      READY   STATUS    RESTARTS   AGE
api-5b876fcbb8-kdcfm      1/1     Running   0          46m
frontend-6d98787d89-mxhks 1/1     Running   0          47m
```

**Resource Usage:**
- Node CPU: 4%
- Node Memory: 54%
- 1 API pod, 1 Frontend pod

### Scaling Operation

Using a single kubectl command, we scaled both services to 3 replicas:
```bash
kubectl scale deployment/api --replicas=3 -n stockbusters-app-namespace
kubectl scale deployment/frontend --replicas=3 -n stockbusters-app-namespace
```

Within 60 seconds, all new pods were running and ready to serve traffic:
```
NAME                          READY   STATUS    RESTARTS   AGE
api-5b876fcbb8-55djf          1/1     Running   0          61s
api-5b876fcbb8-648wr          1/1     Running   0          61s
api-5b876fcbb8-kdcfm          1/1     Running   0          48m
frontend-6d98787d89-65gjq     1/1     Running   0          60s
frontend-6d98787d89-dljc5     1/1     Running   0          60s
frontend-6d98787d89-mxhks     1/1     Running   0          48m
```

**Key observation:** Zero downtime during the scaling operation.

### Load Testing Results

We used Apache Bench to simulate real-world traffic with 1,000 requests and 50 concurrent connections:
```bash
ab -n 1000 -c 50 http://34.60.47.248.sslip.io/
```

**Results:**

| Metric | Value |
|--------|-------|
| Requests per second | **136.18 req/sec** |
| Mean response time | 367 ms |
| Failed requests | **0 (100% success)** |
| Response time (50th percentile) | 335ms |
| Response time (90th percentile) | 445ms |
| Response time (99th percentile) | 593ms |

### Load Balancing Evidence

After scaling, we observed CPU usage distributed across all pods, confirming load balancing:
```
NAME                      CPU(cores)   MEMORY(bytes)
api-5b876fcbb8-55djf      796m         546Mi
api-5b876fcbb8-648wr      595m         538Mi
api-5b876fcbb8-kdcfm      2m           551Mi
```

The varying CPU usage proves that NGINX Ingress is distributing requests across different backend pods.

### Scaling Comparison

| Aspect | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total Pods | 2 | 6 | **3x** |
| Request Success Rate | 100% | 100% | Maintained |
| Failed Requests | 0 | 0 | **0%** |
| Scaling Time | - | 60s | Fast |
| Downtime | - | 0s | **Zero** |

---

## Key Technical Challenges

### Challenge 1: Workload Identity for Secure GCP Access

**Problem:** API needed secure access to Google Cloud Storage and Vertex AI.

**Solution:** Configured Workload Identity to bind Kubernetes service accounts to GCP service accounts without embedding keys.

Required IAM roles:
- Service Account Token Creator
- Storage Admin  
- Vertex AI User

### Challenge 2: Service Account Permissions

**Problem:** `403 Forbidden` errors during node pool creation.

**Solution:** Ensured deployment service account had:
- Kubernetes Engine Admin
- Service Account Admin
- Artifact Registry Administrator

### Challenge 3: Docker Credential Conflicts

**Problem:** Local Docker credential store conflicted with container deployment.

**Solution:** Cleared credential helpers and used gcloud authentication:
```bash
echo '{}' > ~/.docker/config.json
gcloud auth configure-docker us-central1-docker.pkg.dev
```

---

## Monitoring
```bash
# Get cluster access
gcloud container clusters get-credentials stockbusters-app-cluster --region us-central1

# Check status
kubectl get pods -n stockbusters-app-namespace

# View logs
kubectl logs -f deployment/api -n stockbusters-app-namespace

# Check ingress
kubectl get ingress -n stockbusters-app-namespace
```

---

## Cost Estimation

**Monthly costs (default config):**
- GKE Cluster: ~$73
- Node Pool (1-3 nodes): ~$25-75
- Load Balancer: ~$18
- Artifact Registry: ~$0.10/GB

**Total:** ~$116-166/month

**Optimization tips:**
- Use preemptible nodes for dev/test
- Enable GKE Autopilot for production
- Configure HPA for automatic scaling

---

## Why Pulumi Over Ansible?

| Feature | Pulumi | Ansible |
|---------|--------|---------|
| Approach | Declarative IaC | Imperative automation |
| State Management | Built-in | Manual |
| Type Safety | ✅ Python types | ❌ |
| Rollbacks | Automatic | Manual |
| Best For | Infrastructure | Configuration |

**We chose Pulumi for:**
- Type-safe infrastructure definitions
- Automatic state tracking
- Native cloud provider APIs
- Easy rollbacks and versioning

---

## Key Takeaways

1. **Pulumi + K8s = Production-Ready** - Declarative IaC with powerful orchestration
2. **Workload Identity is Essential** - Secure GCP access without embedded keys
3. **Proper IAM from Day 1** - Permissions issues caused most delays
4. **Proven Scalability** - 3x scaling with 0% failure rate
5. **Zero-Downtime Deployments** - Rolling updates keep app available

---

## Future Enhancements

- SSL/TLS with Let's Encrypt
- Horizontal Pod Autoscaler (HPA)
- Multi-region deployment
- CI/CD with GitHub Actions
- Cloud SQL (PostgreSQL)
- Prometheus + Grafana monitoring

---

## Conclusion

Deploying Stock Busters on GKE with Pulumi provided a scalable, maintainable infrastructure. The declarative approach, combined with Kubernetes orchestration, gives us confidence in production deployments. 

**Key achievements:**
- ✅ Automated infrastructure provisioning
- ✅ Zero-downtime deployments
- ✅ Proven horizontal scalability
- ✅ 100% request success rate under load
- ✅ Efficient resource utilization

From 1 to 100+ users, our infrastructure automatically adapts.

**Deployed Application:** http://34.60.47.248.sslip.io

---

## Resources

- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)

---

**About the Project:**

Stock Busters was developed at Harvard AC215, demonstrating enterprise-grade deployment practices for AI-powered financial applications.

---


