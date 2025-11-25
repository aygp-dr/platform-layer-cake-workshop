"""
Exercise 3: Simulate disaster recovery
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Set, Dict
import time
from src.dependency_analyzer import Service, DependencyType

class RecoverySimulation:
    def __init__(self, services: Dict[str, Service]):
        self.services = services
        self.recovered = set()
        self.failed_attempts = []
        
    def can_recover(self, service_name: str) -> bool:
        """
        Check if service can be recovered
        All hard dependencies must be recovered first
        """
        service = self.services[service_name]
        
        for dep_name, dep_type in service.dependencies.items():
            if dep_type == DependencyType.HARD:
                if dep_name not in self.recovered:
                    return False
        
        return True
    
    def recover_service(self, service_name: str) -> bool:
        """
        Attempt to recover a service
        """
        if self.can_recover(service_name):
            print(f"Recovering {service_name}...")
            # time.sleep(0.1) # Simulate time (commented out for speed)
            self.recovered.add(service_name)
            print(f"SUCCESS: {service_name} recovered.")
            return True
        else:
            # print(f"FAILED: Cannot recover {service_name}, missing dependencies.")
            self.failed_attempts.append(service_name)
            return False

    def run_recovery(self):
        """
        Attempt to recover all services until stable
        """
        print("Starting recovery simulation...")
        print(f"Total services to recover: {len(self.services)}")
        
        iteration = 0
        while len(self.recovered) < len(self.services):
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            progress = False
            
            remaining = [s for s in self.services if s not in self.recovered]
            # Sort remaining by layer (low to high) to optimize recovery
            # This simulates the 'bottom-up' approach
            remaining.sort(key=lambda k: self.services[k].layer)
            
            for service_name in remaining:
                if self.recover_service(service_name):
                    progress = True
            
            if not progress:
                print("\nCRITICAL FAILURE: Deadlock detected. Cannot recover remaining services.")
                print(f"Unrecovered services: {remaining}")
                return False
                
        print("\nALL SERVICES RECOVERED SUCCESSFULLY!")
        return True

if __name__ == "__main__":
    # Setup services
    # Using a valid layered architecture
    services = {
        "aws-infra": Service("aws-infra", 1, {}),
        "iam": Service("iam", 2, {"aws-infra": DependencyType.HARD}),
        "vpc": Service("vpc", 3, {"iam": DependencyType.HARD, "aws-infra": DependencyType.HARD}),
        "database": Service("database", 4, {"vpc": DependencyType.HARD, "iam": DependencyType.HARD}),
        "app-api": Service("app-api", 5, {"database": DependencyType.HARD}),
        "frontend": Service("frontend", 6, {"app-api": DependencyType.HARD}),
        # Optional circular dependency to test failure
        # "circular-test": Service("circular-test", 5, {"frontend": DependencyType.HARD}),
    }
    
    # Inject bad dependency to test failure if needed
    # services["aws-infra"].dependencies["frontend"] = DependencyType.HARD 
    
    sim = RecoverySimulation(services)
    sim.run_recovery()
