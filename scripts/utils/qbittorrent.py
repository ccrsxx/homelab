from typing import Final

import qbittorrentapi

from .env import app_env

qbt_client_proxmox: Final = qbittorrentapi.Client(
    host=app_env.QBITTORRENT_PROXMOX_HOST,
    port=app_env.QBITTORRENT_PORT,
    username=app_env.QBITTORRENT_USERNAME,
    password=app_env.QBITTORRENT_PASSWORD,
)

qbt_client_proxmox.auth_log_in()

qbt_client_ubuntu: Final = qbittorrentapi.Client(
    host=app_env.QBITTORRENT_UBUNTU_HOST,
    port=app_env.QBITTORRENT_PORT,
    username=app_env.QBITTORRENT_USERNAME,
    password=app_env.QBITTORRENT_PASSWORD,
)

qbt_client_ubuntu.auth_log_in()


def enable_qbittorrents() -> None:
    qbt_client_proxmox.app.setPreferences({'max_active_torrents': 512})
    qbt_client_ubuntu.app.setPreferences({'max_active_torrents': 512})


def disable_qbittorrents() -> None:
    qbt_client_proxmox.app.setPreferences({'max_active_torrents': 0})
    qbt_client_ubuntu.app.setPreferences({'max_active_torrents': 0})
