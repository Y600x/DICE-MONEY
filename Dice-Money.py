import asyncio
import json
import os
from typing import Optional, Any

from telethon import TelegramClient
from telethon.tl import types
from telethon.errors import UserAlreadyParticipantError

config_file = "config.json"

class config_manager:
    def __init__(self, filename: str = config_file):
        self.filename = filename
        self.config = self.load()

    def load(self) -> dict:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return {}

    def save(self) -> None:
        with open(self.filename, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.save()

class telegram_automation:
    def __init__(self):
        self.config_manager = config_manager()
        self.client: Optional[TelegramClient] = None

    async def setup_client(self) -> None:
        api_id = self.config_manager.get("api_id")
        api_hash = self.config_manager.get("api_hash")

        if not api_id or not api_hash:
            print("Enter your API credentials from my.telegram.org")
            api_id = int(input("api_id :  "))
            api_hash = input("api_hash :  ")
            self.config_manager.set("api_id", api_id)
            self.config_manager.set("api_hash", api_hash)

        self.client = TelegramClient("user_session", api_id, api_hash)
        await self.client.start()
        print("Logged in successfully")

    async def join_required_channel(self, channel_username: str = "@FlashBytesTeam") -> None:
        try:
            await self.client.join_channel(channel_username)
            print(f"Successfully joined {channel_username}")
        except UserAlreadyParticipantError:
            print(f"Already a member of {channel_username}")
        except Exception as e:
            print(f"Failed to join {channel_username}: {e}")

    async def get_bot_entity(self):
        bot_username = input("Enter bot username or ID : ➛  ").strip()
        entity = await self.client.get_entity(bot_username)
        return entity

    async def send_start(self, bot_entity) -> None:
        await self.client.send_message(bot_entity, "/start")
        print("Sent /start")

    async def send_dice_loop(self, bot_entity, interval: int = 8) -> None:
        print(f"Starting to send dice every {interval} seconds... (press Ctrl+C to stop)")
        try:
            while True:
                await self.client.send_message(bot_entity, file=types.InputMediaDice(emoticon='🎲'))
                await asyncio.sleep(interval)
        except KeyboardInterrupt:
            print("Stopped sending dice")
        finally:
            await self.client.disconnect()

    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self) -> None:
        banner = """
=========================================
           DICE-MONEY
=========================================
FlashBytes Team - Telegram Channel: @FlashBytesTeam
GitHub: https://github.com/Y600x
=========================================
"""
        print(banner)

    async def run(self) -> None:
        self.clear_screen()
        self.print_banner()

        await self.setup_client()
        await self.join_required_channel()
        bot_entity = await self.get_bot_entity()
        await self.send_start(bot_entity)
        await self.send_dice_loop(bot_entity)

async def main():
    automation = telegram_automation()
    await automation.run()

if __name__ == "__main__":
    asyncio.run(main())
