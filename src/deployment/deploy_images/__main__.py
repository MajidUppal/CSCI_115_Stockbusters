import os
import pulumi
import pulumi_docker_build as docker_build
from pulumi_gcp import artifactregistry
from pulumi import CustomTimeouts
import datetime

# 🔧 Get project info
gcp_config = pulumi.Config("gcp")
project = gcp_config.require("project")
location = os.environ.get("GCP_REGION", "us-central1")

# Get absolute paths
# Script is at: src/deployment/deploy_images/__main__.py (repo root)
#              or /app/deploy_images/__main__.py (Docker)
# Handle two scenarios:
# 1. Docker: /app/deploy_images/__main__.py -> /app (go up 1 level)
# 2. GitHub Actions/repo root: src/deployment/deploy_images/__main__.py -> src/ (go up 2 levels)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # deploy_images directory
DEPLOYMENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # parent directory

# Check if we're in Docker (path starts with /app) or repo root (path contains src/deployment)
# In Docker, /app is the mount point where api-service and frontend are also mounted
# In repo root, we need to go up to src/ to find api-service and frontend
if DEPLOYMENT_DIR.startswith("/app") or os.path.basename(DEPLOYMENT_DIR) != "deployment":
    # Docker: /app/deploy_images -> go up 1 level to /app
    # Also handles case where parent is not "deployment" (fallback)
    SRC_DIR = DEPLOYMENT_DIR
else:
    # GitHub Actions/repo root: src/deployment/deploy_images -> go up 2 levels to src/
    SRC_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

print(f"Script directory: {SCRIPT_DIR}")
print(f"Src directory: {SRC_DIR}")

# 🕒 Timestamp for tagging
timestamp_tag = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
repository_name = "stockbusters-app-repository"

# 📦 Create Artifact Registry repository
artifact_repo = artifactregistry.Repository(
    "stockbusters-app-repository",
    repository_id=repository_name,
    location=location,
    format="DOCKER",
    description="Docker images for Stockbusters App",
)

# Registry URL
registry_url = artifact_repo.name.apply(
    lambda name: f"{location}-docker.pkg.dev/{project}/{repository_name}"
)

# Common build options
build_opts = pulumi.ResourceOptions(
    custom_timeouts=CustomTimeouts(create="30m"),
    retain_on_delete=True,
    depends_on=[artifact_repo]
)

# ========================================
# 🔨 API Service
# ========================================
api_service_context = os.path.join(SRC_DIR, "api-service")
api_service_dockerfile = os.path.join(api_service_context, "Dockerfile")

print(f"API Service context: {api_service_context}")
print(f"API Service dockerfile: {api_service_dockerfile}")
print(f"Dockerfile exists: {os.path.exists(api_service_dockerfile)}")

api_service_image = docker_build.Image(
    "build-stockbusters-app-api-service",
    tags=[pulumi.Output.concat(registry_url, "/stockbusters-app-api-service:", timestamp_tag)],
    context=docker_build.BuildContextArgs(location=api_service_context),
    dockerfile=docker_build.DockerfileArgs(location=api_service_dockerfile),
    platforms=[docker_build.Platform.LINUX_AMD64],
    push=True,
    opts=build_opts
)

pulumi.export("stockbusters-app-api-service-ref", api_service_image.ref)
pulumi.export("stockbusters-app-api-service-tags", api_service_image.tags)

# ========================================
# 🔨 Frontend
# ========================================
frontend_context = os.path.join(SRC_DIR, "frontend")
frontend_dockerfile = os.path.join(frontend_context, "Dockerfile")

print(f"Frontend context: {frontend_context}")
print(f"Frontend dockerfile: {frontend_dockerfile}")
print(f"Dockerfile exists: {os.path.exists(frontend_dockerfile)}")

# Verify path before building
if not os.path.exists(frontend_dockerfile):
    print(f"ERROR: Dockerfile not found!")
    print(f"Looking for: {frontend_dockerfile}")
    print(f"Contents of {frontend_context}:")
    if os.path.exists(frontend_context):
        print(os.listdir(frontend_context))
    raise FileNotFoundError(f"Dockerfile not found at: {frontend_dockerfile}")

frontend_image = docker_build.Image(
    "build-stockbusters-app-frontend",
    tags=[pulumi.Output.concat(registry_url, "/stockbusters-app-frontend:", timestamp_tag)],
    context=docker_build.BuildContextArgs(location=frontend_context),
    dockerfile=docker_build.DockerfileArgs(location=frontend_dockerfile),
    platforms=[docker_build.Platform.LINUX_AMD64],
    push=True,
    opts=build_opts
)

pulumi.export("stockbusters-app-frontend-ref", frontend_image.ref)
pulumi.export("stockbusters-app-frontend-tags", frontend_image.tags)

# ========================================
# 📊 Summary
# ========================================
pulumi.export("registry_url", registry_url)
pulumi.export("timestamp", timestamp_tag)