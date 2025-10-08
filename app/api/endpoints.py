from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import httpx
import backoff
from app.core.config import settings
import json

class Attachment(BaseModel):
    name: str
    url: str

class CodeRequest(BaseModel):
    email: EmailStr
    secret: str
    task: str
    round: int
    nonce: str
    brief: str
    checks: List[str]
    evaluation_url: str
    attachments: Optional[List[Attachment]] = []

class EvaluationResponse(BaseModel):
    email: str
    task: str
    round: int
    nonce: str
    repo_url: str
    commit_sha: str
    pages_url: str

@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def send_evaluation_result(evaluation_url: str, response: EvaluationResponse):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            evaluation_url,
            json=response.dict(),
            headers={"Content-Type": "application/json"}
        )
        resp.raise_for_status()
        return resp.json()

router = APIRouter()

@router.post("/submit")
async def handle_submission(request: CodeRequest, background_tasks: BackgroundTasks):
    # Verify secret
    if request.secret != settings.SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid secret")

    # Process request based on round
    if request.round == 1:
        # Initial request handling
        result = await process_initial_request(request)
    elif request.round == 2:
        # Revision request handling
        result = await process_revision_request(request)
    else:
        raise HTTPException(status_code=400, detail="Invalid round number")

    # Send evaluation result in background
    background_tasks.add_task(send_evaluation_result, request.evaluation_url, result)
    
    return {"status": "success", "message": "Request processed successfully"}

async def process_initial_request(request: CodeRequest) -> EvaluationResponse:
    # Import here to avoid circular imports
    from app.api.llm_integration import process_initial_request as llm_process
    return await llm_process(request)

async def process_revision_request(request: CodeRequest) -> EvaluationResponse:
    from app.api.llm_integration import process_revision_request as llm_revision_process
    return await llm_revision_process(request)