import socketserver

from . import game


def generate_game_socket_handler(
    game_id: str, game_size: int, faulty_coin: int
) -> type[socketserver.BaseRequestHandler]:
    class GameSocketHandler(socketserver.BaseRequestHandler):
        def handle(self) -> None:
            """
            Construct an instance of the game connected to this socket
            and run the game loop
            """
            self.game = game.CoinGame(
                game_id=game_id,
                sock=self.request,
                game_size=game_size,
                faulty_coin=faulty_coin,
            )
            self.game.run()
            self.finish()

    return GameSocketHandler
