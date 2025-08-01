# Makefile for lovelyRSS

.PHONY: help install build test clean

help:
	@echo "Commands:"
	@echo "  install    - Install dependencies"
	@echo "  build      - Generate the static site"
	@echo "  test       - Run the test suite"
	@echo "  clean      - Remove generated files"

install:
	@echo "Installing dependencies..."
	uv sync --dev

build:
	@echo "Building static site..."
	uv run python scripts/fetch_feeds.py

test:
	@echo "Running tests..."
	uv run python -m pytest

clean:
	@echo "Cleaning up generated files..."
	rm -f latest_rss.xml latest_feeds.xml index.html last_run.json
