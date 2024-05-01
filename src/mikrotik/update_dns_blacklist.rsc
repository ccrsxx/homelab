# Set the address list name
:local blackListName "z_dns_ips_blacklist"

# Set the whitelisted IPs
# GitHub, Vercel, Tailscale in ascending order
:local whiteListIPs [:toarray \
  " \
    185.199.108.153, \
    185.199.109.153, \
    185.199.110.153, \
    185.199.111.153, \
    76.76.21.9, \
    76.76.21.21, \
  " \
]

# Download the DNS IP blacklist file
/tool fetch url="https://raw.githubusercontent.com/jpgpi250/piholemanual/master/DOHipv4.txt" \
  mode=https dst-path=$blackListName

# Read the blacklist file
:local blacklistFile [/file get $blackListName contents]
:local blacklistFileLength [:len $blacklistFile]

# Remove the old address list
/ip firewall address-list remove [find list=$blackListName]

# Variable for parsing the file
:local line ""
:local lineEnd 0
:local lastEnd 0

:while ($lineEnd < $blacklistFileLength) do={
  # Depending on file type (linux/windows), "\n" might need to be "\r\n"
  :set lineEnd [:find $blacklistFile "\n" $lastEnd]

  # If there are no more line breaks, set this to be the last one
  :if ([:len $lineEnd] = 0) do={
    :set lineEnd $blacklistFileLength
  }

  # Get the current line based on the last line break and next one
  :set line [:pick $blacklistFile $lastEnd $lineEnd]

  # Depending on "\n" or "\r\n", this will be 1 or 2 accordingly
  :set lastEnd ($lineEnd + 1)

  # Don't process blank lines and empty lines
  :if ($line != "\r" && [:typeof $line] != "nil") do={
    :local whiteListedIp [:find $whiteListIPs $line]

    if ([:typeof $whiteListedIp] = "nil") do={
      /ip firewall address-list add address=$line list=$blackListName comment="Blacklisted DNS IP"
    }

    if ([:typeof $whiteListedIp] = "num") do={
      /ip firewall address-list add address=$line list=$blackListName disabled=yes comment="Whitelisted DNS IP"
    }
  }
} 

# Clean up
/file remove $blackListName
