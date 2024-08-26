from llm_reader.mail import compose_message
from llm_reader.page import Page

URL = "https://news.ycombinator.com"
p = Page(url=URL)
print(f"🔍 Parsing {URL}...")
p.sync()

print("🧠 Analyzing and summarizing the contents...")
p._get_links()

print("📫 Delivering emails...")
compose_message(p.children)
