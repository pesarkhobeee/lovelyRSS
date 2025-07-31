# Gemini Agent Instructions for lovelyRSS

This document provides instructions for Gemini agents on how to interact with the `lovelyRSS` project.

## About This Project

`lovelyRSS` is a simple, static RSS reader that helps you share what you read. It fetches a list of RSS feeds from an OPML file, processes the entries, and generates a beautiful, static website that you can easily share with friends. The project is designed to be run automatically using GitHub Actions and is built to be easily forkable and configurable by users.

## Key Files

-   `scripts/fetch_feeds.py`: The main Python script that contains all the logic for fetching and processing feeds.
-   `scripts/utils.py`: Utility functions used by the main script.
-   `feeds.opml`: **User-provided file.** A list of RSS feeds in OPML format. This file is git-ignored.
-   `rss.opml.template`: A template for the `feeds.opml` file.
-   `config.json`: **User-provided file.** Configuration for the site, such as title, description, and update interval. This file is git-ignored.
-   `config.json.template`: A template for the `config.json` file.
-   `templates/index.html`: The Jinja2 template for the main HTML output.
-   `pyproject.toml`: Defines project metadata and dependencies, managed by `uv`.
-   `.github/workflows/`: Contains the GitHub Actions workflows for testing, updating feeds, and formatting the OPML file.
-   `tests/`: Contains the test suite for the project.

## Development Setup

The project uses `uv` for dependency management and a `Makefile` for common tasks.

- `make install`: Install all necessary dependencies.
- `make build`: Build the static site.
- `make test`: Run the test suite.
- `make clean`: Remove all generated files.

Alternatively, you can run the commands manually:

1.  **Install dependencies:**
    ```bash
    uv sync --dev
    ```

## Running the Application

To run the main script locally:

```bash
make build
```

Or:

```bash
uv run python scripts/fetch_feeds.py
```

This will generate the output files in the project root based on the `feeds.opml` and `config.json` files. If those files don't exist, it will fall back to using the `.template` versions.

## Running Tests

To run the tests:

```bash
make test
```

Or:

```bash
uv run pytest
```

**Note:** If you encounter issues related to external tools like `ddtrace`, you may need to disable them for the test run:
```bash
DD_TRACE_ENABLED=false uv run pytest -p no:ddtrace
```

## Configuration

User-specific configuration is handled by two files, which are ignored by git:

1.  `feeds.opml`: A list of RSS feeds. Users should copy `rss.opml.template` to `feeds.opml` and add their feeds.
2.  `config.json`: Site-wide settings. Users should copy `config.json.template` to `config.json` and customize the values.

This separation allows users to update the core project files without creating merge conflicts with their personal configuration.