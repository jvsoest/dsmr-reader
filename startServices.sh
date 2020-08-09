docker network create dsmr


docker volume create influxdb_storage
docker run -d \
    --name influxdb \
    --restart unless-stopped \
    -p 8086:8086 \
    -v influxdb_storage:/var/lib/influxdb \
    --net=dsmr \
    influxdb

docker volume create grafana_storage
docker run -d \
    --name grafana \
    --restart unless-stopped \
    -p 3000:3000 \
    -v grafana_storage:/var/lib/grafana \
    --link influxdb \
    --net=dsmr \
    grafana/grafana

# cd reader_service && docker build -t dsmr_reader ./
docker run -d \
    --name dsmr_reader \
    --restart unless-stopped \
    --link influxdb \
    -e INFLUXDB_API_URI=http://influxdb:8086 \
    -e INFLUXDB_DB_NAME=meterstanden \
    --device /dev/ttyUSB0:/dev/ttyUSB1 \
    --net=dsmr \
    dsmr_reader
