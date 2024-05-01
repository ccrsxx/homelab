import sys
import subprocess

from typing import Final, Literal
from utils.mail import send_email


def get_event() -> Literal["up", "down"]:
    args: Final = sys.argv

    if len(args) < 2:
        raise ValueError("No event provided")

    event: Final = args[1]

    if event not in ("up", "down"):
        raise ValueError("Invalid event provided")

    return event


def main() -> None:
    event: Final = get_event()

    if event == "up":
        subprocess.run(["qbt", "torrent", "resume", "all"])
        send_email("Iconnet is up", "Primary WAN connection is up. Failover is over.")
    else:
        subprocess.run(["qbt", "torrent", "pause", "all"])
        send_email(
            "Iconnet is down",
            "Primary WAN connection is down. Using XL as a Failover now.",
        )


if __name__ == "__main__":
    main()
