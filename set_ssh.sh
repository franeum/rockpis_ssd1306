#!/usr/bin/env bash

for i in ROCKPIS-*; do
    cd ${i}
    name=`git remote -v | grep -Po "/.+\.git"`
    git remote set-url origin git@github.com:franeum${name}
    cd ..
done
