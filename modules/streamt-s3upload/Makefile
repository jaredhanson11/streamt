docker-user=jaredhanson11
name=${docker-user}/streamt-s3upload

build:
	docker build . -t ${name}:latest
push: build
	docker push ${name}:latest
