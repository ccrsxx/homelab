import os
import subprocess

from typing import Final

IGNORE_SERVICES_UPDATE: Final = ["nextcloud"]


def main() -> None:
    services = os.listdir("./src/docker")

    running_from_host = os.getenv("SSH_TTY") is None

    for service in services:
        if service == "update_container.py":
            continue

        service_path = os.path.join("src", "docker", service, "compose.yaml")

        allow_service_update = (
            service not in IGNORE_SERVICES_UPDATE and running_from_host
        )

        if allow_service_update:
            subprocess.call(["docker", "compose", "-f", service_path, "pull"])

        subprocess.call(["docker", "compose", "-f", service_path, "up", "-d"])


if __name__ == "__main__":
    main()
