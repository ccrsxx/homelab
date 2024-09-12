import os
import qbittorrentapi

from typing import Final

conn_info: Final = {
    "host": os.getenv("QBITTORRENT_HOST"),
    "port": os.getenv("QBITTORRENT_PORT"),
    "username": os.getenv("QBITTORRENT_USERNAME"),
    "password": os.getenv("QBITTORRENT_PASSWORD"),
}


qbt_client: Final = qbittorrentapi.Client(**conn_info)

try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print("Failed to log in qBittorrent", e)


def enable_torrents() -> None:
    qbt_client.app.setPreferences({"max_active_torrents": 20})


def disable_torrents() -> None:
    qbt_client.app.setPreferences({"max_active_torrents": 0})
