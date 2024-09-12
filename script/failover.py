import sys

from typing import Final, Literal
from utils.mail import send_email

from utils.qbittorrent import enable_torrents, disable_torrents
from utils.uptime_kuma import add_failover_notice, remove_failover_notice


def get_event() -> Literal["up", "down"]:
    args: Final = sys.argv

    if len(args) < 2:
        raise ValueError("No event provided")

    event: Final = args[1]

    if event not in ("up", "down"):
        raise ValueError("Invalid event provided")

    return event


def trigger_up_event() -> None:
    remove_failover_notice()
    enable_torrents()

    send_email("Iconnet is up", "Primary WAN connection is up. Failover is over.")


def trigger_down_event() -> None:
    add_failover_notice()
    disable_torrents()

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
