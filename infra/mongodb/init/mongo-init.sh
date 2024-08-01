#!/bin/bash

# инициализируем серверы конфигурации
echo "Configuring config server replica set..."
mongosh --host mongocfg1:27017 <<EOF
rs.initiate({
  _id: "mongors1conf",
  configsvr: true,
  members: [
    { _id: 0, host: "mongocfg1" },
    { _id: 1, host: "mongocfg2" },
    { _id: 2, host: "mongocfg3" }
  ]
})
EOF

sleep 5

# иницилизируем replica set первого шарда
echo "Configuring shard server replica set..."
mongosh --host mongors1n1:27017 <<EOF
rs.initiate({
  _id: "mongors1",
  members: [
    { _id: 0, host: "mongors1n1" },
    { _id: 1, host: "mongors1n2" },
    { _id: 2, host: "mongors1n3" }
  ]
})
EOF

# иницилизируем replica set второго шарда
echo "Configuring shard server replica set..."
mongosh --host mongors2n1:27017 <<EOF
rs.initiate({
  _id: "mongors2",
  members: [
    { _id: 0, host: "mongors2n1" },
    { _id: 1, host: "mongors2n2" },
    { _id: 2, host: "mongors2n3" }
  ]
})
EOF

# функция для попытки подключения шардов к кластеру
add_shard_with_retry() {
  local shard=$1
  local host=$2
  local max_retries=5
  local attempt=1
  local success=0

  while [ $attempt -le $max_retries ]; do
    echo "Attempt $attempt: Adding shard $shard..."
    mongosh --host mongos1:27017 <<EOF
sh.addShard("$shard/$host")
EOF

    if [ $? -eq 0 ]; then
      success=1
      break
    else
      echo "Failed to add shard $shard. Retrying in 10 seconds..."
      sleep 5
      attempt=$((attempt + 1))
    fi
  done

  if [ $success -ne 1 ]; then
    echo "Failed to add shard $shard after $max_retries attempts. Exiting."
    exit 1
  fi
}

# добавляем шарды в кластер
add_shard_with_retry "mongors1" "mongors1n1"
add_shard_with_retry "mongors2" "mongors2n1"

# настраиваем шардироване коллекций
echo "Adding shards to the cluster..."
mongosh --host mongos1:27017 <<EOF
use ugc
sh.enableSharding("ugc")

db.createCollection("reviews")
sh.shardCollection("ugc.reviews", {"film_id": "hashed"})

db.createCollection("films")
sh.shardCollection("ugc.films", {"_id": "hashed"})

db.createCollection("users")
sh.shardCollection("ugc.users", {"_id": "hashed"})
EOF


echo "MongoDB sharded cluster setup completed."
