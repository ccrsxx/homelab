#!/bin/sh

TARGET="/jellyfin/jellyfin-web/main.jellyfin.bundle.js"

if [ -f "$TARGET" ]; then
  echo "Patching $TARGET ..."
  sed -i 's/enableBackdrops:function(){return R}/enableBackdrops:function(){return E}/g' "$TARGET"
else
  echo "Warning: $TARGET not found, skipping patch"
fi

# Hand control back to Jellyfin
exec /jellyfin/jellyfin "$@"

