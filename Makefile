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