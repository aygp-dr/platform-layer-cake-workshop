"""
Exercise 1: Create a dependency map for your services
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dependency_analyzer import Service, DependencyType, detect_circular_dependencies, validate_layering

# Task 1: Add at least 5 services with dependencies
# We define a mix of services, including a deliberate circular dependency to demonstrate the issue.
services = {
    "load-balancer": Service(
        name="load-balancer",
        layer=3,
        dependencies={"auth-service": DependencyType.HARD} # Circular risk if auth needs LB
    ),
    "auth-service": Service(
        name="auth-service",
        layer=2,
        dependencies={"database": DependencyType.HARD}
    ),
    "database": Service(
        name="database",
        layer=1, # AWS RDS
        dependencies={}
    ),
    "app-server": Service(
        name="app-server",
        layer=4,
        dependencies={
            "auth-service": DependencyType.HARD,
            "database": DependencyType.HARD,
            "logging": DependencyType.SOFT
        }
    ),
    "logging": Service(
        name="logging",
        layer=5, 
        dependencies={"database": DependencyType.HARD}
    ),
    # Introduce the classic deploy cycle.
    "deployment-service": Service(
        name="deployment-service",
        layer=5,
        dependencies={"artifact-store": DependencyType.HARD}
    ),
    "artifact-store": Service(
        name="artifact-store",
        layer=4,
        dependencies={"deployment-service": DependencyType.HARD} # Cycle: needs deployment to be updated/managed
    )
}

def run_exercise():
    print("--- Task 2: Run circular dependency detection ---")
    cycles = detect_circular_dependencies(services)
    if cycles:
        print(f"Found circular dependencies: {cycles}")
    else:
        print("No circular dependencies found.")

    print("\n--- Task 3: Fix any cycles found ---")
    # Fix: artifact-store should not hard-depend on deployment-service for its basic operation/recovery
    print("Applying fix: Removing hard dependency from artifact-store to deployment-service (changing to SOFT)")
    services["artifact-store"].dependencies["deployment-service"] = DependencyType.SOFT
    
    cycles_fixed = detect_circular_dependencies(services)
    if cycles_fixed:
        print(f"Still found cycles: {cycles_fixed}")
    else:
        print("Cycles eliminated!")

    print("\n--- Verifying Layers ---")
    violations = validate_layering(services)
    if violations:
        print("Found layer violations:")
        for v in violations:
            print(f"  {v}")
    else:
        print("No layer violations found.")

if __name__ == "__main__":
    run_exercise()
