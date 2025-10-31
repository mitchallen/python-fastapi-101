# FastAPI Demo Project Makefile

.PHONY: help install run dev test test-cov coverage coverage-report coverage-html clean setup up stop

# Default target - show help
help:
	@echo "FastAPI Demo Project - Available Commands:"
	@echo ""
	@echo "  make up        - Set up everything and run the server in development mode"
	@echo "  make setup     - Set up virtual environment and install dependencies"
	@echo "  make install   - Install dependencies (requires active virtual environment)"
	@echo "  make run       - Run the FastAPI application"
	@echo "  make dev       - Run the application in development mode with auto-reload"
	@echo "  make stop      - Stop any running FastAPI processes on port 8000"
	@echo "  make test      - Run tests without coverage"
	@echo "  make test-cov  - Run tests with coverage report"
	@echo "  make coverage  - Generate and display coverage report"
	@echo "  make coverage-html - Generate HTML coverage report and open it"
	@echo "  make clean     - Clean up generated files and virtual environment"
	@echo "  make help      - Show this help message"
	@echo ""
	@echo "Quick Start:"
	@echo "  make up        - One command to set up and run everything!"
	@echo "  OR:"
	@echo "  1. make setup"
	@echo "  2. make dev"
	@echo ""
	@echo "Python Requirements:"
	@echo "  - Python 3.7+ is required"
	@echo "  - The Makefile will try python3 first, then python"
	@echo ""
	@echo "Then visit http://localhost:8000/docs for the API documentation"

# Set up everything and run the server
up:
	@echo "Setting up and starting FastAPI application..."
	@if [ ! -d "venv" ]; then \
		echo "Creating virtual environment..."; \
		if command -v python3 >/dev/null 2>&1; then \
			python3 -m venv venv; \
		elif command -v python >/dev/null 2>&1; then \
			python -m venv venv; \
		else \
			echo "Error: Python not found. Please install Python 3.7+ and try again."; \
			exit 1; \
		fi; \
		echo "Installing dependencies..."; \
		./venv/bin/pip install --upgrade pip; \
		./venv/bin/pip install -r requirements.txt; \
		echo "Setup complete! Starting server..."; \
	fi
	@echo "Starting FastAPI application in development mode..."
	@if lsof -ti:8000 >/dev/null 2>&1; then \
		echo "Port 8000 is already in use. Stopping existing processes..."; \
		lsof -ti:8000 | xargs kill -9 2>/dev/null || true; \
		sleep 2; \
	fi
	./venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Set up virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment..."
	@if command -v python3 >/dev/null 2>&1; then \
		python3 -m venv venv; \
	elif command -v python >/dev/null 2>&1; then \
		python -m venv venv; \
	else \
		echo "Error: Python not found. Please install Python 3.7+ and try again."; \
		exit 1; \
	fi
	@echo "Installing dependencies..."
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "Setup complete! Activate the virtual environment with: source venv/bin/activate"

# Install dependencies (requires active virtual environment)
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run the FastAPI application
run:
	@echo "Starting FastAPI application..."
	uvicorn main:app --host 0.0.0.0 --port 8000

# Run in development mode with auto-reload
dev:
	@echo "Starting FastAPI application in development mode..."
	@if lsof -ti:8000 >/dev/null 2>&1; then \
		echo "Port 8000 is already in use. Stopping existing processes..."; \
		lsof -ti:8000 | xargs kill -9 2>/dev/null || true; \
		sleep 2; \
	fi
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Stop any running FastAPI processes
stop:
	@echo "Stopping FastAPI processes on port 8000..."
	@if lsof -ti:8000 >/dev/null 2>&1; then \
		lsof -ti:8000 | xargs kill -9 2>/dev/null || true; \
		echo "FastAPI processes stopped."; \
	else \
		echo "No FastAPI processes found on port 8000."; \
	fi

# Run tests without coverage
test:
	@echo "Running tests..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Running 'make setup' first..."; \
		$(MAKE) setup; \
	fi
	./venv/bin/pytest test_main.py -v

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Running 'make setup' first..."; \
		$(MAKE) setup; \
	fi
	./venv/bin/pytest test_main.py -v --cov=main --cov-report=term-missing --cov-report=html

# Generate coverage report
coverage:
	@echo "Generating coverage report..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Running 'make setup' first..."; \
		$(MAKE) setup; \
	fi
	./venv/bin/pytest test_main.py --cov=main --cov-report=term-missing --cov-report=html
	@echo ""
	@echo "Coverage report generated!"
	@echo "Terminal report shown above."
	@echo "HTML report available at: htmlcov/index.html"

# Generate and open HTML coverage report
coverage-html:
	@echo "Generating HTML coverage report..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Running 'make setup' first..."; \
		$(MAKE) setup; \
	fi
	./venv/bin/pytest test_main.py --cov=main --cov-report=html --cov-report=term
	@echo ""
	@echo "Opening HTML coverage report..."
	@if command -v open >/dev/null 2>&1; then \
		open htmlcov/index.html; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open htmlcov/index.html; \
	else \
		echo "HTML report generated at: htmlcov/index.html"; \
		echo "Please open it manually in your browser."; \
	fi

# Clean up generated files and virtual environment
clean:
	@echo "Cleaning up..."
	rm -rf venv/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "Cleanup complete!"

# Default target
.DEFAULT_GOAL := help
