import os

from typing import Final
from uptime_kuma_api import UptimeKumaApi

UPTIME_KUMA_API: Final = UptimeKumaApi(os.getenv("UPTIME_KUMA_URL"))
UPTIME_KUMA_MAINTENANCE_ID: Final = os.getenv("UPTIME_KUMA_MAINTENANCE_ID")

UPTIME_KUMA_API.login(
    os.getenv("UPTIME_KUMA_USERNAME"), os.getenv("UPTIME_KUMA_PASSWORD")
)


def add_failover_notice() -> None:
    UPTIME_KUMA_API.resume_maintenance(UPTIME_KUMA_MAINTENANCE_ID)


def remove_failover_notice() -> None:
    UPTIME_KUMA_API.pause_maintenance(UPTIME_KUMA_MAINTENANCE_ID)
