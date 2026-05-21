#!/bin/bash
# Patch out the "Upgrade to UniFi OS Server" nag modal
# Mount as:
#   -v ./unifi-patch-upgrade-nag.sh:/custom-cont-init.d/unifi-patch-upgrade-nag.sh

set -eu

SWAI_FILE=$(find /usr/lib/unifi/webapps/ROOT/app-unifi/react/js/ -name 'swai.*.js' 2>/dev/null | head -1)

if [ -z "${SWAI_FILE:-}" ]; then
    echo "[patch] swai.js not found, skipping upgrade nag patch"
    exit 0
fi

# Already patched?
if grep -q 'return !1&&r?' "$SWAI_FILE"; then
    echo "[patch] Already patched"
    exit 0
fi

# Replace:
#   return n&&r?<any>.createElement(<any>.aF.Root
# with:
#   return !1&&r?<same>.createElement(<same>.aF.Root
#
# This avoids depending on minified symbol names like e/t and Ne/fe/he.
if sed -E -i \
    's/return n&&r\?([A-Za-z_$][A-Za-z0-9_$]*)\.createElement\(([A-Za-z_$][A-Za-z0-9_$]*)\.aF\.Root/return !1\&\&r?\1.createElement(\2.aF.Root/' \
    "$SWAI_FILE"; then

    if grep -q 'return !1&&r?' "$SWAI_FILE"; then
        echo "[patch] Upgrade to UniFi OS Server nag removed"
    else
        echo "[patch] Pattern not found, UniFi bundle changed"
        exit 1
    fi
else
    echo "[patch] sed failed"
    exit 1
fi
