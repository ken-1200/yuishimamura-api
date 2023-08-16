MARK:="not optional"

-include .env

clean:
	docker compose stop
	docker compose rm -f
	rm -rf test_modules

build:
	docker compose build yuishimamura-api

build-mainimage:
	docker build -t ${APP_IMAGE} -f Dockerfile-SLS .

run:
	docker compose up yuishimamura-api

requirements.lock: requirements.txt
	docker run -it --rm -v $$(pwd):/app -w /app python:3.10 bash -c 'pip install -r requirements.txt && pip freeze > requirements.lock'

test_modules: requirements_test.txt
	rm -rf test_modules
	docker run -it --rm -v $$(pwd):/app -w /app python:3.10 bash -c 'pip install -t test_modules -r requirements_test.txt'

test: test_modules
	@make test-pytest

test-pytest:
	docker compose exec -e PYTHONPATH=test_modules yuishimamura-api python3 -m pytest -m ${MARK}

push-mainimage:
	aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ${ECR_DOMAIN}
	@make build-mainimage
	docker tag ${APP_IMAGE}:latest ${ECR_REPO_APP}:latest
	docker push ${ECR_REPO_APP}:latest

deploy:
	@make push-mainimage
	yarn sls deploy --stage prod
