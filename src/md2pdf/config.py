"""Configuration file handling for md2pdf."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class MarginsConfig:
    """Page margin configuration."""

    top: str = "2.5cm"
    bottom: str = "2.5cm"
    left: str = "2cm"
    right: str = "2cm"


@dataclass
class FontFace:
    """Custom font-face registration."""

    family: str = ""
    src: str = ""  # Path to font file (TTF, OTF)
    weight: str = "normal"  # normal, bold, 100-900
    style: str = "normal"  # normal, italic


@dataclass
class FontConfig:
    """Font configuration."""

    family: str = "Helvetica, Arial, sans-serif"
    size: str = "11pt"
    line_height: float = 1.5


@dataclass
class HeaderFooterConfig:
    """Header or footer configuration."""

    content: str = ""
    height: str = "1.5cm"


@dataclass
class TitlePageConfig:
    """Title page configuration."""

    enabled: bool = False
    content: str = ""


@dataclass
class Config:
    """Complete md2pdf configuration."""

    font: FontConfig = field(default_factory=FontConfig)
    fonts: list[FontFace] = field(default_factory=list)
    margins: MarginsConfig = field(default_factory=MarginsConfig)
    page_size: str = "A4"
    header: HeaderFooterConfig = field(default_factory=HeaderFooterConfig)
    footer: HeaderFooterConfig = field(default_factory=HeaderFooterConfig)
    title_page: TitlePageConfig = field(default_factory=TitlePageConfig)


def find_config(input_file: Path) -> Path | None:
    """Find configuration file using search hierarchy.

    Search order:
    1. Same directory as input file (md2pdf.yaml)
    2. Current working directory (md2pdf.yaml)
    3. User home directory (~/.md2pdf.yaml)

    Args:
        input_file: Path to the input Markdown file.

    Returns:
        Path to config file if found, None otherwise.
    """
    search_paths = [
        input_file.parent / "md2pdf.yaml",
        Path.cwd() / "md2pdf.yaml",
        Path.home() / ".md2pdf.yaml",
    ]

    for path in search_paths:
        if path.is_file():
            return path

    return None


def load_config(config_path: Path) -> dict[str, Any]:
    """Load and parse YAML configuration file.

    Args:
        config_path: Path to the YAML config file.

    Returns:
        Dictionary containing configuration values.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def merge_config(user_config: dict[str, Any]) -> Config:
    """Merge user configuration with defaults.

    Args:
        user_config: User-provided configuration dictionary.

    Returns:
        Complete Config object with defaults filled in.
    """
    config = Config()

    if "font" in user_config:
        font_data = user_config["font"]
        config.font = FontConfig(
            family=font_data.get("family", config.font.family),
            size=font_data.get("size", config.font.size),
            line_height=font_data.get("line_height", config.font.line_height),
        )

    if "margins" in user_config:
        margins_data = user_config["margins"]
        config.margins = MarginsConfig(
            top=margins_data.get("top", config.margins.top),
            bottom=margins_data.get("bottom", config.margins.bottom),
            left=margins_data.get("left", config.margins.left),
            right=margins_data.get("right", config.margins.right),
        )

    if "page_size" in user_config:
        config.page_size = user_config["page_size"]

    if "header" in user_config:
        header_data = user_config["header"]
        config.header = HeaderFooterConfig(
            content=header_data.get("content", ""),
            height=header_data.get("height", "1.5cm"),
        )

    if "footer" in user_config:
        footer_data = user_config["footer"]
        config.footer = HeaderFooterConfig(
            content=footer_data.get("content", ""),
            height=footer_data.get("height", "1.5cm"),
        )

    if "title_page" in user_config:
        title_page_data = user_config["title_page"]
        config.title_page = TitlePageConfig(
            enabled=title_page_data.get("enabled", False),
            content=title_page_data.get("content", ""),
        )

    if "fonts" in user_config:
        config.fonts = [
            FontFace(
                family=font.get("family", ""),
                src=font.get("src", ""),
                weight=font.get("weight", "normal"),
                style=font.get("style", "normal"),
            )
            for font in user_config["fonts"]
        ]

    return config
