

.PHONY: script

script:
	kubectl -n istio-system delete cm luawebhook
	kubectl -n istio-system create cm luawebhook --from-file scripts/plugin.lua


.PHONE: deploy docker

docker:
	docker build . -t gcr.io/istio-testing/luawebhook:mjog
	@echo "Retag and push the image"

deploy:
	kubectl -n istio-system apply -f luawebhook.yaml
