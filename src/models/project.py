"""Project model for Portfolio OS.

Represents project metadata stored inside each project's metadata/project.json file.
Single source of truth for portfolio project information.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from .base import ProjectCategory, ProjectStatus


class Project(BaseModel):
    """Portfolio project metadata model.

    Represents the full metadata stored in the project's project.json file.

    Attributes:
        id: Unique project identifier (e.g. proj-xxxxxx).
        slug: URL-friendly identifier and directory name.
        title: Title of the project.
        subtitle: Short subtitle or tagline.
        description: Detailed description of the project.
        category: Category classification of the project.
        status: Progress status (draft, in_progress, completed, archived).
        year: Year the project was developed.
        technologies: List of technologies used.
        tags: Search tags or keywords.
        github: Link to the GitHub repository.
        website: Link to the deployed project website.
        demo: Link to a demonstration video or screenshot.
        role: Developer role on the project.
        featured: True if project is highlighted.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    id: str = Field(..., description="Unique project identifier")
    slug: str = Field(..., description="URL-friendly directory name")
    title: str = Field(..., description="Project title")
    subtitle: str | None = Field(None, description="Short project tagline")
    description: str | None = Field(None, description="Detailed project description")
    category: ProjectCategory = Field(..., description="Category classification")
    status: ProjectStatus = Field(
        ProjectStatus.DRAFT, description="Project progress status"
    )
    year: str | None = Field(None, description="Year the project was developed")
    technologies: list[str] = Field(
        default_factory=list, description="Technologies and languages used"
    )
    tags: list[str] = Field(default_factory=list, description="Search tags or keywords")
    github: str | None = Field(None, description="URL to GitHub or repository")
    website: str | None = Field(None, description="URL to deployed project website")
    demo: str | None = Field(None, description="URL to project demo or video")
    role: str | None = Field(None, description="Developer role")
    featured: bool = Field(default=False, description="Whether to feature on portfolio")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        json_schema_extra = {
            "example": {
                "id": "proj-001abc",
                "slug": "e-commerce-platform",
                "title": "E-Commerce Platform",
                "subtitle": "Scalable Django/React e-commerce solution",
                "description": "Full-stack e-commerce with microservices",
                "category": "personal",
                "status": "completed",
                "year": "2023",
                "technologies": ["Python", "Django", "React", "PostgreSQL"],
                "tags": ["Fullstack", "Web", "Backend"],
                "github": "https://github.com/user/ecommerce",
                "website": "https://ecommerce.example.com",
                "demo": "https://ecommerce.example.com/demo.mp4",
                "role": "Full Stack Developer",
                "featured": True,
                "created_at": "2026-06-23T18:52:28.000Z",
                "updated_at": "2026-06-23T18:52:28.000Z",
            }
        }
