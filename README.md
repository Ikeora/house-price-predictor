## Automated End-to-End MLOps Pipeline: GitOps Simulation

This project demonstrates a production-designed, fully automated MLOps (Machine Learning Operations) ecosystem simulated locally. It handles the entire lifecycle of a machine learning model—from raw data engineering and MLflow experiment tracking to containerized microservices and automated GitOps continuous delivery inside a Kubernetes cluster via ArgoCD.
To eliminate cloud hosting costs during development, the entire production infrastructure is replicated locally using KinD (Kubernetes in Docker).

------------------------------
## System Architecture & Workflow
The architecture decouples the machine learning workspace, container registries, pipeline runners, and cluster orchestrators to ensure high security, independent scaling, and high availability.

```
[ On Push/ Workflow dispatch ] 
        │
        ▼
┌────────────────────────────────────────────────────────┐
│ GitHub Actions CI/CD Pipeline                          │
│  1. Run Feature Engineering & ML Model Training        │
│  2. Spin up ephemeral MLflow container for tracking    │
│  3. Build & Integration Test App Docker Images         │
│  4. Push verified Docker images to Docker Hub          │
│  5. Dynamically patch K8s Manifests with COMMIT_HASH   │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼ (Git Push GitOps Manifests)
┌────────────────────────────────────────────────────────┐
│ GitHub Repository (Single Source of Truth)             │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼ (Pull Tracking)
┌────────────────────────────────────────────────────────┐
│ ArgoCD Orchestrator (Running inside KinD)              │
│  - Detects out-of-sync manifest version in Git         │
│  - Triggers automated rollout to local cluster         │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼ (Local Host Mapping via NodePort)
┌────────────────────────────────────────────────────────┐
│ KinD Kubernetes Cluster (Local Production Simulation)  │
│  ├── Path: localhost:30000 ──► [ Streamlit Pods ]      │
│  └── Path: localhost:30100 ──► [ FastAPI Pods ]        │
└────────────────────────────────────────────────────────┘
```
------------------------------
## Key MLOps Engineering Highlights

* Automated GitOps Paradigm: Implemented Git as the strict Single Source of Truth. Local cluster configurations automatically mirror GitHub repository changes without manual kubectl intervention.
* Decoupled Microservices: Separated the model compute layer (FastAPI backend) from the UI presentation layer (Streamlit frontend) to minimize deployment dependencies and optimize scaling.
* Rigorous Integration Testing: The CI pipeline builds and launches test instances of the Docker containers on the fly, running curl-based health checks to guarantee container viability before registry pushing.
* Deterministic Version Tracking: Eliminated mutable tags like latest. Every deployment uses an explicit Git COMMIT_HASH for reliable audit trails and instant, single-click cluster rollbacks.
* Cost-Efficient Local Replication: Utilizes KinD (Kubernetes in Docker) to replicate enterprise cloud paradigms (declarative states, self-healing pods, control planes) directly on a local workstation for zero-cost development.

------------------------------
------------------------------
## Project Structure
```
house-price-predictor/
├── .github/workflows/      # GitHub Actions end-to-end CI/CD pipeline
├── configs/                # Model hyperparameter and evaluation settings
├── data/                   # Raw and temporary staging datasets
├── .github/workflows/      # GitHub Actions end-to-end CI/CD pipeline
├── configs/                # Model hyperparameter and evaluation settings
├── data/                   # Raw and temporary staging datasets
├── deployment/
│   └── kubernetes/         # Production-ready K8s Manifests (Deployments, Services)
├── models/                 # Staged binaries (trained models and preprocessors)
│   └── kubernetes/         # Production-ready K8s Manifests (Deployments, Services)
├── models/                 # Staged binaries (trained models and preprocessors)
├── src/
│   ├── data/               # Data cleaning and robust processing validation
│   ├── features/           # Feature engineering and serialization logic
│   └── models/             # XGBoost model training, assessment, & MLflow logging
└── streamlit_app/          # Streamlit dashboard source and isolated Docker environment
```
------------------------------
## Automated CI/CD Pipeline (GitHub Actions)
The declarative .github/workflows/ pipeline triggers on code changes and performs the following tasks:

   1. Environment Initialization: Boots an active runner and provisions an isolated Python environment.
   2. Data & Feature Engineering: Executes data transformation and saves feature preprocessing binaries (preprocessor.pkl).
   3. Model Training & Experiment Tracking: Orchestrates an ephemeral MLflow engine via Docker to store runs, metrics, and parameters, producing the final deployment-ready model binary.
   4. Container Integration Tests:
   * Compiles the FastAPI app and verifies the /health endpoint responds successfully.
      * Compiles the Streamlit app and validates UI initialization stability.
   5. Image Distribution: Labels and pushes stable containers to Docker Hub under explicit commit signatures.
   6. GitOps Synchronization: Dynamically executes string updates (sed) on the staging Kubernetes files, commits the changed images using an automated runner token, and drops a [skip ci] flag to safely break automation infinite loops.

