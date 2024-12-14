from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from ..services.database import DatabaseService
from ..models.document import Document

app = FastAPI(title="InsightVault API")
db = DatabaseService()

class QueryRequest(BaseModel):
    query: str
    collection: str = "default"
    k: int = 5

class QueryResponse(BaseModel):
    results: List[Document]

@app.on_event("startup")
async def startup() -> None:
    await db.init()

@app.post("/documents/", response_model=Document)
async def add_document(
    file: UploadFile = File(...),
    collection: str = "default"
) -> Document:
    """Add a document to the database"""
    try:
        content = await file.read()
        # TODO: Implement document creation from file
        document = Document(id="temp", content=content.decode())
        await db.add_document(document, collection)
        return document
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/query/", response_model=QueryResponse)
async def query(request: QueryRequest) -> QueryResponse:
    """Query the database"""
    try:
        results = await db.query(
            query=request.query,
            collection=request.collection,
            k=request.k
        )
        return QueryResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint"""
    return {"status": "healthy"} 