# Corporate Office Network Operations Dashboard — CI/CD Pipeline

## 1. Project Overview

This project demonstrates the implementation of a Continuous Integration and Continuous Deployment (CI/CD) pipeline for an existing Python Flask application. The application is packaged using Docker and deployed to a Kubernetes cluster using Jenkins automation.

The project uses a Corporate Office Network Operations Dashboard as the application and demonstrates how code changes can be built, tested, containerized, and deployed through a repeatable pipeline.

## 2. Project Information

- **Project:** Corporate Office Network Operations Dashboard
- **Student:** Sahil Verma
- **Repository:** [GitHub Repository](https://github.com/unaxpro/corporate-office-cicd)
- **Docker Hub:** [Docker Image Repository](https://hub.docker.com/r/unaxpro/corporate-office-cicd)

## 3. Objectives

- Integrate GitHub with Jenkins for source-code management.
- Automate application build and testing.
- Build and tag a Docker image.
- Push the image to Docker Hub.
- Deploy the application to Kubernetes using Deployment and Service manifests.
- Verify the deployment and demonstrate an application update through a second pipeline run.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python and Flask | Application development |
| Git and GitHub | Source-code management |
| Jenkins | CI/CD pipeline automation |
| AWS EC2 | Hosting the Jenkins server |
| Docker | Building and packaging the application |
| Docker Hub | Storing Docker images |
| Kubernetes | Application deployment and management |
| Minikube | Running the Kubernetes cluster |
| YAML | Kubernetes Deployment and Service configuration |

## 5. Repository Structure

```text
corporate-office-cicd/
├── Jenkinsfile
└── python_gui/
    ├── app.py
    ├── corporate_network.py
    ├── requirements.txt
    ├── Dockerfile
    ├── tests/
    └── k8s/
        ├── deployment.yaml
        └── service.yaml
```

**Main files:**

- `Jenkinsfile` — Defines the automated pipeline.
- `python_gui/app.py` — Flask application entry point.
- `python_gui/corporate_network.py` — Supporting application module.
- `python_gui/requirements.txt` — Python dependencies.
- `python_gui/Dockerfile` — Instructions for building the Docker image.
- `python_gui/k8s/deployment.yaml` — Defines the Kubernetes Deployment and application replicas.
- `python_gui/k8s/service.yaml` — Exposes the application through a Kubernetes NodePort Service.
- `python_gui/tests/` — Contains application tests.

## 6. CI/CD Pipeline Workflow

The pipeline follows this workflow:

```text
GitHub Repository
        |
        v
Jenkins Pipeline
        |
        v
Checkout Source Code
        |
        v
Install Dependencies and Run Tests
        |
        v
Build Docker Image
        |
        v
Push Image to Docker Hub
        |
        v
Deploy to Kubernetes (Minikube)
        |
        v
Verify Deployment and Application
```

### Pipeline stages

1. **Checkout:** Retrieves the source code from the GitHub repository.
2. **Build and Test:** Installs the required Python dependencies, executes the tests, and checks Python source files for compilation errors.
3. **Docker Build:** Builds the application image and tags it using the Jenkins build number, along with a `latest` tag.
4. **Push Image:** Authenticates with Docker Hub using Jenkins credentials and pushes the image to the image repository.
5. **Deploy to Minikube:** Applies the Kubernetes manifests and updates the Deployment to use the image produced by the current build.
6. **Verify Deployment:** Checks the Kubernetes Deployment, Pods, and Services to confirm the deployment status.

The pipeline is defined as code in the root-level `Jenkinsfile`.

## 7. Jenkins Setup on AWS EC2

Jenkins was configured on an Ubuntu-based AWS EC2 instance in the Asia Pacific (Mumbai) region.

The setup included:

1. Launching an Ubuntu EC2 instance and configuring the required security-group access.
2. Installing and configuring Jenkins with a compatible Java runtime.
3. Installing Docker and configuring Jenkins access to Docker.
4. Configuring the Jenkins pipeline to retrieve the project from GitHub.
5. Adding Docker Hub authentication through a Jenkins credential with the ID `dockerhub-creds`.
6. Configuring access to the Minikube Kubernetes cluster for deployment.
7. Running the pipeline and checking the console output and build result.

The Jenkins job was configured to use **Pipeline script from SCM**, with the GitHub repository URL, the `main` branch, and `Jenkinsfile` as the script path.

## 8. Docker Image Build and Publishing

The Dockerfile uses the Python 3.11 slim image, installs the application's dependencies, copies the project files, exposes port `5000`, and starts the Flask application.

The Docker image repository is:

**[unaxpro/corporate-office-cicd](https://hub.docker.com/r/unaxpro/corporate-office-cicd)**

The pipeline creates build-specific image tags and a `latest` tag, then pushes the image to Docker Hub using Jenkins-managed credentials.

Credentials and access tokens should never be committed to the source repository.

## 9. Kubernetes Deployment

The application is deployed to a Minikube Kubernetes cluster.

### Deployment configuration

- **Deployment name:** `corporate-network`
- **Replicas:** 2
- **Container port:** `5000`
- **Image:** `unaxpro/corporate-office-cicd:latest`, with the pipeline also deploying the build-specific image tag.

### Service configuration

- **Service name:** `corporate-network-service`
- **Service type:** NodePort
- **Service port:** `5000`
- **Target port:** `5000`
- **NodePort:** `30080`

The two replicas provide multiple application Pods managed by Kubernetes. The Service provides a stable endpoint within the cluster and a NodePort for external access when the cluster and networking are available.

The Kubernetes manifests are stored in `python_gui/k8s/`.

## 10. Verification and Testing

The following checks were performed during execution:

- Jenkins pipeline completed with a `SUCCESS` result.
- Kubernetes Deployment reached a ready state with two application replicas.
- Both application Pods were reported as `Running`.
- The application responded successfully to an HTTP request with **HTTP 200 OK**.
- The application was updated and checked again after the second pipeline run.

These checks demonstrate the successful build, deployment, and verification of the application during the practical.

## 11. Second Pipeline Run — Application Update

To demonstrate an application change, the main heading in `python_gui/app.py` was updated from:

```html
<h1>Your office network, at a glance.</h1>
```

to:

```html
<h1>Corporate Network — CI/CD Deployment Verified!</h1>
```

The Jenkins pipeline was run again. The build completed successfully, and the updated heading was visible when the application was checked in the browser after deployment.

This demonstrates how a code change can be incorporated into a subsequent pipeline run and reflected in the deployed application.

## 12. Result

The CI/CD practical demonstrated an automated workflow using GitHub, Jenkins, Docker, Docker Hub, AWS EC2, and Kubernetes with Minikube.

The pipeline checked out the project, installed dependencies, ran tests, built and published the Docker image, deployed the application to Kubernetes, and verified the deployment. A subsequent pipeline run also demonstrated an application update.

**Current status:** The AWS EC2 instance used for Jenkins has been terminated after completing the practical. Therefore, the Jenkins server and deployed application should not be assumed to be currently accessible online. The repository and Docker Hub links remain available subject to their access settings.

## 13. Submission Checklist

- [x] GitHub repository URL
- [x] Jenkinsfile
- [x] Dockerfile
- [x] Kubernetes Deployment manifest
- [x] Kubernetes Service manifest
- [x] Application source code and tests
- [x] Docker Hub repository link
- [x] Successful pipeline and deployment verification
- [x] Second application update demonstrated

