import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.core.config import settings

app = FastAPI(
    version="0.0.1",
    title=settings.project_name,
    description="UGC service for Online cinema",
    docs_url="/ugc/api/openapi",
    openapi_url="/ugc/api/openapi.json",
    default_response_class=ORJSONResponse,
    contact={
        "name": "Amazing python team",
        "email": "amazaingpythonteam@fake.com",
    },
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
