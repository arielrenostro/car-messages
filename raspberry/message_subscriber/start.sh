#!/bin/bash

for i in $(cat .env); do
    eval "export ${i}"
done

python3.7 app.py