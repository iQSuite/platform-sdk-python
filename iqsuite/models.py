from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Optional
from datetime import datetime


class User(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class Index(BaseModel):
    id: str
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    document_count: Optional[int] = None

    model_config = ConfigDict(extra="allow")


class Document(BaseModel):
    """Model for document information"""

    id: str
    title: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(extra="allow")


class DocumentListData(BaseModel):
    """Model for document list data"""

    documents: List[Document]
    index: str

    model_config = ConfigDict(extra="allow")


class DocumentListResponse(BaseModel):
    """Model for document list response wrapper"""

    data: DocumentListData

    model_config = ConfigDict(extra="allow")


class TaskStatus(BaseModel):
    status: str
    task_id: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class TaskResponseData(BaseModel):
    """Model for task response data"""

    message: str
    task_id: str
    check_status: str

    model_config = ConfigDict(extra="allow")


class TaskResponse(BaseModel):
    """Model for task creation response wrapper"""

    data: TaskResponseData

    model_config = ConfigDict(extra="allow")


class InstantRagResponse(BaseModel):
    """Model for instant RAG creation response"""

    message: str
    id: str
    query_url: str

    model_config = ConfigDict(extra="allow")


class InstantRagQueryData(BaseModel):
    """Model for instant RAG query response data"""

    uuid: str
    query: str
    retrieval_response: str
    credits_cost: float
    total_tokens: int

    model_config = ConfigDict(extra="allow")


class SourceDocument(BaseModel):
    id: str
    file_name: str

    model_config = ConfigDict(extra="allow")


class InstantRagQueryResponse(BaseModel):
    uuid: str
    total_tokens: int
    retrieval_response: str
    credits_cost: int
    query: str

    model_config = ConfigDict(extra="allow")


class Webhook(BaseModel):
    """Model for webhook information"""

    id: int
    name: str
    enabled: bool
    secret: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra="allow")



class WebhookListResponse(BaseModel):
    """Model for webhook list response"""

    data: List[Webhook]

    model_config = ConfigDict(extra="allow")


class WebhookResponse(BaseModel):
    webhook: Webhook

    model_config = ConfigDict(extra="allow")


class WebhookDeleteResponse(BaseModel):
    """Model for webhook deletion response"""

    data: Dict[str, str]

    model_config = ConfigDict(extra="allow")
