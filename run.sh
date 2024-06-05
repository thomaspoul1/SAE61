docker build -t flask:1.1 flask/.

docker compose up
#sans paramètre -d pour test que tout fonctionne
#docker compose up -d

host=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mariadb)
mysql -u root -p'foo' -h $host < SQL/db.sql
