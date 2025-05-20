import json
from typing import TypedDict
from urllib.parse import urljoin

import js2py
from bs4 import BeautifulSoup
from bs4.element import Tag

from .env import app_env
from .router_client import Client
from .router_utils import WanType, get_wan_list

client = Client()


@client.is_authenticated
def get_hardware_token_on_wan_page() -> str:
    url = urljoin(app_env.ROUTER_URL, '/html/bbsp/wan/wan.asp')

    res = client.session.get(url)

    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')

    hidden_token_element = soup.find('input', {'id': 'hwonttoken'})

    if not isinstance(hidden_token_element, Tag):
        raise ValueError('Cannot find the hwonttoken input element.')

    hw_token = hidden_token_element.get('value')

    if not hw_token or not isinstance(hw_token, str):
        raise ValueError('hwtoken is invalid or not found')

    return hw_token


@client.is_authenticated
def change_device_to_bridge_mode() -> None:
    print('Changing router to bridge mode...')

    wan_type = get_device_wan_type()

    if wan_type == 'PPPoE_Bridged':
        print('Router is already in bridge mode.')
        return

    url = urljoin(
        app_env.ROUTER_URL,
        '/html/bbsp/wan/complex.cgi?y=InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1&RequestFile=html/bbsp/wan/confirmwancfginfo.html',
    )

    hw_token = get_hardware_token_on_wan_page()

    params = {
        'y.Enable': '1',
        'y.X_HW_IPv4Enable': '1',
        'y.X_HW_IPv6Enable': '0',
        'y.X_HW_IPv6MultiCastVLAN': '-1',
        'y.X_HW_SERVICELIST': 'INTERNET',
        'y.X_HW_ExServiceList': '',
        'y.X_HW_VLAN': '2908',
        'y.X_HW_PRI': '0',
        'y.X_HW_PriPolicy': 'Specified',
        'y.X_HW_DefaultPri': '0',
        'y.ConnectionType': 'PPPoE_Bridged',
        'y.X_HW_MultiCastVLAN': '4294967295',
        'y.X_HW_BindPhyPortInfo': 'Lan1,SSID1',
        'X_HW_OverrideAllowed': '0',
        'x.X_HW_Token': hw_token,
    }

    res = client.session.post(url, data=params)

    res.raise_for_status()

    print('Successfully changed router to bridge mode.')


class DeviceStatus(TypedDict):
    cpu_usage: str
    ont_status: str
    system_time: str
    memory_usage: str


@client.is_authenticated
def get_device_status() -> DeviceStatus:
    url = urljoin(app_env.ROUTER_URL, '/html/ssmp/deviceinfo/deviceinfo.asp')

    res = client.session.get(url)

    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')
    script = soup.find('script', text=True)

    if not script:
        raise ValueError('Cannot find the script in the page.')

    script_content = script.text

    context = js2py.EvalJs()
    context.execute(script_content)

    device_status: DeviceStatus = {
        'cpu_usage': context.cpuUsed,
        'ont_status': context.ontInfo.Status,
        'system_time': context.systemdsttime,
        'memory_usage': context.memUsed,
    }

    print('Router stats:', json.dumps(device_status, indent=2))

    return device_status


@client.is_authenticated
def get_device_wan_type() -> WanType:
    url = urljoin(app_env.ROUTER_URL, '/html/bbsp/common/getwanlist.asp')

    res = client.session.get(url)

    res.raise_for_status()

    script_content = res.text

    wan_list = get_wan_list(script_content)

    if not wan_list:
        raise ValueError('No WAN list found')

    wan_type = wan_list[0]['type']

    print('Device WAN Type:', wan_type)

    return wan_type
