import os
import sys
import subprocess

from typing import Final, Literal
from utils.mail import send_email

from uptime_kuma_api import UptimeKumaApi


UPTIME_KUMA_API: Final = UptimeKumaApi(os.getenv("UPTIME_KUMA_URL"))

UPTIME_KUMA_API.login(
    os.getenv("UPTIME_KUMA_USERNAME"), os.getenv("UPTIME_KUMA_PASSWORD")
)

UPTIME_KUMA_MAINTENANCE_ID: Final = os.getenv("UPTIME_KUMA_MAINTENANCE_ID")


def get_event() -> Literal["up", "down"]:
    args: Final = sys.argv

    if len(args) < 2:
        raise ValueError("No event provided")

    event: Final = args[1]

    if event not in ("up", "down"):
        raise ValueError("Invalid event provided")

    return event


def trigger_up_event() -> None:
    subprocess.run(["qbt", "torrent", "resume", "all"])

    UPTIME_KUMA_API.pause_maintenance(UPTIME_KUMA_MAINTENANCE_ID)

    send_email("Iconnet is up", "Primary WAN connection is up. Failover is over.")


def trigger_down_event() -> None:
    subprocess.run(["qbt", "torrent", "pause", "all"])

    UPTIME_KUMA_API.resume_maintenance(UPTIME_KUMA_MAINTENANCE_ID)

    send_email(
        "Iconnet is down",
        "Primary WAN connection is down. Using XL as a Failover now.",
    )


def main() -> None:
    event: Final = get_event()

    if event == "up":
        trigger_up_event()
    else:
        trigger_down_event()


if __name__ == "__main__":
    main()
