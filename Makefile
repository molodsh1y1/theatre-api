FILE_NAME := manage.py
RUN := poetry run

.PHONY: install
install:
	$(RUN) install

.PHONY: migrate
migrate:
	$(RUN) python $(FILE_NAME) migrate

.PHONY: migrations
migrations:
	$(RUN) python $(FILE_NAME) makemigrations

.PHONY: runserver
runserver:
	$(RUN) python $(FILE_NAME) runserver

.PHONY: superuser
superuser:
	$(RUN) python $(FILE_NAME) createsuperuser

.PHONY: update
update: install migrate

.PHONY: flake8
flake8:
	$(RUN) pflake8 .

.PHONY: test
test:
	$(RUN) coverage run $(FILE_NAME) test
	$(RUN) coverage report

.PHONY: test-clean
test-clean:
	$(RUN) coverage erase

.PHONY: isort
isort:
	$(RUN) isort .

.PHONY: docker-compose up build
up build:
	docker-compose up --build

.PHONY: docker-compose down
down:
	docker-compose down
