import re
from datetime import datetime, timezone
from typing import Literal, TypedDict

WanType = Literal['IP_Routed', 'PPPoE_Bridged']


class WanStatus(TypedDict):
    type: WanType
    status: str
    uptime: str
    mac_address: str
    service_list: str
    connection_status: str


def decode_unicode_escape(s: str) -> str:
    return bytes(s, 'utf-8').decode('unicode_escape')


def get_wan_list(js_data: str) -> list[WanStatus]:
    raw_wan_list = re.findall(r'new WanPPP\((.*?)\)', js_data, re.DOTALL)

    parsed_wan_list: list[WanStatus] = []

    for match in raw_wan_list:
        fields = re.findall(r'"(.*?)"|([^,]+)', match)
        fields = [decode_unicode_escape(f[0] or f[1]).strip() for f in fields]

        if not fields or fields[0] == '':
            continue

        wan: WanStatus = {
            'type': fields[12],
            'status': fields[11],
            'uptime': fields[39],
            'mac_address': fields[18],
            'service_list': fields[26],
            'connection_status': fields[4],
        }

        parsed_wan_list.append(wan)

    return parsed_wan_list


def parse_local_date_to_iso_date(local_date_str: str) -> str:
    local_dt = datetime.fromisoformat(local_date_str)

    utc_dt = local_dt.astimezone(timezone.utc)

    parsed_dt = utc_dt.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

    return parsed_dt
