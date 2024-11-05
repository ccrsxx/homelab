import os
import utils.env
import subprocess

from typing import Final


def get_container_list() -> list[str]:
    raw_container_list: Final = os.getenv("CONTAINER_LIST")

    if not raw_container_list:
        raise ValueError("No container list provided")

    parsed_container_list: Final = [
        container.strip() for container in raw_container_list.split(",")
    ]

    if not parsed_container_list:
        raise ValueError("No containers to deploy")

    os.chdir("docker")

    valid_container_list: Final = []

    available_containers: Final = os.listdir()

    for container in parsed_container_list:
        if container in valid_container_list:
            raise ValueError(f"Container {container} is duplicated")

        if container not in available_containers:
            raise ValueError(f"Container {container} does not exist")

        valid_container_list.append(container)

    if not valid_container_list:
        raise ValueError("No valid containers to deploy")

    return valid_container_list


def create_traefik_network() -> None:
    traefik_network_exists = (
        subprocess.call(
            ["docker", "network", "inspect", "traefik"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        == 0
    )

    if traefik_network_exists:
        return

    subprocess.call(["docker", "network", "create", "traefik"])


def deploy_containers(container_list: list[str]) -> None:
    create_traefik_network()

    for container in container_list:
        service_path = os.path.join(container, "compose.yaml")

        subprocess.call(["docker", "compose", "-f", service_path, "pull"])
        subprocess.call(["docker", "compose", "-f", service_path, "up", "-d"])


def main() -> None:
    container_list: Final = get_container_list()

    deploy_containers(container_list)


if __name__ == "__main__":
    main()
