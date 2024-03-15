import math
import random
import socketserver
import uuid

import structlog

from . import cli

logger = structlog.get_logger()


class CoinGame:
    def __init__(self, game_id: str, game_size: int, faulty_coin: int) -> None:
        self.game_id = game_id
        self.game_size = game_size
        self.faulty_coin = faulty_coin

        logger.info(
            "Creating game",
            game_id=self.game_id,
            game_size=self.game_size,
            faulty_coin=self.faulty_coin,
        )

    def get_coin_total(self, coin_list: list[int]) -> int:
        """
        Add up coin weights, checking for any invalid values or
        if we've hit upon the faulty coin which weighs 9 instead of 10
        """
        total = 0
        for entry in coin_list:
            if entry < 0 or entry >= self.game_size:
                # Invalid entry provided
                return -1
            elif entry == self.faulty_coin:
                total += 9
            else:
                total += 10
        return total


class TCPSocketHandler(socketserver.BaseRequestHandler):
    def read_line(self) -> bytes:
        """
        Read a line from the socket until we reach a newline
        """
        line = b""
        while True:
            part = self.request.recv(1)
            if part == b"":
                break
            elif part != b"\n":
                line += part
            elif part == b"\n":
                break
        return line

    @staticmethod
    def process_submission(submission: bytes) -> list[int] | None:
        try:
            index_list = [
                int(i) for i in submission.decode("utf-8").replace(" ", "").split(",")
            ]
            return index_list
        except Exception as e:
            logger.warning("Unable to process submission properly", exception=str(e))
            return None

    def run_game(self) -> None:
        game_size = random.randint(100, 1_000_000)
        self.game = CoinGame(uuid.uuid4().hex, game_size, random.randint(0, game_size))
        self.request.sendall(
            f"Starting the game, the game size is {game_size} and coins are zero-indexed\n".encode(
                "utf-8"
            )
        )

        max_guesses = math.floor(math.log2(game_size)) + 1
        self.request.sendall(
            f"You have a maximum of {max_guesses} guesses. Enter 'quit' to exit\n".encode(
                "utf-8"
            )
        )

        guess_count = 0
        while guess_count < max_guesses:
            self.request.sendall(
                b"Input your list of coins, or a single index for a guess: "
            )
            current_submission = self.read_line()
            if len(current_submission) == 0:
                logger.error("Closed", game_id=self.game.game_id)
                break
            elif current_submission == b"quit":
                logger.error("Quitting", game_id=self.game.game_id)
                break

            index_list = self.process_submission(current_submission)
            if index_list is None:
                # Invalid submission, try again
                logger.error(
                    "Unable to process submission", submission=current_submission
                )
                self.request.sendall(b"Invalid submission, try again\n")
                continue

            if len(index_list) == 1 and index_list[0] == self.game.faulty_coin:
                # Successful guess
                self.request.sendall(b"Success!\n")
                self.finish()
                logger.info("Game successfully finished", game_id=self.game.game_id)
                return

            submission_coin_total = self.game.get_coin_total(index_list)
            if submission_coin_total == -1:
                # Invalid submission, try again
                error_message = "Invalid coin values submitted, unable to process"
                logger.error(error_message, guess_count=guess_count)
                self.request.sendall(error_message.encode("utf-8") + b"\n")
                continue

            self.request.sendall(f"{submission_coin_total}\n".encode("utf-8"))
            guess_count += 1

        self.request.sendall(b"Failed!\n")
        self.finish()
        logger.info("Game ended in failure", game_id=self.game.game_id)
        return

    def handle(self):
        self.run_game()


def main() -> None:
    cli_args = cli.parse_args()
    logger.info("Binding to host and port", host=cli_args.host, port=cli_args.port)
    with socketserver.TCPServer(
        (cli_args.host, cli_args.port), TCPSocketHandler
    ) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
