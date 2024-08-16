cd ~
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github

cd ~/swissmed-health
git pull

cd ~/frappe_docker
git pull

# docker pull phalouvas/swissmed-worker:version-15
docker compose --project-name erpnext-v15 down
docker compose --project-name erpnext-v15 -f ~/swissmed-health/deploy/erpnext-v15.yaml up -d
docker exec -it erpnext-v15-backend-1 bench pip install invoice2data
docker exec -it erpnext-v15-backend-1 bench pip install json2table
docker exec -it erpnext-v15-backend-1 bench --site all migrate
docker exec -it erpnext-v15-backend-1 bench --site all clear-cache
docker exec -it erpnext-v15-backend-1 bench --site all clear-website-cache

docker images | grep swissmed
