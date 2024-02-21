import sys
from loguru import logger

from models.Client import Client
from utils import file_reader

import asyncio


def init():
    clients = []

    logger.remove()
    logger.add(sys.stdout, colorize=True, format="<light-cyan>{time:HH:mm:ss}</light-cyan> | <level> {level: "
                                                 "<8}</level> | <white>{""message}</white>")

    discord_tokens: list = file_reader.read_txt_file("discord_tokens", "data/discord_tokens.txt")
    proxies = file_reader.read_txt_file("proxies", "data/proxies.txt")

    if len(proxies) > len(discord_tokens):
        for discord_token_id in range(len(discord_tokens)):
            clients.append(Client(discord_token_id, proxies[discord_token_id], discord_tokens[discord_token_id]))
    else:
        for proxy_id in range(len(proxies)):
            clients.append(Client(proxy_id, proxies[proxy_id], discord_tokens[proxy_id]))
    return clients


async def main():
    clients = init()
    tasks = [client.press_button_by_time() for client in clients]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
