import os
from typing import Final

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, Field

load_dotenv(find_dotenv())


class AppEnv(BaseModel):
    CONTAINER_LIST: str = Field(description='List of containers to deploy')

    EMAIL_API: str = Field(description='Email API')
    EMAIL_API_KEY: str = Field(description='Gmail API key')
    TARGET_EMAIL_SENDER: str = Field(description='Email recipient')

    DISCORD_WEBHOOK_ID: str = Field(description='Discord webhook ID')
    DISCORD_WEBHOOK_TOKEN: str = Field(description='Discord webhook token')

    PUSHOVER_USER: str = Field(description='Pushover user key')
    PUSHOVER_TOKEN: str = Field(description='Pushover app token')

    ROUTER_URL: str = Field(description='Router URL')
    ROUTER_USERNAME: str = Field(description='Router username')
    ROUTER_PASSWORD: str = Field(description='Router password')

    PC_USERNAME: str = Field(description='PC username')
    PC_PASSWORD: str = Field(description='PC password')
    PC_IP_ADDRESS: str = Field(description='PC IP address')

    UPTIME_KUMA_URL: str = Field(description='Uptime Kuma URL')
    UPTIME_KUMA_USERNAME: str = Field(description='Uptime Kuma username')
    UPTIME_KUMA_PASSWORD: str = Field(description='Uptime Kuma password')
    UPTIME_KUMA_MAINTENANCE_ID: str = Field(description='Uptime Kuma maintenance ID')

    QBITTORRENT_PROXMOX_HOST: str = Field(description='qBittorrent Proxmox host')
    QBITTORRENT_UBUNTU_HOST: str = Field(description='qBittorrent Ubuntu host')

    QBITTORRENT_PORT: str = Field(description='qBittorrent port')
    QBITTORRENT_USERNAME: str = Field(description='qBittorrent username')
    QBITTORRENT_PASSWORD: str = Field(description='qBittorrent password')


app_env: Final = AppEnv(**os.environ)
