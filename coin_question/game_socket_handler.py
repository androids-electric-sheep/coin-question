import random
import socketserver
import uuid

from . import game


class GameSocketHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        """
        Construct an instance of the game connected to this socket
        and run the game loop
        """
        game_id = uuid.uuid4().hex
        game_size = random.randint(100, 1_000_000)
        faulty_coin = random.randint(0, game_size)
        self.game = game.CoinGame(
            game_id=game_id,
            sock=self.request,
            game_size=game_size,
            faulty_coin=faulty_coin,
        )
        self.game.run()
        self.finish()
