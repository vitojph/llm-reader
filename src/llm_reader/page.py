from dataclasses import dataclass
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from llm_reader.ai import isATargetPage, isAValidPage, summarize


@dataclass
class Page:
    url: str
    title: str = ""
    text: str = ""
    summary: str = ""
    categories: List[str] = None
    links: List[str] = None
    updated_at: datetime = datetime.now()
    status: str = "init"

    def __post_init__(self):
        self.children: List[Page] = []
        self._update()

    def sync(self):
        try:
            res = requests.get(self.url)
            if res.status_code == 200:
                self.soup = BeautifulSoup(res.text, "html.parser")
                self.title = self.soup.find("title").text
                self.text = self.soup.get_text()
                summary = summarize(f"# {self.title} {self.text}")
                self.summary = summary.text
                self.categories = summary.categories
                self.status = "synced"
            else:
                self.status = "error"
        except Exception as e:
            raise e

    def _get_links(self) -> None:
        cells = self.soup.find_all("td", class_="title")
        for cell in cells:
            a = cell.find("a")
            if a and isAValidPage(a["href"]) and isATargetPage(a.text):
                p = Page(url=a["href"], title=a.text)
                try:
                    p.sync()
                    self.children.append(p)
                except Exception:
                    pass

    def _update(self):
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"Page(url='{self.url}', title={self.title})"
