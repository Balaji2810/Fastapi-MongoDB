from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field
from bson import ObjectId
import os


class Student(Document):
    id: str = Field(default_factory=lambda:str(ObjectId()))
    name: str 
    age: int 
    dept: str 


MONGODB_URI = os.environ["MONGODB_URI"]


async def mongo_init():
    # Beanie uses Motor async client under the hood 
    client = AsyncIOMotorClient(MONGODB_URI)

    # Initialize beanie with the Product document class
    await init_beanie(database=client[MONGODB_URI.split("/")[-1]], document_models=[Student])