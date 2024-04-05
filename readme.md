README
The function of this database is to track the users gym visits and show the progress that the user has made.

It will have atleast the following features:
  Logging in
  input the made exercises
  the weight of the exercises
  the date
  graph of previous exercises
  ability to make custom exercises
  total repetitions per workout
  
Run these 2 commands in different terminals in this order
docker run --name inventory-dev-postgres -e POSTGRES_USER=db-username -e POSTGRES_PASSWORD=db-password -e POSTGRES_DB=db-name --rm -p 5432:5432 postgres

docker exec -i inventory-dev-postgres psql -U db-username db-name < schema.sql

And run this to start the server:
docker image build . -t sovellus-server && docker run -it --rm -p 5000:5000 sovellus-server

How to get in to the db usin docker exec:
docker exec -it inventory-dev-postgres bash

In bash:
psql -d db-name -U db-username