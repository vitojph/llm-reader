from llm_reader.db import fetch_pages
from llm_reader.mail import compose_message

pages = fetch_pages()
print(f"Sending {len(pages)} readings...")
compose_message(pages)
