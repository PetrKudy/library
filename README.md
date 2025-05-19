# Library app

## Run project
1) git clone this repository
2) rename .env-sample to .env
3) run `docker-compose -f docker-compose.local.yml up`
4) develop!

## Testing
1) exec to container: `docker exec -it library_web bash`
2) run `pytest`