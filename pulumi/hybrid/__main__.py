"""
Pulumi Stack: Hybrid (Kubernetes)
"""
import pulumi
import pulumi_kubernetes as k8s

# Layer 1: Foundation (Namespaces)
ns = k8s.core.v1.Namespace(
    "layer-cake-ns",
    metadata={"name": "platform-layers"}
)

# Layer 2: Data Services (Mock Database)
# Depends explicitly on Namespace
db_labels = {"app": "mock-db"}
db_deployment = k8s.apps.v1.Deployment(
    "layer2-db",
    metadata={
        "namespace": ns.metadata["name"],
        "name": "mock-database"
    },
    spec={
        "selector": {"matchLabels": db_labels},
        "replicas": 1,
        "template": {
            "metadata": {"labels": db_labels},
            "spec": {
                "containers": [{
                    "name": "db",
                    "image": "postgres:13-alpine",
                    "env": [{"name": "POSTGRES_PASSWORD", "value": "example"}],
                    "ports": [{"containerPort": 5432}]
                }]
            }
        }
    },
    opts=pulumi.ResourceOptions(depends_on=[ns])
)

db_service = k8s.core.v1.Service(
    "layer2-db-svc",
    metadata={
        "namespace": ns.metadata["name"],
        "name": "database"
    },
    spec={
        "ports": [{"port": 5432, "targetPort": 5432}],
        "selector": db_labels
    },
    opts=pulumi.ResourceOptions(depends_on=[db_deployment])
)

# Layer 3: Application (Stateless)
# Depends on DB Service availability (simulated by explicit depends_on)
app_labels = {"app": "layer-app"}
app_deployment = k8s.apps.v1.Deployment(
    "layer3-app",
    metadata={
        "namespace": ns.metadata["name"],
        "name": "layer-app"
    },
    spec={
        "selector": {"matchLabels": app_labels},
        "replicas": 2,
        "template": {
            "metadata": {"labels": app_labels},
            "spec": {
                "containers": [{
                    "name": "app",
                    "image": "nginx:alpine", # Placeholder for app
                    "env": [
                        {"name": "DB_HOST", "value": db_service.metadata["name"]}
                    ]
                }]
            }
        }
    },
    opts=pulumi.ResourceOptions(depends_on=[db_service])
)

pulumi.export("namespace", ns.metadata["name"])
pulumi.export("db_url", db_service.metadata["name"])
