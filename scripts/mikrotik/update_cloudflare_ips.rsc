# Set the file name
:local cloudflareIpsFileName "cloudflare_ips"

# Download the DNS IP blacklist file
/tool fetch url="https://cloudflare.com/ips-v4" \
  mode=https dst-path=$cloudflareIpsFileName

# Read the cloudflare IPs file
:local cloudflareIpsFile [/file get $cloudflareIpsFileName contents]
:local cloudflareIpsFileLength [:len $cloudflareIpsFile]

# Variable for parsing the file
:local line ""
:local lineEnd 0
:local lastEnd 0

:while ($lineEnd < $cloudflareIpsFileLength) do={
  # Depending on file type (linux/windows), "\n" might need to be "\r\n"
  :set lineEnd [:find $cloudflareIpsFile "\n" $lastEnd]

  # If there are no more line breaks, set this to be the last one
  :if ([:len $lineEnd] = 0) do={
    :set lineEnd $cloudflareIpsFileLength
  }

  # Get the current line based on the last line break and next one
  :set line [:pick $cloudflareIpsFile $lastEnd $lineEnd]

  # Depending on "\n" or "\r\n", this will be 1 or 2 accordingly
  :set lastEnd ($lineEnd + 1)

  # Don't process blank lines and empty lines
  :if ($line != "\r" && [:typeof $line] != "nil") do={
    /ip firewall address-list add address=$line list=$cloudflareIpsFileName comment="Cloudflare IP"
  }
} 

# Clean up
/file remove $cloudflareIpsFileName
