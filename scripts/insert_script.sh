#!/bin/sh

head -n 50 $1 | \
    awk -F':' 'NR!=1 {system("echo "$2" | sha256sum") }' | \
    awk '{system("echo psql -d zucced_db -c INSERT INTO compromised_accounts(facebook_id_hash) VALUES (\'"$1"\');") }'
