nope:
	$(error Invalid target)

check-env-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

up:
	docker-compose up -d --build

down:
	docker-compose down

deploy:
	git pull && make restart

staging:
	docker-compose -f docker-compose.staging.yml up -d --build

restart:
	docker-compose restart app

stop:
	docker-compose stop

shell:
	docker-compose exec app ./manage.py shell

migrate:
	docker-compose exec app make migrate

admin:
	docker-compose exec app ./manage.py createsuperuser

test:
	docker-compose exec app make test

test-nomigrations:
	docker-compose exec app pytest --disable-warnings --nomigrations
