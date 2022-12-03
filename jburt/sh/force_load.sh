#!/bin/bash

# force-load data from S3 onto FSx

TARGET="*.h5"

find "$1" -type f -name "$TARGET" -print0 | while IFS= read -r -d '' file
do
    echo "$file" && head -c 1 "$file" > /dev/null 2>&1
done
