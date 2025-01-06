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
    """Model for document information"""
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        extra = 'allow'

class DocumentListResponse(BaseModel):
    """Model for document list response"""
    documents: List[Document]
    index: str
    
    class Config:
        extra = 'allow'

class TaskStatus(BaseModel):
    status: str
    task_id: Optional[str] = None
    
    class Config:
        extra = 'allow'


class TaskResponse(BaseModel):
    """Model for task creation response"""
    message: str
    task_id: str
    check_status: str
    
    class Config:
        extra = 'allow'