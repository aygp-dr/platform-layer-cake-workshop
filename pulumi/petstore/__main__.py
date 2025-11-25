"""
Pulumi Stack: Event-Driven PetStore
"""
import json
import pulumi
import pulumi_aws as aws
import pulumi_grafana as grafana

# --- Layer 1: Event Bus ---
bus = aws.cloudwatch.EventBus("petstore-bus")

# --- Layer 2: Actor (Lambda) ---
# This actor processes "CreatePet" events
role = aws.iam.Role("actor-role", 
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Effect": "Allow"
        }]
    })
)

# Allow logging and tracing
aws.iam.RolePolicyAttachment("basic-exec",
    role=role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)

actor_func = aws.lambda_.Function("pet-actor",
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./actor")
    }),
    role=role.arn,
    handler="actor.handler",
    runtime="python3.9",
    tracing_config={"mode": "Active"}, # Enable X-Ray/OpenTelemetry
    environment={
        "variables": {
            "EVENT_BUS_NAME": bus.name
        }
    }
)

# Connect Bus -> Actor
rule = aws.cloudwatch.EventRule("pet-create-rule",
    event_bus_name=bus.name,
    event_pattern=json.dumps({
        "source": ["com.petstore"],
        "detail-type": ["PetCreated"]
    })
)

aws.cloudwatch.EventTarget("actor-target",
    rule=rule.name,
    event_bus_name=bus.name,
    arn=actor_func.arn
)

aws.lambda_.Permission("allow-cloudwatch",
    action="lambda:InvokeFunction",
    function=actor_func.name,
    principal="events.amazonaws.com",
    source_arn=rule.arn
)

# --- Layer 3: API Gateway (OpenAPI) ---
# We import the OpenAPI spec and inject the integration URI
# Note: In a real world scenario, we'd template the URI into the YAML.
# Here we simulate a simple proxy.

api = aws.apigatewayv2.Api("petstore-api",
    protocol_type="HTTP",
    body=open("../../petstore.yaml").read()
)

# --- Layer 4: Observability as Code ---
# Define a Grafana Dashboard for the PetStore
# Note: Requires GRAFANA_AUTH and GRAFANA_URL env vars
dashboard_json = json.dumps({
    "title": "PetStore Observability",
    "panels": [
        {
            "title": "Pet Actor Invocations",
            "type": "graph",
            "targets": [
                {"expr": f"aws_lambda_invocations_total{{function_name='{actor_func.name}'}}"}
            ]
        },
        {
            "title": "Event Bus Traffic",
            "type": "graph",
            "targets": [
                {"expr": f"aws_events_events_total{{event_bus='{bus.name}'}}"}
            ]
        }
    ]
})

# Only create if configured (mocking for workshop safety)
if pulumi.Config().get_bool("deploy_grafana"):
    dashboard = grafana.Dashboard("petstore-dashboard",
        config_json=dashboard_json
    )

pulumi.export("api_endpoint", api.api_endpoint)
pulumi.export("dashboard_json", dashboard_json)
