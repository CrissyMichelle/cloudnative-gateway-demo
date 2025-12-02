.PHONY: wheel create-image push run


push: docker/Dockerfile
	docker buildx build --push --tag p6acr.azurecr.io/login:latest -f docker/Dockerfile  . 

run: push
	docker run -p 8080:8080 p3acr.azurecr.io/login:latest

