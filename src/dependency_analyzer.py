"""
Analyze circular dependencies in service architecture
"""

from typing import Set, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class DependencyType(Enum):
    HARD = "hard"
    SOFT = "soft"

@dataclass
class Service:
    name: str
    layer: int
    dependencies: Dict[str, DependencyType]
    
def detect_circular_dependencies(services: Dict[str, Service]) -> List[Tuple[str, str]]:
    """
    Detect circular dependencies in service graph
    
    Returns list of (service_a, service_b) tuples representing cycles
    """
    cycles = []
    
    def has_path(start: str, end: str, visited: Set[str] = None) -> bool:
        if visited is None:
            visited = set()
        
        if start == end:
            return True
        
        if start in visited:
            return False
            
        visited.add(start)
        
        service = services.get(start)
        if not service:
            return False
            
        for dep_name, dep_type in service.dependencies.items():
            if dep_type == DependencyType.HARD:
                if has_path(dep_name, end, visited.copy()):
                    return True
        
        return False
    
    # Check each pair of services
    for svc_a in services:
        for svc_b in services:
            if svc_a != svc_b:
                # Check if A->B and B->A both exist
                if (has_path(svc_a, svc_b) and 
                    has_path(svc_b, svc_a)):
                    # Avoid duplicate entries
                    pair = tuple(sorted([svc_a, svc_b]))
                    if pair not in cycles:
                        cycles.append(pair)
    
    return cycles

def validate_layering(services: Dict[str, Service]) -> List[str]:
    """
    Validate that services only depend on lower layers
    
    Returns list of violations
    """
    violations = []
    
    for svc_name, service in services.items():
        for dep_name, dep_type in service.dependencies.items():
            if dep_type == DependencyType.HARD:
                dep_service = services.get(dep_name)
                if dep_service:
                    if dep_service.layer >= service.layer:
                        violation = (
                            f"{svc_name} (L{service.layer}) depends on "
                            f"{dep_name} (L{dep_service.layer})"
                        )
                        violations.append(violation)
    
    return violations

# Example usage
if __name__ == "__main__":
    # Atlassian 2021 problem scenario
    services = {
        "artifactory": Service(
            name="artifactory",
            layer=5,
            dependencies={"micros": DependencyType.HARD}
        ),
        "micros": Service(
            name="micros",
            layer=5,
            dependencies={"artifactory": DependencyType.HARD}
        )
    }
    
    cycles = detect_circular_dependencies(services)
    print(f"Circular dependencies found: {cycles}")
    
    violations = validate_layering(services)
    print(f"Layer violations: {violations}")
