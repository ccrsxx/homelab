import subprocess

from utils.env import app_env


def main() -> None:
    # Turn off Homelab
    subprocess.run(['ssh', 'proxmox'])

    # Turn off PC if regardless if it's on or off
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
