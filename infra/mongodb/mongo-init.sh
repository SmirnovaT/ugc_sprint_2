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

sleep 5

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

sleep 5

# добавляем шарды в кластер
echo "Adding shards to the cluster..."
mongosh --host mongos1:27017 <<EOF
sh.addShard("mongors1/mongors1n1")
sh.addShard("mongors2/mongors2n1")
sh.status()
EOF

echo "MongoDB sharded cluster setup completed."
