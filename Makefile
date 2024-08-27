.PHONY: clean db analyze

clean:
	rm -f llm-reader.db

db:
	uv run src/create-db.py

analyze:
	uv run src/analyze-news.py

all: clean db analyze

