#!/bin/bash
# Take a picture of a page with headless Chrome (nothing opens on screen).
rm -f "$2"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
    --user-data-dir="$(mktemp -d)" --no-proxy-server --window-size=1280,760 --screenshot="$2" "$1" > /dev/null 2>&1
[ -f "$2" ] && echo "saved $2"
