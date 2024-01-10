"""Download attachments from Odoo by their ID"""
import re
from argparse import ArgumentParser
from getpass import getpass
from html.parser import HTMLParser
from os import getenv
from urllib.parse import unquote, urljoin

import requests

file_pattern = re.compile(r"filename.*(''|\")(.*)")


class CSRFParser(HTMLParser):
    """Parser to extract Odoo's CSRF token from an HTML page."""

    def __init__(self):
        super().__init__()
        self.token = ""

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            is_csrf = False
            token = False
            for name, value in attrs:
                if name == "name" and value == "csrf_token":
                    is_csrf = True
                if name == "value":
                    token = value

            if is_csrf:
                self.token = token


def main():
    parser = ArgumentParser()
    parser.add_argument("url", help="Odoo base URL")
    parser.add_argument("--user", help="Odoo username", default=getenv("ODOO_USER"))
    parser.add_argument("--password", help="Username's password", default=getenv("ODOO_PASSWORD"))
    args = parser.parse_args()

    user = args.user
    if not user:
        user = input("Username: ")

    password = args.password
    if not password:
        password = getpass("Password: ")

    login_url = urljoin(args.url, "/web/login")
    session = requests.Session()
    parser = CSRFParser()

    parser.feed(session.get(login_url).text)
    if not parser.token:
        print("CSRF Token not found. Can't continue")
        return 1

    response = session.post(
        login_url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"login": user, "password": password, "csrf_token": parser.token, "redirect": ""},
        allow_redirects=False,
    )
    if response.status_code != 303:
        print("Failed to login. Can't continue")
        return 1

    while attachment_id := input("Attachment ID: "):
        download_url = urljoin(args.url, f"/web/content/ir.attachment/{attachment_id}/datas")
        response = session.get(download_url, params={"download": True})
        if response.status_code != 200:
            print(f"Failed to download, status code {response.status_code}")
            continue

        disposition = response.headers["Content-Disposition"]
        match = file_pattern.search(disposition)
        if match:
            filename = unquote(match.group(2))
        else:
            filename = f"attachment-{attachment_id}"

        with open(filename, "wb") as file_fd:
            file_fd.write(response.content)

    print("Goodbye :)")
    return 0


if __name__ == "__main__":
    main()
