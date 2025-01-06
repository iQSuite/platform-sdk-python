from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class User(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    
    class Config:
        extra = 'allow'

class Index(BaseModel):
    id: str
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    document_count: Optional[int] = None
    
    class Config:
        extra = 'allow'

class Document(BaseModel):
    id: str
    filename: Optional[str] = None
    created_at: Optional[datetime] = None
    index_id: Optional[str] = None
    
    class Config:
        extra = 'allow'

class TaskStatus(BaseModel):
    status: str
    task_id: Optional[str] = None
    progress: Optional[float] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        extra = 'allow'