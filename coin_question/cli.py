import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coin game")
    parser.add_argument("--host", type=str, default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=9999, help="Port to bind to")
    parser.add_argument(
        "--game-size",
        type=int,
        default=1_000,
        help="Number of coins to include in the game",
    )
    parser.add_argument(
        "--faulty-coin", type=int, required=False, help="Coin to mark as the faulty one"
    )
    args = parser.parse_args()

    # Validate cli arguments make sense
    if args.game_size < 1:
        raise ValueError("Game size must be greater than one")
    elif args.faulty_coin is not None:
        if args.faulty_coin < 0 or args.faulty_coin >= args.game_size:
            raise ValueError("Faulty coin must be indexed between 0 and game-size")

    return args
