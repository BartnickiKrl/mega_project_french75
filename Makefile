APP_DIR = letterboxd_stats

.PHONY: run_dev run migrate shell

run_dev:
	cd $(APP_DIR) && python manage.py runserver
	
run:
	cd $(APP_DIR) && uvicorn letterboxd_stats.asgi:application --reload

migrate:
	cd $(APP_DIR) && python manage.py makemigrations
	cd $(APP_DIR) && python manage.py migrate

shell:
	cd $(APP_DIR) && python manage.py shell