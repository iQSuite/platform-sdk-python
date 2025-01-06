from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class User(BaseModel):
    id: str
    name: Optional[str]
    email: Optional[str]

class Index(BaseModel):
    id: str
    name: Optional[str]
    created_at: datetime
    document_count: Optional[int]

class Document(BaseModel):
    id: str
    filename: str
    created_at: datetime
    index_id: str

class TaskStatus(BaseModel):
    id: str
    status: str
    progress: Optional[float]
    created_at: datetime
    completed_at: Optional[datetime]