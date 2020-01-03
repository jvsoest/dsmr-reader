docker volume create influxdb_storage
docker run -d \
    --name influxdb \
    --restart unless-stopped \
    -p 8086:8086 \
    -v influxdb_storage:/var/lib/influxdb \
    influxdb

docker volume create grafana_storage
docker run -d \
    --name grafana \
    --restart unless-stopped \
    -p 3000:3000 \
    -v grafana_storage:/var/lib/grafana \
    --link influxdb \
    grafana/grafana
