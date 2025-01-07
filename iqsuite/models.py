from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class User(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        extra = "allow"


class Index(BaseModel):
    id: str
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    document_count: Optional[int] = None

    class Config:
        extra = "allow"


class Document(BaseModel):
    """Model for document information"""

    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        extra = "allow"


class DocumentListData(BaseModel):
    """Model for document list data"""

    documents: List[Document]
    index: str

    class Config:
        extra = "allow"


class DocumentListResponse(BaseModel):
    """Model for document list response wrapper"""

    data: DocumentListData

    class Config:
        extra = "allow"


class TaskStatus(BaseModel):
    status: str
    task_id: Optional[str] = None

    class Config:
        extra = "allow"


class TaskResponseData(BaseModel):
    """Model for task response data"""

    message: str
    task_id: str
    check_status: str

    class Config:
        extra = "allow"


class TaskResponse(BaseModel):
    """Model for task creation response wrapper"""

    data: TaskResponseData

    class Config:
        extra = "allow"


class InstantRagResponse(BaseModel):
    """Model for instant RAG creation response"""

    message: str
    id: str
    query_url: str

    class Config:
        extra = "allow"


class InstantRagQueryData(BaseModel):
    """Model for instant RAG query response data"""

    uuid: str
    query: str
    retrieval_response: str
    credits_cost: float
    total_tokens: int

    class Config:
        extra = "allow"


class InstantRagQueryResponse(BaseModel):
    """Model for instant RAG query response"""

    data: InstantRagQueryData

    class Config:
        extra = "allow"
