import sys
from typing import Final, Literal, cast

from utils.homelab import disable_slskd, enable_slskd, play_sound
from utils.notification import send_discord, send_pushover
from utils.qbittorrent import disable_qbittorrents, enable_qbittorrents
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
    play_sound('internet-up.wav')

    remove_failover_notice()

    enable_qbittorrents()
    enable_slskd()

    up_event_message = 'Iconnet is up. Primary WAN connection is up. Failover is over.'

    send_pushover(up_event_message)
    send_discord(up_event_message)


def trigger_down_event() -> None:
    play_sound('internet-down.wav')

    add_failover_notice()

    disable_qbittorrents()
    disable_slskd()

    down_event_message = (
        'Iconnet is down. Primary WAN connection is down. Using XL as a Failover now.'
    )

    send_pushover(down_event_message)
    send_discord(down_event_message)


def main() -> None:
    event: Final = get_event()

    if event == 'up':
        trigger_up_event()
    else:
        trigger_down_event()


if __name__ == '__main__':
    main()
