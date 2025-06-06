# Variables
COMPOSE=docker-compose
WEB=web

.PHONY: help build up down logs shell migrate createsuperuser celery

help:
	@echo "Available commands:"
	@echo "  make build              Build Docker images"
	@echo "  make up                 Start all containers"
	@echo "  make down               Stop all containers"
	@echo "  make logs               Show logs"
	@echo "  make shell              Django shell"
	@echo "  make migrate            Run Django migrations"
	@echo "  make createsuperuser    Create Django superuser"
	@echo "  make celery             Run Celery worker"

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

shell:
	$(COMPOSE) exec $(WEB) python manage.py shell

migrate:
	$(COMPOSE) exec $(WEB) python manage.py migrate

migrations:
	$(COMPOSE) exec $(WEB) python manage.py makemigrations

createsuperuser:
	$(COMPOSE) exec $(WEB) python manage.py createsuperuser

celery:
	$(COMPOSE) exec celery celery -A project_name worker --loglevel=info
