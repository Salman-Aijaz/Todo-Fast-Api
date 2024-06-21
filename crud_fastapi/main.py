from typing import Optional
from fastapi import     FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager


class Work(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(index=True)


sqlite_url = f"postgresql://salman333699:SqWz08hpuMdw@ep-muddy-flower-00941143.us-east-2.aws.neon.tech/neonsk?sslmode=require"

engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app:FastAPI =FastAPI(lifespan=lifespan)



@app.post("/todos/")
def create_todo(todo: Work):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.put("/todos/")
def update_todo(todo:Work):
    with Session(engine) as session:
        statement = select(Work).where(Work.id == todo.id)
        results = session.exec(statement)
        workUpdate = results.one()
        print("Updated Work:", workUpdate)

        workUpdate.content =todo.content
        session.add(workUpdate)
        session.commit()
        session.refresh(workUpdate)
        print("Updated Work:", workUpdate)
        return workUpdate

@app.delete("/todos/")
def delete_heroes(todo:Work):
    with Session(engine) as session:
        statement = select(Work).where(Work.id == todo.id)
        results = session.exec(statement)
        deleteTask = results.one()

        session.delete(deleteTask)
        session.commit()
        return "TASK DELETE........"


@app.get("/todos/")
def read_todo():
    with Session(engine) as session:
        todos = session.exec(select(Work)).all()
        return todos