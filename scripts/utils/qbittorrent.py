from typing import Final

import qbittorrentapi

from .env import app_env

qbt_client: Final = qbittorrentapi.Client(
    host=app_env.QBITTORRENT_HOST,
    port=app_env.QBITTORRENT_PORT,
    username=app_env.QBITTORRENT_USERNAME,
    password=app_env.QBITTORRENT_PASSWORD,
)

qbt_client.auth_log_in()


def enable_torrents() -> None:
    qbt_client.app.setPreferences({'max_active_torrents': 20})


def disable_torrents() -> None:
    qbt_client.app.setPreferences({'max_active_torrents': 0})
