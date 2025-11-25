"""
Exercise 2: Assign services to appropriate layers
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dependency_analyzer import Service, DependencyType, validate_layering

services_data = {
    "database": {"current_layer": None, "dependencies": ["aws-rds"]},
    "auth": {"current_layer": None, "dependencies": ["database"]},
    "api": {"current_layer": None, "dependencies": ["auth", "database"]},
    "frontend": {"current_layer": None, "dependencies": ["api"]},
    "aws-rds": {"current_layer": 1, "dependencies": []},
}

def assign_layers(services_data):
    """
    Assign each service to a layer based on dependencies
    
    Rules:
    1. Services with no dependencies → Layer 2 (Layer 1 is cloud)
    2. Services depend only on lower layers
    3. Minimize layer count while respecting dependencies
    """
    print("Starting layer assignment...")
    
    # Reset layers (except fixed Layer 1)
    for s in services_data.values():
        if s.get("current_layer") != 1: 
            s["current_layer"] = None
            
    changed = True
    iteration = 0
    while changed:
        changed = False
        iteration += 1
        # Safe guard against infinite loops
        if iteration > 100:
            break
            
        for name, svc in services_data.items():
            if svc["current_layer"] is not None:
                continue
                
            # Check if all dependencies have layers
            deps_resolved = True
            max_dep_layer = 0
            
            for dep in svc["dependencies"]:
                if dep not in services_data:
                    # Skip unknown dependencies or assume they are external
                    continue
                    
                if services_data[dep]["current_layer"] is None:
                    deps_resolved = False
                    break
                max_dep_layer = max(max_dep_layer, services_data[dep]["current_layer"])
            
            if deps_resolved:
                # Assign layer: strictly greater than max dependency
                # If max_dep_layer is 0 (no deps), assign 2 (since 1 is cloud)
                if max_dep_layer == 0:
                     new_layer = 2
                else:
                     new_layer = max_dep_layer + 1
                
                svc["current_layer"] = new_layer
                changed = True
                print(f"Assigned {name} to Layer {new_layer}")

    # Check for unassigned (cycles)
    unassigned = [n for n, s in services_data.items() if s["current_layer"] is None]
    if unassigned:
        print(f"Could not assign layers to: {unassigned} (likely circular dependency)")
    else:
        print("\nLayer assignment complete:")
        # Sort by layer
        sorted_services = sorted(services_data.items(), key=lambda x: x[1]["current_layer"])
        for n, s in sorted_services:
            print(f"  Layer {s['current_layer']}: {n}")

# Task: Implement assign_layers() function
# Verify no layer violations exist
if __name__ == "__main__":
    assign_layers(services_data)
