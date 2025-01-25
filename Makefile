.PHONY: run test lint format clean

run:
	streamlit run src/ppt_chatbot/main.py

test:
	pytest -v tests/

lint:
	flake8 src/ tests/
	mypy src/ tests/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache .pytest_cache __pycache__ logs/ temp/