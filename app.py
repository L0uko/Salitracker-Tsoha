from flask import Flask
#How to make new image and run server:
#docker image build . -t sovellus-server && docker run -it --rm -p 5000:5000 sovellus-server

#Run these 2 commands in different terminals in this order to start the database
#docker run --name inventory-dev-postgres -e POSTGRES_USER=db-username -e POSTGRES_PASSWORD=db-password -e POSTGRES_DB=db-name  -p 5432:5432
#docker exec -i inventory-dev-postgres psql -U db-username db-name < schema.sql

'''TODOLIST:

'''
app = Flask(__name__)
import routes
