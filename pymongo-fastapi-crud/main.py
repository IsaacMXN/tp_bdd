from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as movies_router
from neo4j import GraphDatabase

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_URL"])
    app.database = app.mongodb_client[config["MONGODB_NAME"]]
    app.neo4j_driver = GraphDatabase.driver(config["BOLT_URI"], auth=(config["USERNAME"], config["PASSWORD"]))
    print("Connected to MongoDB and Neo4j!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    app.neo4j_driver.close()

app.include_router(movies_router, tags=["movies"], prefix="/movies")