#!/bin/bash
set -e
current_directory=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
python3 "$current_directory/utils/encrypt.py"
echo "successfully encrypted your aws credentials"