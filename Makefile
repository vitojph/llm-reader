.PHONY: clean db analyze send

clean:
	rm -f llm-reader.db

db:
	uv run src/create-db.py

analyze:
	uv run src/analyze-news.py

all: clean db analyze

send:
	uv run src/send-emails.py
