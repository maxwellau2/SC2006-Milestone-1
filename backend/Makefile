
.PHONY: test clean migrate-full

# running the main.py
run:
	python main.py

enable-ollama-gpu:
	watch -n 0.5 nvidia-smi

run-reloadable: 
	uvicorn main:app --reload

# sync dependancies
sync:
	pip install -r "requirements.txt"

# update dependencies
update:
	pip freeze >> requirements.txt

# run migrations
migrate-up:
	python migrate.py up

migrate-down:
	python migrate.py down

seed:
	python seed.py

migrate-full:
	make migrate-down && make migrate-up && make seed

generate-architecture:
	tree -I 'venv|__pycache__' -I 'images' > structure.txt

lint:
	black .

test:
	make migrate-full && PYTHONPATH=./ pytest --verbose --disable-warnings && make-migrate-full

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -rf .pytest_cache