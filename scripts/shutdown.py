import subprocess

from utils.env import app_env


def main() -> None:
    subprocess.run(['shutdown', '/s', '/f', '/t', '60', '/c', 'From UPS'])

    # Turn off PC if regardless if it's on or off
    subprocess.run(
        [
            'net',
            'use',
            f'\\\{app_env.PC_IP_ADDRESS}\\IPC$',
            app_env.PC_PASSWORD,
            f'/USER:{app_env.PC_USERNAME}',
        ]
    )

    subprocess.run(
        [
            'shutdown',
            '/s',
            '/f',
            '/m',
            app_env.PC_IP_ADDRESS,
            '/t',
            '60',
            '/c',
            'From UPS',
        ]
    )


if __name__ == '__main__':
    main()
