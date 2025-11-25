"""
Pulumi Stack: Cloud Native (AWS)
"""
import pulumi
import pulumi_aws as aws
import json

# Layer 1: Identity (IAM)
role = aws.iam.Role("layer1-role", 
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Effect": "Allow"
        }]
    })
)

# Layer 2: Storage (DynamoDB)
# Independent of Compute, dependent on Region (Layer 0)
table = aws.dynamodb.Table("layer2-table",
    attributes=[{"name": "Id", "type": "S"}],
    hash_key="Id",
    read_capacity=1,
    write_capacity=1
)

# Attach policy to Role (connecting Layer 1 and 2)
policy = aws.iam.RolePolicy("layer1-policy",
    role=role.id,
    policy=table.arn.apply(lambda arn: json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": ["dynamodb:GetItem", "dynamodb:PutItem"],
            "Resource": arn,
            "Effect": "Allow"
        }]
    }))
)

# Layer 3: Compute (Lambda)
# Hard Dependency on Role (L1) and Policy (L1/L2 link)
# Soft Dependency on Table (env var config)
lambda_func = aws.lambda_.Function("layer3-function",
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./app")
    }),
    role=role.arn,
    handler="handler.handle",
    runtime="python3.9",
    environment={
        "variables": {
            "TABLE_NAME": table.name
        }
    },
    opts=pulumi.ResourceOptions(depends_on=[policy])
)

pulumi.export("table_name", table.name)
pulumi.export("function_arn", lambda_func.arn)
