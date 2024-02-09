from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from database import mongo_init, Student


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Database connection opened")
    await mongo_init()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/student")
async def create_student(name: str = Form(...), age: int = Form(...), dept: str = Form(...)):
    student = Student(name=name, age=age, dept=dept)
    await student.create()
    return {"message": "Student has been created","id":student.id}

@app.get("/student")
async def get_student():
    students = await Student.find_all().to_list()
    return {"message": "Student has been fetched","data":students}

@app.get("/student/{id}")
async def get_student_by_id(id: str):
    student = await Student.get(id)
    return JSONResponse({"message": f"Student with id {id} has been fetched","data":student})

@app.put("/student/{id}")
async def update_student(id: str, name: str = Form(...), age: int = Form(...), dept: str = Form(...)):
    student = await Student.get(id)
    student.name = name
    student.age = age
    student.dept = dept
    await student.save()
    return {"message": f"Student with id {id} has been updated"}

@app.delete("/student/{id}")
async def delete_student(id: str):
    student = await Student.get(id)
    await student.delete()
    return {"message": f"Student with id {id} has been deleted"}