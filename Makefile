run:
	docker-compose up

test:
	# Unit Testing
	docker build -t rutigs/redisproxytest --file docker/testDockerfile .
	docker run -t rutigs/redisproxytest

	docker-compose up -d
	docker build -t rutigs/redisproxye2e --file docker/e2eTestDockerfile .
	docker run --net host -t rutigs/redisproxye2e

