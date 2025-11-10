#!/bin/bash
# ============================================================
# hardlink-to-shoko.sh
# ------------------------------------------------------------
# Create hardlinks for completed torrents (category: anime-hentai)
# from qBittorrent's downloads directory into Shoko's Source folder.
#
# - Keeps originals for seeding
# - Preserves directory structure under the download root
# - Lets Shoko later move/rename however it wants
# ============================================================

# qBittorrent parameters (from the "Run external program" command)
TORRENT_NAME="$1"          # %N - Torrent name
TORRENT_CATEGORY="$2"      # %L - Category
TORRENT_TAGS="$3"          # %G - Tags (comma-separated)
TORRENT_CONTENT_PATH="$4"  # %F - Content path (root of torrent)
TORRENT_ROOT_PATH="$5"     # %R - First subdir in torrent
TORRENT_SAVE_PATH="$6"     # %D - Save path (download root)
TORRENT_NUM_FILES="$7"     # %C - Number of files
TORRENT_SIZE="$8"          # %Z - Size in bytes
TORRENT_TRACKER="$9"       # %T - Tracker

# Shoko Source folder (inside the container)
# This should be the folder you configured in Shoko as an Import Folder with Drop Type = Source
SHOKO_SOURCE="/data/torrents/anime-hentai/source"

# Log file for debugging
LOG_FILE="/scripts/hardlink-debug.log"

# Timestamp helper
ts() {
  date '+%Y-%m-%d %H:%M:%S'
}

echo "[$(ts)] Start Torrent: '$TORRENT_NAME' (Category: $TORRENT_CATEGORY)" >> "$LOG_FILE"
echo "[$(ts)] Content path: $TORRENT_CONTENT_PATH" >> "$LOG_FILE"
echo "[$(ts)] Save path:    $TORRENT_SAVE_PATH" >> "$LOG_FILE"

# Only process hentai category
if [[ "$TORRENT_CATEGORY" != "anime-hentai" ]]; then
  echo "[$(ts)] Skipped (category not 'anime-hentai')" >> "$LOG_FILE"
  exit 0
fi

# Ensure target exists
mkdir -p "$SHOKO_SOURCE"

# Validate paths
if [[ -z "$TORRENT_CONTENT_PATH" || ! -e "$TORRENT_CONTENT_PATH" ]]; then
  echo "[$(ts)] ERROR: Content path does not exist or empty: '$TORRENT_CONTENT_PATH'" >> "$LOG_FILE"
  exit 1
fi

if [[ -z "$TORRENT_SAVE_PATH" || ! -d "$TORRENT_SAVE_PATH" ]]; then
  echo "[$(ts)] WARN: Save path is not a directory or empty: '$TORRENT_SAVE_PATH'" >> "$LOG_FILE"
  # We *can* still try to work, but relative paths may be weird
fi

# Recursively find video files and hardlink them
find "$TORRENT_CONTENT_PATH" -type f \
  \( -iname "*.mkv" -o -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mov" \) | while IFS= read -r file; do

  # Compute path relative to the SAVE path (download root)
  # Example:
  #   SAVE_PATH: /data/torrents/anime-hentai/downloads
  #   file:      /data/torrents/anime-hentai/downloads/[SakuraCircle]/Ep01.mkv
  #   relpath:   [SakuraCircle]/Ep01.mkv
  relpath="${file#"$TORRENT_SAVE_PATH"/}"

  # If stripping didn't change anything (edge case), fall back to stripping content path
  if [[ "$relpath" == "$file" ]]; then
    relpath="${file#"$TORRENT_CONTENT_PATH"/}"
  fi

  destfile="$SHOKO_SOURCE/$relpath"

  mkdir -p "$(dirname "$destfile")"

  # Attempt to hardlink
  if ln "$file" "$destfile" 2>/dev/null; then
    echo "[$(ts)] ✅ Hardlinked: $relpath" >> "$LOG_FILE"
  else
    echo "[$(ts)] ⚠️ Failed to hardlink (maybe cross-dataset or already exists): $relpath" >> "$LOG_FILE"
  fi
done

echo "[$(ts)] Done Torrent: '$TORRENT_NAME'" >> "$LOG_FILE"
exit 0

