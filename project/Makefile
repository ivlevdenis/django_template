nope:
	$(error Invalid target)

check-env-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

req:
	pip install --no-cache-dir --upgrade pip setuptools
	pip install --no-cache-dir -r requirements/common.txt

req-dev:
	pip install --no-cache-dir --upgrade pip setuptools
	pip install --no-cache-dir -r requirements/dev.txt

migrate:
	./manage.py makemigrations
	./manage.py migrate -v 3 --noinput

static:
	./manage.py collectstatic --noinput

app: migrate
	./manage.py runserver 0.0.0.0:8000

gunicorn: static migrate
	gunicorn \
		--bind 0.0.0.0:8000 \
		--workers 4 \
		apps.wsgi:application


celery:
	celery worker -A apps -l info -B -c 4

celery-beat:
	celery beat -A apps -l info

test:
	flake8
	pytest --disable-warnings
