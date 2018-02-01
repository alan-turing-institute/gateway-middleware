#!/bin/bash
name=$(docker-compose run -p "8082:5432" postgres)
sleep 10
python create_and_mint_case_using_stores.py
sleep 10
docker stop "$name"