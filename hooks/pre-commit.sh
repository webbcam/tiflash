#!/bin/sh

echo "Running pre-commit hook"
added_files=$(git diff --cached --name-only | grep "\.py" | tr '\n' ' ')
if [ -n "${added_files// }" ]; then
    echo "running flake8 on ${added_files}"
    flake8 --exclude=__init__.py --ignore=E128 $added_files
    if [ $? -ne 0 ]; then
        echo "Test must pass flake8 coding style checks before commit!"
        exit 1
    fi
fi
exit 0
