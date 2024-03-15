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
    with socketserver.TCPServer(
        (cli_args.host, cli_args.port), game_socket_handler.GameSocketHandler
    ) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
