import os
import sys
import subprocess

from typing import Final

IGNORE_SERVICES_UPDATE: Final = ["nextcloud"]


def main() -> None:
    current_file_dir_path = os.path.dirname(sys.argv[0])

    services = os.listdir(current_file_dir_path)

    running_from_host = os.getenv("SSH_TTY") is None

    for service in services:
        if service == "update_container.py":
            continue

        service_path = os.path.join(current_file_dir_path, service, "compose.yaml")

        allow_service_update = (
            service not in IGNORE_SERVICES_UPDATE and running_from_host
        )

        if allow_service_update:
            subprocess.call(["docker", "compose", "-f", service_path, "pull"])

        subprocess.call(["docker", "compose", "-f", service_path, "up", "-d"])


if __name__ == "__main__":
    main()
