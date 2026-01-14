"""Command-line interface for md2pdf."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from md2pdf import __version__
from md2pdf.config import find_config, load_config
from md2pdf.converter import convert_markdown_to_pdf


@click.command()
@click.argument(
    "input_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Output PDF file path. Defaults to input filename with .pdf extension.",
)
@click.option(
    "-c",
    "--config",
    "config_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to YAML configuration file.",
)
@click.option(
    "--no-config",
    is_flag=True,
    help="Ignore all configuration files and use defaults only.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose output.",
)
@click.version_option(version=__version__, prog_name="md2pdf")
def main(
    input_file: Path,
    output: Path | None,
    config_path: Path | None,
    no_config: bool,
    verbose: bool,
) -> None:
    """Convert a Markdown file to PDF.

    INPUT_FILE is the path to the Markdown file to convert.

    \b
    Examples:
        md2pdf document.md
        md2pdf document.md -o output.pdf
        md2pdf document.md --config custom.yaml
    """
    # Determine output path
    if output is None:
        output = input_file.with_suffix(".pdf")

    # Load configuration
    if no_config:
        config_data: dict = {}
        if verbose:
            click.echo("Using default configuration (--no-config specified).")
    elif config_path:
        config_data = load_config(config_path)
        if verbose:
            click.echo(f"Using config: {config_path}")
    else:
        found_config = find_config(input_file)
        if found_config:
            config_data = load_config(found_config)
            if verbose:
                click.echo(f"Found config: {found_config}")
        else:
            config_data = {}
            if verbose:
                click.echo("No config file found, using defaults.")

    # Convert
    try:
        if verbose:
            click.echo(f"Converting: {input_file}")
        convert_markdown_to_pdf(input_file, output, config_data, verbose=verbose)
        click.echo(f"Created: {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
