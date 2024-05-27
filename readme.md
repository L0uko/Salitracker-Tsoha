
# Salitracker 
The function of this database is to track the users gym visits and show the progress that the user has made.

# Features
The webpage has the following features:
  - Logging in
  - Input the made exercises
  - input the done cardio workout
  - The weight and sets of the exercises / distance and time in cardios 
  - The date
  - List of previous exercises
  - Total repetitions per workout / speed
  - The maximum weight that the user has lifted for every exercise
  - A ready list of motivational quotes that rotate on the main page
  - ability to add your own quotes to the list



# How to run and debug
Below is a brief tutorial on how to get the database and webpage running on your own (linux) computer: (If you are on Windows, you can run these commands through Git Bash etc.)

Firstly you need to have [Docker](https://www.docker.com/) installed on your machine.


So, 
Run these 2 commands in different terminals in this order
This command makes the database exist inside a container and it gives it a name, user and a password.

    docker run --name inventory-dev-postgres -e POSTGRES_USER=db-username -e POSTGRES_PASSWORD=db-password -e POSTGRES_DB=db-name --rm -p 5432:5432 postgres

   This second command puts the necessary tables to the database from schema.sql.

     docker exec -i inventory-dev-postgres psql -U db-username db-name < schema.sql

Now you must create .env file for the enviromental variables.
Copy this into the file:

`DATABASE_URL=postgresql://db-username:db-password@localhost/db-name`  
`SECRET_KEY=<your-secret-key>`  



Now that the db is running to start the webpage you just need to run the normal `flask run` I dont know about others but I didn't need to run the `source venv/bin/activate`.


 If you want to see the actual db the normal `psql` wont work because it's inside a container. You need to run 2 commands. First you go inside the container and then connect to the db. 

How to get in to the db using docker exec: `docker exec -it inventory-dev-postgres bash`

In bash:    `psql -d db-name -U db-username`






