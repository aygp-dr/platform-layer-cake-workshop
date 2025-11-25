# Open Source Chaos & Resilience Testing Tools

A curated list of open-source tools for evaluating resilience across production, infrastructure as code (IaC), and platform tooling.

## 1. Production & Kubernetes (User-Facing)

Tools best suited for testing microservices, web applications, and APIs running in live environments.

### [Chaos Mesh](https://chaos-mesh.org/) (CNCF Project)
*   **Best For:** Kubernetes-native environments requiring deep fault injection.
*   **Capabilities:** 
    *   Pod killing, network partitioning, packet loss/corruption.
    *   High CPU/memory stress, IO fault injection.
    *   JVM-level fault injection.
    *   Rich dashboard for visualization and scheduling.
*   **Use Case:** Simulating specific user-facing failures (e.g., adding 500ms latency to a payment service).

### [LitmusChaos](https://litmuschaos.io/) (CNCF Project)
*   **Best For:** End-to-end resilience testing and CI/CD pipeline integration.
*   **Capabilities:** 
    *   "Chaos Hub" with pre-defined experiments.
    *   Declarative "Probes" to measure the "Steady State" of applications before/after chaos.
    *   Manages chaos experiments as Kubernetes CRDs.
*   **Use Case:** Automated chaos gates in release pipelines.

### [ChaosBlade](https://github.com/chaosblade-io/chaosblade) (Alibaba)
*   **Best For:** High-volume traffic simulation and Java/C++ applications.
*   **Capabilities:** 
    *   JVM-level fault injection (e.g., throwing exceptions inside specific methods).
    *   Docker and host-level resource attacks.
*   **Use Case:** Testing legacy Java applications or high-load scenarios.

## 2. Infrastructure as Code (IaC) & Cloud Resources

Tools for validating that IaC (Terraform, Pulumi) can reconcile drift and that cloud resources self-heal.

### [Chaos Toolkit](https://chaostoolkit.org/)
*   **Best For:** Orchestrating "Game Days" and verifying non-Kubernetes resources.
*   **Capabilities:** 
    *   Python-based driver framework with plugins for AWS, Azure, GCP, and Terraform.
    *   JSON/YAML experiment definition.
*   **Use Case:** 
    1.  Run `terraform apply` (steady state).
    2.  **Action:** Delete an Auto Scaling Group or modify a Security Group via AWS driver.
    3.  **Probe:** Assert service reachability.
    4.  **Recovery:** Run `terraform apply` to verify self-healing.

### [LocalStack](https://localstack.cloud/) (with Fault Injection)
*   **Best For:** Testing IaC resilience locally before deploying to real cloud.
*   **Capabilities:** Simulating AWS services locally with ability to inject errors (e.g., S3 500 errors).

## 3. Platform Tooling, Messaging & Middleware

Tools for the "backplane" of the platform: CI/CD agents, Artifact Repositories, and Message Queues.

### Messaging (Kafka, RabbitMQ)

#### [Toxiproxy](https://github.com/shopify/toxiproxy) (Shopify)
*   **Best For:** Simulating "bad network" conditions between services and queues.
*   **Capabilities:** TCP proxy that introduces latency, bandwidth limits, and connection resets.
*   **Use Case:** 
    *   Simulate connection timeouts to Kafka brokers to test client retry logic.
    *   Introduce high latency to test RabbitMQ consumer lag handling.

### CI/CD & Artifacts (Jenkins, Artifactory, Git)

#### [Pumba](https://github.com/alexei-led/pumba)
*   **Best For:** Testing containerized build agents and CI runners.
*   **Capabilities:** Randomly kill, stop, or pause Docker containers.
*   **Use Case:** Killing Jenkins/GitLab runner containers to ensure the pipeline automatically retries jobs.

#### Network Policy (Calico/Cilium) + Chaos Mesh
*   **Use Case:** Create a network partition blocking traffic from Build Agents to the Artifact Repository (e.g., `npm install` hangs) to verify CI pipeline timeouts and error handling.

## Summary Recommendation

| Area | Primary Tool | Secondary Tool |
| :--- | :--- | :--- |
| **K8s / Production** | **Chaos Mesh** | LitmusChaos |
| **Legacy / VM / Host** | **ChaosBlade** | Pumba |
| **IaC / AWS / Cloud** | **Chaos Toolkit** | AWS FIS (Non-OSS alternative) |
| **Network / Messaging**| **Toxiproxy** | Chaos Mesh (Network Chaos) |
