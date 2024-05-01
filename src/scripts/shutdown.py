import os
import utils.env
import subprocess

from typing import Final

PC_USERNAME: Final = os.getenv("PC_USERNAME")
PC_PASSWORD: Final = os.getenv("PC_PASSWORD")


def main() -> None:
    subprocess.run(["shutdown", "/s", "/t", "60", "/c", "From UPS"])

    # Turn off PC if regardless if it's on or off
    subprocess.run(["net", "use", "\\\PC\\IPC$", PC_PASSWORD, f"/USER:{PC_USERNAME}"])
    subprocess.run(["shutdown", "/s", "/m", "pc", "/t", "60", "/c", "From UPS"])


if __name__ == "__main__":
    main()
