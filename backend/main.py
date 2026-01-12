from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
from decision_engine import DecisionEngine
from models import ComparisonRequest, ComparisonResult
from db import Database

app = FastAPI(title="Decision Intelligence Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db = Database()
decision_engine = DecisionEngine()

@app.on_event("startup")
async def startup_event():
    await db.init_db()

@app.get("/")
async def root():
    return {"message": "Decision Intelligence Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/compare", response_model=ComparisonResult)
async def compare_options(request: ComparisonRequest):
    try:
        # Process the comparison request
        result = await decision_engine.compare(request)
        
        # Store in database
        comparison_id = await db.store_comparison(request, result)
        result.comparison_id = comparison_id
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/comparisons/{comparison_id}")
async def get_comparison(comparison_id: str):
    try:
        comparison = await db.get_comparison(comparison_id)
        if not comparison:
            raise HTTPException(status_code=404, detail="Comparison not found")
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/comparisons")
async def list_comparisons(limit: int = 10):
    try:
        comparisons = await db.list_comparisons(limit)
        return {"comparisons": comparisons}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)