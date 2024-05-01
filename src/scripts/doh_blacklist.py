from urllib.request import urlretrieve, urlcleanup

ADDRESS_LIST_NAME = "z_dns_ips_blacklist"

WHITELISTED_IPS = [
    "76.76.21.9",  # Vercel
    "185.199.109.153",  # GitHub
    "185.199.110.153",  # GitHub
    "76.76.21.21",  # Tailscale
]


def main() -> None:
    dns_ips_blacklist = (
        "https://raw.githubusercontent.com/jpgpi250/piholemanual/master/DOHipv4.txt"
    )

    temp_dns_ips_blacklist_file, _ = urlretrieve(dns_ips_blacklist)

    with open("add_dns_ips_blacklist.rsc", "w") as blacklist_script_file:
        blacklist_script_file.write(
            f"/ip firewall address-list remove [find list={ADDRESS_LIST_NAME}]\n"
        )

        with open(temp_dns_ips_blacklist_file, "r") as ip_addresses:
            for ip_address in ip_addresses:
                stripped_ip_address = ip_address.strip()

                if stripped_ip_address in WHITELISTED_IPS:
                    blacklist_script_file.write(
                        f'/ip firewall address-list add address={ip_address.strip()} list={ADDRESS_LIST_NAME} disabled=yes comment="Whitelisted IP"\n'
                    )
                    continue

                blacklist_script_file.write(
                    f"/ip firewall address-list add address={stripped_ip_address} list={ADDRESS_LIST_NAME}\n"
                )

    urlcleanup()


if __name__ == "__main__":
    main()
