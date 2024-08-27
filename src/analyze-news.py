from llm_reader.db import add_page
from llm_reader.page import Page

URL = "https://news.ycombinator.com"
p = Page(url=URL)
print(f"🔍 Parsing {URL}...")

p.sync()

print("🧠 Analyzing and summarizing the contents...")
p._get_links()

print("🗄️ Updating the database...")
for page in p.children:
    add_page(page)
print("Done!")
