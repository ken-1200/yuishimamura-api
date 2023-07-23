MARK:="not optional"
# ./app/envs/.env.local を指定。
STAGE:=local

clean:
	STAGE=${STAGE} docker compose stop
	STAGE=${STAGE} docker compose rm -f

build:
	STAGE=${STAGE} docker compose build yuishimamura-api

build-mainimage:
	docker build -t p01-yuishimamura-api -f Dockerfile-SLS .

run:
	STAGE=${STAGE} docker compose up yuishimamura-api

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
	aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 909937076167.dkr.ecr.ap-northeast-1.amazonaws.com
	@make build-mainimage
	docker tag p01-yuishimamura-api:latest 909937076167.dkr.ecr.ap-northeast-1.amazonaws.com/p01-yuishimamura-api:latest
	docker push 909937076167.dkr.ecr.ap-northeast-1.amazonaws.com/p01-yuishimamura-api:latest

deploy:
	@make push-mainimage
	yarn sls deploy --stage prod
