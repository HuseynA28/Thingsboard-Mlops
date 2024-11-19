#!/bin/bash
jupyter lab --ip=0.0.0.0 --allow-root --port=1010 --no-browser &
uvicorn myFastapi.main:app --reload --host 0.0.0.0 --port 8060
