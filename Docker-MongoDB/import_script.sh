#!/bin/bash

# Start MongoDB in the background with the bind_ip setting
mongod --fork --logpath /var/log/mongod.log --bind_ip 0.0.0.0

# Wait for MongoDB to fully start
sleep 5

# Import the CSV file into MongoDB
mongoimport --type csv -d mydatabase -c mycollection --headerline --drop --file /data/train.csv

# Keep the container running
tail -f /dev/null