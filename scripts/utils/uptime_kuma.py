from typing import Final

from uptime_kuma_api import UptimeKumaApi

from .env import app_env

UPTIME_KUMA_API: Final = UptimeKumaApi(app_env.UPTIME_KUMA_URL)


UPTIME_KUMA_API.login(app_env.UPTIME_KUMA_USERNAME, app_env.UPTIME_KUMA_PASSWORD)


def add_failover_notice() -> None:
    UPTIME_KUMA_API.resume_maintenance(app_env.UPTIME_KUMA_MAINTENANCE_ID)


def remove_failover_notice() -> None:
    UPTIME_KUMA_API.pause_maintenance(app_env.UPTIME_KUMA_MAINTENANCE_ID)
