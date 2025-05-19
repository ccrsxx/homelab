import sys
from typing import Final, Literal, cast

from utils.mail import send_email
from utils.qbittorrent import disable_torrents, enable_torrents
from utils.router import change_device_to_bridge_mode, login
from utils.uptime_kuma import add_failover_notice, remove_failover_notice

VALID_EVENT = Literal['up', 'down']


def get_event() -> VALID_EVENT:
    args: Final = sys.argv

    if len(args) < 2:
        raise ValueError('No event provided')

    event: Final = args[1]

    if event not in ('up', 'down'):
        raise ValueError('Invalid event provided')

    return cast(VALID_EVENT, event)


def trigger_up_event() -> None:
    login()
    change_device_to_bridge_mode()

    remove_failover_notice()
    enable_torrents()

    send_email(
        'Iconnet is up',
        'Primary WAN connection is up. Failover is over.',
    )


def trigger_down_event() -> None:
    add_failover_notice()
    disable_torrents()

    send_email(
        'Iconnet is down',
        'Primary WAN connection is down. Using XL as a Failover now.',
    )


def main() -> None:
    event: Final = get_event()

    if event == 'up':
        trigger_up_event()
    else:
        trigger_down_event()


if __name__ == '__main__':
    main()
