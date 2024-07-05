
# Setup and deploy

For preparing and setup of docker services this repository works together with fork repository [frappe_docker](https://github.com/phalouvas/frappe_docker.git)

## First time setup

All commands should by run only once for a new server. Make sure to update passwords in evnironment files before running.
The files to update are:
* erpnext-v15.env
* mariadb.env

**Traefik**

```shell
docker compose --project-name traefik \
  --env-file ~/swissmedhealth/deploy/traefik.env \
  -f ~/frappe_docker/overrides/compose.traefik.yaml \
  -f ~/frappe_docker/overrides/compose.traefik-ssl.yaml up -d
```

**MariaDB**

```shell
docker compose --project-name mariadb --env-file ~/swissmedhealth/deploy/mariadb.env -f ~/frappe_docker/overrides/compose.mariadb-shared.yaml up -d
```

**phpMyAdmin**

```shell
docker compose --project-name phpmyadmin --env-file ~/swissmedhealth/deploy/phpmyadmin.env -f ~/frappe_docker/overrides/compose.phpmyadmin.yaml up -d
```

**Erpnext**

Create a yaml file called `erpnext-v15.yaml` in `~/swissmedhealth/deploy` directory:

```shell
docker compose --project-name erpnext-v15 \
  --env-file ~/swissmedhealth/deploy/erpnext-v15.env \
  -f ~/frappe_docker/compose.yaml \
  -f ~/frappe_docker/overrides/compose.redis.yaml \
  -f ~/frappe_docker/overrides/compose.backup.yaml \
  -f ~/frappe_docker/overrides/compose.multi-bench.yaml \
  -f ~/frappe_docker/overrides/compose.multi-bench-kainotomo.yaml \
  -f ~/frappe_docker/overrides/compose.multi-bench-ssl.yaml config > ~/swissmedhealth/deploy/erpnext-v15.yaml
```

```shell
docker compose --project-name erpnext-v15 -f ~/swissmedhealth/deploy/erpnext-v15.yaml up -d
```

## Build image

Below should be run on local machine to avoid availability on production server.

- Export apps to variable and build image
  ```shell

  export APPS_JSON_BASE64=$(base64 -w 0 ~/swissmedhealth/deploy/v15.json)

  cd ~/frappe_docker

  docker build  --no-cache --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe \
    --build-arg=FRAPPE_BRANCH=version-15 \
    --build-arg=PYTHON_VERSION=3.11.6 \
    --build-arg=NODE_VERSION=18.18.2 \
    --build-arg=APPS_JSON_BASE64=$APPS_JSON_BASE64 \
    --tag=phalouvas/swissmed-worker:15.29.2 \
    --file=images/azure/Containerfile .

  docker push phalouvas/swissmed-worker:15.29.2
  docker tag phalouvas/swissmed-worker:15.29.2 phalouvas/swissmed-worker:version-15
  docker push phalouvas/swissmed-worker:version-15

    ```

## Deploy

Run below on production server.

```shell
~/swissmedhealth/deploy/deploy.sh
```

To delete old image in order to free up space use command `docker rmi -f phalouvas/swissmed-worker:x.x.x` where x.x.x the old version
