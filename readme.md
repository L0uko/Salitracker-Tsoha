
# Salitracker 
The function of this database is to track the users gym visits and show the progress that the user has made.

# Features
The final version will have  the following features:
  - Logging in
  - Input the made exercises
  - The weight of the exercises
  - The date
  - Graph of previous exercises
  - Ability to make custom exercises
  - Total repetitions per workout
# Working features
- Logging in
	- Visual confirmation TODO
- Input the made exercises
	- Visual confirmation is still TODO
 - The weight of the exercises
 - Amount of sets
 - The date
 	- You can set the date but it doesnt go to the table (TODO)

# How to run and debug
Below is a brief tutorial on how to get the database and webpage running on your own (linux) computer: (If you are on Windows, you can run these commands through Git Bash etc.)

Firstly you need to have [Docker](https://www.docker.com/) installed on your machine.
[Link to the database docker image](https://hub.docker.com/repository/docker/l0uko/salitracker-db/general). The Docker image is right now useless. You dont need need the image to run the database (if you do it doesnt have a name and creates problems (TODO).

So, 
Run these 2 commands in different terminals in this order
This command makes the database exist inside a container and it gives it a name, user and a password.

    docker run --name inventory-dev-postgres -e POSTGRES_USER=db-username -e POSTGRES_PASSWORD=db-password -e POSTGRES_DB=db-name --rm -p 5432:5432 postgres

   This second command puts the necessary tables to the database from schema.sql.

    docker exec -i inventory-dev-postgres psql -U db-username db-name < schema.sql

Now that the db is running to start the webpage you just need to run the normal `flask run` I dont know about others but I didn't need to run the `source venv/bin/activate`.

~~And run this to start the server:
docker image build . -t sovellus-server && docker run -it --rm -p 5000:5000 sovellus-server~~

 If you want to see the actual db the normal `psql` wont work because it's inside a container. You need to run 2 commands. First you go inside the container and then connect to the db. 

How to get in to the db using docker exec: `docker exec -it inventory-dev-postgres bash`

In bash:    `psql -d db-name -U db-username`

> (The amount of tables has diminished because in the beginning I made
> redundant tables and realised that only now.)





