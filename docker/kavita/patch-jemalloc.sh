#!/bin/bash
# ==============================================================================
# LinuxServer Kavita Startup Patch
# ==============================================================================
# Problem:
#   Upstream LSIO image searches root ('find / -name libjemalloc.so.2') to locate
#   jemalloc. When /data is mounted with large manga/book collections, 'find'
#   crawls every file, delaying container startup by 10+ minutes.
#
# Fix:
#   Restrict the search to '/usr' where the package manager installs libraries.
#   Runs once at container boot via /custom-cont-init.d before services launch.
# ==============================================================================

sed -i 's|find / |find /usr |g' /run/s6-rc/servicedirs/svc-kavita/run
