.PHONY: clean build run stop inspect
IMAGE_NAME = api-rose-${DST}
CONTAINER_NAME = api-rose-${DST}

build:
	docker build -t ${IMAGE_NAME} .

release:
	docker build \
		--build-arg VCS_REF=`git rev-parse --short HEAD` \
		--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` -t $(IMAGE_NAME) .

run_dev:
	docker run -d -p 5001:3001 -e environment='dev' -e port='5001' --net=host --restart=on-failure --name $(CONTAINER_NAME)dev $(IMAGE_NAME)dev

run_prod:
	docker run -d -p 3001:3001 -e environment='prod' -e port='3001:3001' --net=host --restart=on-failure --name $(CONTAINER_NAME)prod $(IMAGE_NAME)prod

inspect:
	docker inspect $(CONTAINER_NAME)

shell:
	docker exec -it $(CONTAINER_NAME) /bin/sh

stop:
	docker stop $(CONTAINER_NAME)

rm:
	docker rm $(CONTAINER_NAME)

rerun:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
	docker run -d -p 3001:3001 -e environment='prod' -e port='3001' --restart=on-failure --name $(CONTAINER_NAME) $(IMAGE_NAME)

clean:
	docker ps -a | grep '$(CONTAINER_NAME)' | awk -F " " '{print $1}' | xargs docker rm \
	docker images | grep '$(IMAGE_NAME)' | awk -F " " '{print $1}' | xargs docker rmi