import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from app import create_app

    app = create_app("testing")
    with app.test_client() as client:
        response = client.get("/health")
        if response.status_code != 200:
            raise SystemExit(f"Health check failed: {response.status_code}")


if __name__ == "__main__":
    main()
