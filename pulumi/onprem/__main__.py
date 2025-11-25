"""
Pulumi Stack: On-Prem / Bare Metal (FreeBSD Focus)
"""
import platform
import pulumi
from pulumi_command import local

# 1. Verify Environment (Layer 0)
# We want to ensure we are running on the expected architecture
os_check = local.Command(
    "os-check",
    create="uname -a",
    triggers=[platform.system()] # Re-run if platform changes (unlikely but good practice)
)

pulumi.export("host_info", os_check.stdout)

# 2. Define Layers using Directory Structures

# Layer 1: Storage (Base)
# On FreeBSD, we might use ZFS datasets, but here we simulate with directories
layer1_storage = local.Command(
    "layer1-storage",
    create="mkdir -p ./layers/storage/data",
    delete="rm -rf ./layers/storage",
    opts=pulumi.ResourceOptions(depends_on=[os_check])
)

# Layer 2: Configuration (Depends on Storage)
# We write a config file that points to the storage layer
config_content = 'STORAGE_PATH=./layers/storage/data\nDB_PORT=5432'
layer2_config = local.Command(
    "layer2-config",
    create=f"mkdir -p ./layers/config && echo '{config_content}' > ./layers/config/app.conf",
    delete="rm -rf ./layers/config",
    opts=pulumi.ResourceOptions(depends_on=[layer1_storage])
)

# Layer 3: Application Service (Depends on Config)
# We verify the config exists before "starting" the service
layer3_service = local.Command(
    "layer3-service",
    create="cat ./layers/config/app.conf && echo 'Service Started' > ./layers/service.status",
    delete="rm -f ./layers/service.status",
    opts=pulumi.ResourceOptions(depends_on=[layer2_config])
)

# Violation Simulation (Optional)
# Uncommenting this would create a circular dependency if Pulumi allowed it,
# or a logic error if we try to make Storage depend on Service.
#
# bad_dependency = local.Command("bad", ..., opts=pulumi.ResourceOptions(depends_on=[layer3_service]))
# layer1_storage.depends_on = [bad_dependency] # This would cause a cycle

pulumi.export("service_status", layer3_service.stdout)
