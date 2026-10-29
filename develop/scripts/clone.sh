#!/bin/bash
# Clone every [package] from sources.ini into ./sources (same layout mxdev uses
# inside the image), so ./sources can be mounted for live editing.

mkdir -p sources

awk -F' = ' '
  /^\[/ { name = substr($0, 2, length($0) - 2) }
  $1 == "url" { url[name] = $2 }
  $1 == "branch" { branch[name] = $2 }
  END { for (n in url) if (n != "settings") print n, url[n], branch[n] }
' sources.ini | while read -r name url branch; do
  if [ -d "sources/$name" ]; then
    echo "exists: sources/$name"
  else
    git clone -b "$branch" "$url" "sources/$name"
  fi
done
