#!/usr/bin/env bash

GIT_DIR=$(git rev-parse --git-dir)

echo "Installing hooks..."
# ln -s in Windows is just a cp (needs to be recopied each time)
if [ -f $GIT_DIR/hooks/pre-commit ]; then
    rm -f $GIT_DIR/hooks/pre-commit
fi
# this command creates symlink to our pre-commit script
ln -s ../../hooks/pre-commit.sh $GIT_DIR/hooks/pre-commit
echo "Done!"
