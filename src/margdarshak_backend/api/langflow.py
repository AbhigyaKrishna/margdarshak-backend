import json
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import requests
from pydantic import BaseModel

from src.margdarshak_backend.core.config import settings

router = APIRouter()

with open('flow_endpoint.json', 'r') as file:
    flow_endpoint = json.load(file)

class AIRequest(BaseModel):
    message: str
    endpoint: str
    output_type: str = "chat"
    input_type: str = "chat"

@router.post("/execute_ai")
def run_flow(request: AIRequest) -> dict:
    """
    Run a flow with a given message.

    Args:
        request: AIRequest object containing:
            - message: The message to send to the flow
            - endpoint: The ID or the endpoint name of the flow
            - output_type: Type of output (default: "chat")
            - input_type: Type of input (default: "chat")
    
    Returns:
        dict: The JSON response from the flow
    """
    endpoint = flow_endpoint[request.endpoint] if request.endpoint in flow_endpoint else request.endpoint
    api_url = f"{settings.LANGFLOW_API_URL}/lf/{settings.LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": request.message,
        "output_type": request.output_type,
        "input_type": request.input_type,
    }
    headers = {"Authorization": f"Bearer {settings.LANGFLOW_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()