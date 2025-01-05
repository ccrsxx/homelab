import os
import utils.env
import subprocess

from typing import Final

PC_USERNAME: Final = os.getenv("PC_USERNAME")
PC_PASSWORD: Final = os.getenv("PC_PASSWORD")
PC_IP_ADDRESS: Final = os.getenv("PC_IP_ADDRESS")


def main() -> None:
    subprocess.run(["shutdown", "/s", "/f", "/t", "60", "/c", "From UPS"])

    # Turn off PC if regardless if it's on or off
    subprocess.run(
        ["net", "use", f"\\\{PC_IP_ADDRESS}\\IPC$", PC_PASSWORD, f"/USER:{PC_USERNAME}"]
    )

    subprocess.run(
        ["shutdown", "/s", "/f", "/m", PC_IP_ADDRESS, "/t", "60", "/c", "From UPS"]
    )


if __name__ == "__main__":
    main()
