.PHONY: dev up down build clean

VENV = .venv
FASTAPI = $(VENV)/bin/fastapi

# Run FastAPI in development mode
dev:
	@if [ -f $(FASTAPI) ]; then \
		$(FASTAPI) dev main.py; \
	else \
		fastapi dev main.py; \
	fi

# Start Docker Compose services in background and run FastAPI dev server
up:
	docker compose up -d
	$(MAKE) dev

# Stop Docker Compose services
down:
	docker compose down

# Build and start Docker Compose services
build:
	docker compose up --build
