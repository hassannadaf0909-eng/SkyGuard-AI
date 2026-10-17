import json
import urllib.request


SERVICES = [
    ("backend", "http://localhost:8000/"),
    ("frontend", "http://localhost:8001/"),
]


def check_service(name, url):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {
                "service": name,
                "status": "up" if response.status == 200 else "error",
                "code": response.status,
                "body": body[:200],
            }
    except Exception as exc:  # pragma: no cover
        return {
            "service": name,
            "status": "down",
            "error": str(exc),
        }


if __name__ == "__main__":
    results = [check_service(name, url) for name, url in SERVICES]
    print(json.dumps(results, indent=2))
