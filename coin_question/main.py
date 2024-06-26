import socketserver

import structlog

from . import cli, game_socket_handler

logger = structlog.get_logger()


def main() -> None:
    """
    Main entrypoint
    """
    cli_args = cli.parse_args()
    logger.info("Binding to host and port", host=cli_args.host, port=cli_args.port)

    socket_handler = game_socket_handler.generate_game_socket_handler(
        cli_args.game_size, cli_args.faulty_coin
    )
    with socketserver.TCPServer(
        (cli_args.host, cli_args.port), socket_handler
    ) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
