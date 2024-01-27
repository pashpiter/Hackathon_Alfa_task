postgres-up:
	@echo "Running postgres ..."
	cd infra && sudo docker compose --env-file=env/general up --build -d

postgres-down:
	@echo "Stopping postgres ..."
	cd infra && sudo docker compose --env-file=env/general down

postgres-down-volume:
	@echo "Stopping postgres and removing the volume ..."
	cd infra && sudo docker compose --env-file=env/general down -v

app-up:
	@echo "Starting FastAPI app ..."
	cd app && uvicorn main:app --reload
