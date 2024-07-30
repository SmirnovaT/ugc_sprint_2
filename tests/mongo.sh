#!/bin/bash
mongosh --quiet <<EOF
use ugc

db.createCollection("reviews")
db.createCollection("films")
db.createCollection("users")
EOF