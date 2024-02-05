up:
	@echo "Running service ..."
	cd infra && sudo docker compose --env-file=env/general up --build -d

down:
	@echo "Stopping service ..."
	cd infra && sudo docker compose --env-file=env/general down

down-volumes:
	@echo "Stopping service and removing all volumes ..."
	cd infra && sudo docker compose --env-file=env/general down -v

dev-up:
	@echo "Running service in a development mode ..."
	cd infra && sudo docker compose -f docker-compose.yaml -f docker-compose-dev.yaml --env-file=env/general up --build -d

dev-down:
	@echo "Stopping service in a development mode ..."
	cd infra && sudo docker compose -f docker-compose.yaml -f docker-compose-dev.yaml --env-file=env/general down

dev-down-volumes:
	@echo "Stopping service and removing all volumes in a development mode ..."
	cd infra && sudo docker compose -f docker-compose.yaml -f docker-compose-dev.yaml --env-file=env/general down -v

test-up:
	@echo "Running test ..."
	cd infra && sudo docker compose -f docker-compose-test.yaml --env-file=test-env/general up --build -d

test-down:
	@echo "Running test ..."
	cd infra && sudo docker compose -f docker-compose-test.yaml --env-file=test-env/general down

test-down-volumes:
	@echo "Running test ..."
	cd infra && sudo docker compose -f docker-compose-test.yaml --env-file=test-env/general down -v

app-up:
	@echo "Starting FastAPI app ..."
	cd app && uvicorn main:app --reload
