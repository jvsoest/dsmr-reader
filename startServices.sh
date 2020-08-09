
if [ -z "$1" ] || [ "$1" -eq "influxdb" ]
then
docker volume create influxdb_storage
docker run -d \
    --name influxdb \
    --restart unless-stopped \
    -p 8086:8086 \
    -v influxdb_storage:/var/lib/influxdb \
    influxdb
fi

if [ -z "$1" ] || [ "$1" -eq "grafana" ]
then
docker volume create grafana_storage
docker run -d \
    --name grafana \
    --restart unless-stopped \
    -p 3000:3000 \
    -v grafana_storage:/var/lib/grafana \
    --link influxdb \
    grafana/grafana
fi

if [ -z "$1" ] || [ "$1" -eq "dsmr_reader" ]
then

if [[ "$(docker images -q dsmr_reader 2> /dev/null)" == "" ]]; then
    cd reader_service && docker build -t dsmr_reader ./
fi

docker run -d \
    --name dsmr_reader \
    --restart unless-stopped \
    --link influxdb \
    -e INFLUXDB_API_URL=http://influxdb:8086 \
    -e INFLUXDB_DB_NAME=meterstanden \
    dsmr_reader
fi
