from fastapi import FastAPI
from sqlalchemy import inspect

from auth import auth_router
from db import Base, engine
from service import service_router

app = FastAPI()
app.include_router(service_router)
app.include_router(auth_router)


@app.on_event("startup")
def setup():
    print("Creating db tables...")
    Base.metadata.create_all(bind=engine)
    inspection = inspect(engine)
    print(f"Created {len(inspection.get_table_names())} tables: "
          f"{inspection.get_table_names()}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app")
