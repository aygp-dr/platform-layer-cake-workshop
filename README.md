# Platform Layer Cake Workshop

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Work_In_Progress-orange)](https://github.com/aygp-dr/platform-layer-cake-workshop)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A workshop on **Layered Recovery Architecture** and breaking circular dependencies in platform engineering.

## Overview

This workshop explores the "Layer Cake" architecture pattern for platform recovery, drawing lessons from:
*   **Atlassian's CPR (Continuous PaaS Recovery) Program**: How they migrated from a tangled "ball of mud" to a layered architecture to enable disaster recovery.
*   **Netflix's Chaos Engineering**: Using steady-state hypothesis and fault injection to validate resilience.

The core problem addressed is **Circular Dependencies** (e.g., Service A needs Service B, Service B needs Service A), which make cold-start recovery impossible during a total outage.

## Workshop Content

All content is available in [setup.org](setup.org).

### Exercises

1.  **Dependency Mapping**: Identify and visualize circular dependencies in a service graph.
2.  **Layer Assignment**: Implement an algorithm to assign services to layers (N) such that they only depend on layers < N.
3.  **Recovery Simulation**: Simulate a disaster recovery scenario to verify that the layered architecture allows for a bottom-up restoration of services.

## Getting Started

### Prerequisites
*   Python 3.9+
*   Emacs (optional, for Org mode interaction)
*   Make

### Setup

Initialize the workshop:

```bash
make setup
```

### Running Exercises

You can run the solution code for the exercises using:

```bash
make test
```

## Concepts

### The Layer Cake Rule
> A component in layer N can only have hard dependencies on lower layers (N-1, N-2, etc.).

### Hard vs. Soft Dependencies
*   **Hard Dependency**: Service cannot function/start without it (e.g., Database, IAM).
*   **Soft Dependency**: Service works with reduced functionality (e.g., Logging, Metrics).

## References

*   [Removing dependency tangles in the Atlassian Platform](https://www.atlassian.com/blog/atlassian-engineering/removing-dependency-tangles-in-the-atlassian-platform-for-increased-reliability-and-recoverability)
*   [Netflix Technology Blog](https://netflixtechblog.com/)

## Additional Resources

*   [Open Source Chaos & Resilience Testing Tools](CHAOS_TOOLS.md): A curated list of tools for evaluating resilience in production, IaC, and platform tooling.
