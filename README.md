# k8s-express: Production-Grade Kubernetes Platform
<div align="center">

[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.30+-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.110+-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![ArgoCD](https://img.shields.io/badge/ArgoCD-GitOps-EF7b4D?style=for-the-badge&logo=argocd&logoColor=white)](https://argo-cd.readthedocs.io/)
[![Docker](https://img.shields.io/badge/Docker-NonRoot-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/Amazon_AWS-ECR%20%7C%20EKS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*An enterprise-ready, cloud-native microservices platform engineered with declarative GitOps pipelines, zero-downtime rolling deployments, strict container security hardening, and resilient autoscaling architectures.*

</div>

---

## 🎯 Executive Summary & Platform Objectives

**CloudForge Enterprise** is a reference architecture designed to bridge the gap between application development and production-grade Kubernetes infrastructure. It eliminates configuration drift through automated **ArgoCD GitOps synchronization**, enforces strict **CIS benchmarks** for container security, and provides dynamic scaling via **Horizontal Pod Autoscalers (HPA v2)**.

---

## 🏗️ End-to-End System Architecture

```text
  [ Developer Push ]
         │
         ▼
  [ GitHub Repository ] ──(Trigger)──> [ GitHub Actions CI/CD ]
                                              │
                                       (Build & Push)
                                              │
                                              ▼
                                      [ Amazon AWS ECR ]
                                      (Image Tag: SHA)
                                              │
                                       (Auto-Commit Tag)
                                              │
         ┌────────────────────────────────────┘
         ▼
  [ GitHub Repo Manifests ] 
         │
   (Poll / Sync)
         │
         ▼
  [ ArgoCD Controller ] ──────────────────────┐
         │                                    │
    (Reconcile)                        (Self-Heal / Prune)
         │                                    │
         ▼                                    ▼
  [ Kubernetes Cluster (EKS) ] <──────────────┘
  ├── Namespace: production
  ├── Deployments (Replicas: 3, RollingUpdate)
  ├── Services & Ingress (TLS Termination)
  └── HPA (CPU / Memory Triggers)
  🏛️ Core Technical Blueprint
1. Workload Orchestration & Kustomize Architecture
Decoupled Base & Overlays: The k8s/base directory defines immutable, enterprise-standard API primitives (Namespaces, Secrets, ConfigMaps, Deployments, Services, Ingress, HPA, and ArgoCD Application definitions).

Environment Specialization: k8s/overlays/dev and k8s/overlays/production apply targeted Strategic Merge Patches and ConfigMap generators to scale resources (e.g., 1 replica for dev vs. 3+ high-availability replicas for production).

2. Security Hardening & Compliance
Unprivileged Containers: Enforces runAsNonRoot: true with explicitly mapped non-root UIDs/GIDs (10001:10001) inside the pod security context.

Secret Management: Abstracted sensitive variables injected securely through Kubernetes Secrets and runtime environment mapping.

Resource Governance: Mandatory CPU and Memory request/limit boundaries (requests: 150m/128Mi, limits: 500m/512Mi) to prevent cluster resource starvation.

3. High Availability & Resilience
Zero-Downtime Rollouts: Configured with maxSurge: 1 and maxUnavailable: 0 strategy to guarantee service continuity during rolling deployments.

Proactive Health Monitoring: Granular lifecycle probes implemented:

Startup Probe: Protects slow-starting application containers (failureThreshold: 30, periodSeconds: 5).

Liveness Probe: Automatically restarts unhealthy instances.

Readiness Probe: Isolates traffic from pods undergoing heavy processing loads.

📂 Repository Layout
Plaintext
.
├── app/                        # Python FastAPI Microservice Source
│   ├── Dockerfile              # Multi-stage hardened build
│   ├── main.py                 # Core application endpoints & health checks
│   └── requirements.txt        # Pinned runtime dependencies
├── k8s/                        # Declarative Infrastructure Manifests
│   ├── base/                   # Immutable Base Resources
│   │   ├── 00-namespace.yaml
│   │   ├── 01-secret.yaml
│   │   ├── 02-configmap.yaml
│   │   ├── 03-deployment.yaml
│   │   ├── 04-service.yaml
│   │   ├── 05-ingress.yaml
│   │   ├── 06-hpa.yaml
│   │   ├── 07-argocd-app.yaml
│   │   └── kustomization.yaml
│   └── overlays/               # Environment Overlays
│       ├── dev/                # Development Overlay Configuration
│       │   ├── kustomization.yaml
│       │   └── patch-replicas.yaml
│       └── production/         # Production Enterprise Overlay
│           ├── kustomization.yaml
│           └── patch-replicas.yaml
└── .github/
    └── workflows/
        └── ci.yaml             # Automated CI Pipeline & GitOps Bridge
🚀 Getting Started & Local Validation
Prerequisites
kubectl CLI installed.

kustomize (or kubectl kustomize) operational.

Docker runtime for local container builds.
1. Compile & Inspect Manifests (Dry-Run)
Validate Kustomize accumulation and manifest rendering prior to cluster injection:

Bash
# Render Development Manifests
kubectl kustomize k8s/overlays/dev

# Render Production Manifests
kubectl kustomize k8s/overlays/production
2. Direct Cluster Deployment
Apply environments imperatively via Kustomize:

Bash
# Deploy Development Stack
kubectl apply -k k8s/overlays/dev

# Deploy Production Stack
kubectl apply -k k8s/overlays/production
🔄 Automated CI/CD & GitOps Workflow
Continuous Integration: Code pushes targeting the main branch trigger GitHub Actions workflow execution.

Container Lifecycle: The workflow authenticates with Amazon ECR, builds an optimized multi-stage Docker image tagged with the unique Git Commit SHA, and pushes it to the registry.

GitOps Reconciliation: The pipeline automatically updates the base deployment manifest image reference and pushes back to the repository. ArgoCD detects the state mutation and seamlessly synchronizes the live Kubernetes cluster.

👨‍💻 Author & Professional Profile
Ahmed Wael Abdelaziz Ahmed

Cloud & DevOps Engineer
