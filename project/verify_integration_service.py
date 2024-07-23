from typing import List

from pydantic import BaseModel


class TechStackComponent(BaseModel):
    """
    Defines a single component of our technical stack, including its name and version.
    """

    name: str
    version: str


class VerifyIntegrationResponse(BaseModel):
    """
    Provides the result of the compatibility check, indicating success or detailing the issues encountered.
    """

    compatible: bool
    issues: List[str]
    recommendations: List[str]


def verify_integration(
    k1a_version: str,
    tech_stack_details: List[TechStackComponent],
    integration_strategy: str,
) -> VerifyIntegrationResponse:
    """
    Endpoint to verify 'k1a's integration compatibility with our system

    Args:
        k1a_version (str): The version of 'k1a' that is being considered for integration.
        tech_stack_details (List[TechStackComponent]): A detailed enumeration of our technical stack components and their versions.
        integration_strategy (str): Proposed strategy or approaches for integrating 'k1a' with our system, such as using APIs or as a module/plugin.

    Returns:
        VerifyIntegrationResponse: Provides the result of the compatibility check, indicating success or detailing the issues encountered.
    """
    compatible_versions = ["1.0", "2.0", "3.0"]
    compatible_tech_stacks = {
        "Python": "3.8",
        "FastAPI": "0.65.0",
        "PostgreSQL": "13",
        "Prisma": "2.20.0",
    }
    issues = []
    recommendations = []
    if k1a_version not in compatible_versions:
        issues.append(
            f"'k1a' version {k1a_version} is not compatible with the current system."
        )
        recommendations.append(
            f"Consider using one of the 'k1a' compatible versions: {', '.join(compatible_versions)}."
        )
    for component in tech_stack_details:
        required_version = compatible_tech_stacks.get(component.name)
        if required_version is None:
            issues.append(
                f"'k1a' integration does not support the tech stack component {component.name}."
            )
        elif component.version != required_version:
            issues.append(
                f"Component {component.name} version {component.version} is not compatible; requires version {required_version}."
            )
            recommendations.append(
                f"Upgrade {component.name} to version {required_version}."
            )
    compatible = len(issues) == 0
    return VerifyIntegrationResponse(
        compatible=compatible, issues=issues, recommendations=recommendations
    )
