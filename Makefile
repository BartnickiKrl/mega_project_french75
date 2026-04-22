APP_DIR = letterboxd_stats

.PHONY: run migrate shell

run:
	cd $(APP_DIR) && python manage.py runserver

migrate:
	cd $(APP_DIR) && python manage.py makemigrations
	cd $(APP_DIR) && python manage.py migrate

shell:
	cd $(APP_DIR) && python manage.py shell