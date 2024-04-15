from flask import Flask
#How to make new image and run server:
#docker image build . -t sovellus-server && docker run -it --rm -p 5000:5000 sovellus-server

#Run these 2 commands in different terminals in this order to start the database
#docker run --name inventory-dev-postgres -e POSTGRES_USER=db-username -e POSTGRES_PASSWORD=db-password -e POSTGRES_DB=db-name  -p 5432:5432
#docker exec -i inventory-dev-postgres psql -U db-username db-name < schema.sql

'''TODOLIST:
TODO more tables (dont know how)
TODO profile sort by time exercises
TODO Running
TODO route where can choose between running and gym 
(maybe 3rd option? sport?)
TODO Profile see all exercises
TODO Templates?(new tables?)
'''
app = Flask(__name__)
import routes
