all:build

build:
	@echo "Building..."
	docker-compose up -d --build

up:
	@echo "Starting..."
	docker-compose up -d

down:
	@echo "Stopping..."
	docker-compose down

rebuild:
	@echo "Recreating all services..."
	docker-compose down && docker-compose build --no-cache && docker-compose up -d

clean:
	@echo "Delete all containers and volumes..."
	docker-compose down -v

logs:
	@echo "Printing logs..."
	docker-compose logs

status:
	@echo "Docker status..."
	docker ps

black:
	@echo "Formatting with black..."
	isort --apply ./service/
	python3 -m black ./service/

.PHONY: build up down rebuild clean logs status black