------------------------------
## Local Infrastructure & Service Architecture
The microservices are hosted locally inside a KinD (Kubernetes in Docker) cluster, with deployments and configurations synchronized dynamically using ArgoCD.
## Networking & Port Layout
The cluster exposes application interfaces directly to the local host machine using NodePort configurations:

* model Service (type: NodePort): Maps the internal FastAPI endpoint (port 8000) to the local host machine at http://localhost:30100.
* streamlit Service (type: NodePort): Maps the frontend UI layout (port 8501) to the local host machine at http://localhost:30000.

------------------------------
## Local Testing & Verification
To verify the prediction contract directly via your local terminal, query the exposed model endpoint:
```
curl -X POST "http://localhost:30100/predict" \
│   ├── data/               # Data cleaning and robust processing validation
│   ├── features/           # Feature engineering and serialization logic
│   └── models/             # XGBoost model training, assessment, & MLflow logging
└── streamlit_app/          # Streamlit dashboard source and isolated Docker environment
```
------------------------------
## Automated CI/CD Pipeline (GitHub Actions)
The declarative .github/workflows/ pipeline triggers on code changes and performs the following tasks:

   1. Environment Initialization: Boots an active runner and provisions an isolated Python environment.
   2. Data & Feature Engineering: Executes data transformation and saves feature preprocessing binaries (preprocessor.pkl).
   3. Model Training & Experiment Tracking: Orchestrates an ephemeral MLflow engine via Docker to store runs, metrics, and parameters, producing the final deployment-ready model binary.
   4. Container Integration Tests:
   * Compiles the FastAPI app and verifies the /health endpoint responds successfully.
      * Compiles the Streamlit app and validates UI initialization stability.
   5. Image Distribution: Labels and pushes stable containers to Docker Hub under explicit commit signatures.
   6. GitOps Synchronization: Dynamically executes string updates (sed) on the staging Kubernetes files, commits the changed images using an automated runner token, and drops a [skip ci] flag to safely break automation infinite loops.

------------------------------
## Local Infrastructure & Service Architecture
The microservices are hosted locally inside a KinD (Kubernetes in Docker) cluster, with deployments and configurations synchronized dynamically using ArgoCD.
## Networking & Port Layout
The cluster exposes application interfaces directly to the local host machine using NodePort configurations:

* model Service (type: NodePort): Maps the internal FastAPI endpoint (port 8000) to the local host machine at http://localhost:30100.
* streamlit Service (type: NodePort): Maps the frontend UI layout (port 8501) to the local host machine at http://localhost:30000.

------------------------------
## Local Testing & Verification
To verify the prediction contract directly via your local terminal, query the exposed model endpoint:
```
curl -X POST "http://localhost:30100/predict" \
-H "Content-Type: application/json" \
-d '{
  "sqft": 1500,
  "bedrooms": 3,
  "bathrooms": 2,
  "location": "suburban",
  "year_built": 2000
  "condition": "Good"
}'
```
------------------------------
## Future Cloud Roadmap
Because this architecture strictly adheres to cloud-native Kubernetes standards, migrating this exact pipeline to a cloud provider like Azure AKS (Azure Kubernetes Service) requires zero pipeline changes. The operational steps for production scale include:

   1. Converting Service types from NodePort to secure internal ClusterIP instances.
   2. Provisioning an NGINX Ingress Controller to act as a unified, public-facing gateway for routing traffic via a single external IP address.
   3. Redirecting the existing ArgoCD instances to the new cloud cluster context.



