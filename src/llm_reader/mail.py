import os
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()


def compose_message(pages=List) -> None:
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")

    body = f"""<h1>News Summary from {formatted_date}</h1>"""
    for p in pages:
        body += f"""
        <h2><a href="{p[1]}" target="_blank">{p[0]}</a></h2>
        <p>{p[2]}</p>
        <p>categories: <tt>{p[3]}</tt></p>
        """
    res = send_email(body)
    if res == 202:
        print("✅ Emails delivered successfully!!")
    else:
        print(f"❌ Something went wrong: {res}")


def send_email(body: str) -> int:
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    message = Mail(
        from_email=os.environ.get("FROM_EMAIL"),
        to_emails=os.environ.get("TO_EMAIL"),
        subject=f"AI News {formatted_date}",
        html_content=body,
    )

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        resp = sg.send(message)
        return int(resp.status_code)
    except Exception as e:
        print(f"Failed to send email: {e} {resp.status_code}")
        return None
