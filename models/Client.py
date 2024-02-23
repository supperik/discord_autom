import asyncio
from datetime import datetime, timedelta
import random

from curl_cffi import requests
import utils
from loguru import logger


class Client:
    def __init__(self, account_index: int, proxy: str, discord_token: str):
        self.channel_id: str | None = None
        self.message_id: str | None = None
        self.guild_id: str | None = None

        self.account_index = account_index
        self.discord_token = discord_token
        self.proxy = proxy
        self.flag = False

        self.time_format = '%d %m %y %H:%M:%S'
        self.day = datetime.strftime(datetime.now(), '%d %m %y')

        self.button_press_time = datetime.strptime(f"{self.day} 15:40:20", self.time_format) #datetime.strptime(f"{self.day} {utils.generate_rofls.generate_random_time(account_index)}", self.time_format)

        self.user_agent: str = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/110.0.0.0 Safari/537.36")
        self.response: requests.Response | None = None

        self.client = self.create_client()
        self.init_cf()

    def init_cf(self) -> bool:
        try:
            self.response = self.client.get("https://discord.com/login",
                                            headers={
                                                'authority': 'discord.com',
                                                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                                                          'image/avif,image/webp,image/apng,*/*;q=0.8,'
                                                          'application/signed-exchange;v=b3;q=0.7',
                                                'accept-language': 'en-US,en;q=0.9',
                                                'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google '
                                                             'Chrome";v="110"',
                                                'sec-ch-ua-mobile': '?0',
                                                'sec-ch-ua-platform': '"Windows"',
                                                'sec-fetch-dest': 'document',
                                                'sec-fetch-mode': 'navigate',
                                                'sec-fetch-site': 'none',
                                                'sec-fetch-user': '?1',
                                                'upgrade-insecure-requests': '1',
                                                'user-agent': self.user_agent,
                                            }
                                            )
            if self.set_response_cookies():
                logger.success(f"{self.account_index} | Initialized new cookies.")
                return True
            else:
                logger.error(f"{self.account_index} | Failed to initialize new cookies.")
                return False
        except Exception as err:
            logger.error(f"{self.account_index} | Failed to initialize new cookies: {err}")
            return False

    def set_response_cookies(self) -> bool:
        try:
            cookies = self.response.headers.get_list("set-cookie")
            for cookie in cookies:
                try:
                    key, value = cookie.split(';')[0].strip().split("=")
                    self.client.cookies.set(name=key, value=value, domain="discord.com", path="/")
                except Exception as err:
                    logger.error(f"Failed to set response cookies: {err}")
            return True

        except Exception as err:
            logger.error(f"Failed to set response cookies: {err}")
            return False

    def create_client(self) -> requests.Session:
        session = requests.Session(impersonate="chrome110", timeout=60)
        if self.proxy:
            session.proxies.update({
                "http": "http://" + self.proxy,
                "https": "http://" + self.proxy,
            })
        session.headers.update({
            "authorization": self.discord_token,
            "x-super-properties": utils.create_super_properties.create_x_super_properties(self.user_agent)
        })
        return session

    async def press_button_by_time(self):
        while True:
            current_time = datetime.strptime(datetime.now().strftime(self.time_format), self.time_format)
            if (current_time >= self.button_press_time) and (not self.flag):
                await self.press_button()
            if (datetime.now().day == self.button_press_time.day + 1) and self.flag:
                self.button_press_time = self.button_press_time + timedelta(days=1)
                self.flag = False
            await asyncio.sleep(random.randint(5, 10)+self.account_index)

    async def press_button(self) -> bool:
        message_link = 'https://discord.com/channels/848599369879388170/1093212373793378335/1170416762588774522'.strip()
        self.guild_id = message_link.split("/")[-3]
        self.channel_id = message_link.split("/")[-2]
        self.message_id = message_link.split("/")[-1]

        self.flag = True
        self.button_press_time = datetime.strptime(f"{self.day} {utils.generate_rofls.generate_random_time(self.account_index)}", self.time_format)

        button_data, application_id, ok = self.message_click_button_info()

        try:
            resp = self.client.post("https://discord.com/api/v9/interactions",
                                    headers={
                                        'authority': 'discord.com',
                                        'accept': '*/*',
                                        'content-type': 'application/json',
                                        'origin': 'https://discord.com',
                                        'referer': f'https://discord.com/channels/{self.guild_id}/{self.channel_id}',
                                        'sec-ch-ua-mobile': '?0',
                                        'sec-ch-ua-platform': '"Windows"',
                                        'sec-fetch-dest': 'empty',
                                        'sec-fetch-mode': 'cors',
                                        'sec-fetch-site': 'same-origin',
                                        'x-debug-options': 'bugReporterEnabled',
                                        'x-discord-locale': 'en-US',
                                    },
                                    json={
                                        'type': 3,
                                        'nonce': utils.create_nonce.calculate_nonce(),
                                        'guild_id': self.guild_id,
                                        'channel_id': self.channel_id,
                                        'message_flags': 0,
                                        'message_id': self.message_id,
                                        'application_id': application_id,
                                        'session_id': utils.generate_rofls.generate_random_session_id(),
                                        'data': {
                                            'component_type': button_data['type'],
                                            'custom_id': button_data['custom_id'],
                                        },
                                    }
                                    )

            if resp.status_code == 204:
                logger.success(f"{self.account_index} | Successfully pressed the button.")
                return True
            else:
                raise Exception("Unknown error")



        except Exception as err:
            logger.error(f"{self.account_index} | Failed to press a button: {err}")
            return False


    def message_click_button_info(self) -> tuple[dict, str, bool]:
        try:
            resp = requests.get(
                "https://discord.com/api/v9/channels/" + self.channel_id + "/messages?limit=1&around=" + self.message_id,
                headers={"Authorization": self.discord_token})

            if '"custom_id":"enter-giveaway"' in resp.text:
                return resp.json()[0]['components'][0]['components'][0], resp.json()[0]['author']['id'], True

            result, ok = self.choose_button_to_click(resp.json()[0]['components'])

            return result, resp.json()[0]['author']['id'], ok

        except Exception as err:
            logger.error(f'Failed to get message info: {err}')
            return {}, "", False

    @staticmethod
    def choose_button_to_click(components: list) -> tuple[dict, bool]:
        try:
            def collect_components(element):
                parsed_components = []
                if isinstance(element, dict):
                    if element.get("type") == 2:
                        parsed_components.append(element)
                    for key, value in element.items():
                        parsed_components.extend(collect_components(value))
                elif isinstance(element, list):
                    for item in element:
                        parsed_components.extend(collect_components(item))

                return parsed_components

            all_components = collect_components(components)

            buttons = []
            for index, comp in enumerate(all_components, start=1):
                buttons.append(comp['label'])

            button = ['Daily Drop -February 20']

            for index, comp in enumerate(all_components, start=1):
                if comp['label'] == button[0]:
                    return comp, True

        except Exception as err:
            logger.error(f"Failed to choose button to click: {err}")
            return {}, False
