"""Send a Websocket Handshake to an Odoo Server. Useful to debug bus issues."""
from argparse import ArgumentParser
from base64 import b64encode
from pprint import pprint
from random import randbytes
from urllib.parse import urljoin, urlparse

from requests import get


def main():
    parser = ArgumentParser()
    parser.add_argument("url", help="Base URL of the Odoo Server. Example: http://localhost:8069")
    args = parser.parse_args()

    key = b64encode(randbytes(16))
    parsed_url = urlparse(args.url)

    response = get(
        urljoin(args.url, "/websocket"),
        headers={
            "Host": parsed_url.hostname,
            "Origin": args.url,
            "Connection": "Upgrade",
            "Upgrade": "websocket",
            "Sec-Websocket-Extensions": "permessage-deflate; client_max_window_bits",
            "Sec-WebSocket-Version": "13",
            "Sec-WebSocket-Key": key,
        },
        timeout=10,
    )

    print(f"HTTP {response.status_code}")
    pprint(dict(response.headers))
    print(response.content.decode("utf-8"))


if __name__ == "__main__":
    main()
