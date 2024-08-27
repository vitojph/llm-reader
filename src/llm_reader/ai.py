import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class InterestingPage(BaseModel):
    is_interesting: bool


class Summary(BaseModel):
    text: str
    categories: List[str]


isATargetPagePrompt = f"""You are an enthusiast and practitioner of the following areas:
{os.environ.get("CATEGORIES")}
Read the following title of a web page and decide whether it looks interesting or not"""

summarizePrompt = f"""You are an expert practitioner in areas such as
{os.environ.get("CATEGORIES")}
Summarize the following in about a paragragh, and generate a list of 3-5 categories that describe the contents"""


def isATargetPage(title: str) -> bool:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": isATargetPagePrompt},
            {
                "role": "user",
                "content": title,
            },
        ],
        response_format=InterestingPage,
    )
    resp = completion.choices[0].message.parsed
    return resp.is_interesting


def isAValidPage(url: str) -> bool:
    if len(url) < 5:
        return False
    elif url.endswith("pdf"):
        return False
    elif ("twitter.com" or "x.com") in url:
        return False
    return True


def summarize(text: str) -> str:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": summarizePrompt},
            {
                "role": "user",
                "content": text,
            },
        ],
        response_format=Summary,
    )
    resp = completion.choices[0].message.parsed
    return resp
