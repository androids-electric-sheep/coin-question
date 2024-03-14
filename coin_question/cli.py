import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coin game")
    parser.add_argument("--host", type=str, default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=9999, help="Port to bind to")
    args = parser.parse_args()
    return args
