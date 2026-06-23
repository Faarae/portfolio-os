"""Base data models for Portfolio OS.

Provides Pydantic models for type-safe data handling.
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class ProjectStatus(StrEnum):
    """Project status enumeration."""

    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ProjectCategory(StrEnum):
    """Project category enumeration."""

    ACADEMIC = "academic"
    COMPETITION = "competition"
    FREELANCE = "freelance"
    ORGANIZATION = "organization"
    PERSONAL = "personal"
    RESEARCH = "research"


class ProjectModel(BaseModel):
    """Project data model.

    Attributes:
        id: Unique project identifier.
        name: Project name.
        description: Project description.
        status: Current project status.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    id: str = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Project name")
    description: str | None = Field(None, description="Project description")
    status: ProjectStatus = Field(ProjectStatus.DRAFT, description="Project status")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        """Pydantic configuration."""

        use_enum_values = False
