import requests
import os
import time
from typing import List, Dict, Any, BinaryIO, Tuple

from iqsuite.utils import get_mime_type
from .exceptions import AuthenticationError, APIError
from .models import (
    DocumentListResponse,
    TaskResponse,
    User,
    Index,
    TaskStatus,
    InstantRagResponse,
    InstantRagQueryResponse,
    WebhookDeleteResponse,
    WebhookListResponse,
    WebhookResponse,
)


class IQSuiteClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = None,
    ):
        self.api_key = api_key
        self.base_url = (
            base_url or os.getenv("IQSUITE_BASE_URL") or "https://iqsuite.ai/api/v1"
        ).rstrip("/")

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            response.raise_for_status()
            try:
                data = response.json()
            except ValueError:
                raise APIError("Invalid JSON response from API")

            if isinstance(data, dict) and data.get("error"):
                raise APIError(
                    f"API error: {data['error']}",
                    status_code=response.status_code,
                    response=response,
                )

            if isinstance(data, dict) and "data" in data:
                return data

            return data

        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 422:
                try:
                    error_data = response.json()
                    error_message = error_data.get("message", str(e))
                    raise APIError(
                        f"Validation error: {error_message}",
                        status_code=response.status_code,
                        response=response,
                    )
                except ValueError:
                    pass

            raise APIError(
                f"HTTP {response.status_code} error: {str(e)}",
                status_code=response.status_code,
                response=response,
            )

    def get_user(self) -> User:
        response = self.session.get(f"{self.base_url}/user")
        data = self._handle_response(response)
        return User(**data)

    def list_indexes(self) -> List[Index]:
        response = self.session.get(f"{self.base_url}/index")
        data = self._handle_response(response)
        return [Index(**index) for index in data]

    def get_documents(self, index_id: str) -> DocumentListResponse:
        response = self.session.get(
            f"{self.base_url}/index/get-all-documents", params={"index": index_id}
        )
        response_data = self._handle_response(response)
        return DocumentListResponse(data=response_data["data"])

    def create_index(self, document: BinaryIO, filename: str) -> TaskResponse:
        mime_type = get_mime_type(filename)

        supported_types = {
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        }

        if mime_type not in supported_types:
            raise ValueError(
                f"Unsupported file type: {mime_type}. "
                "Supported types are: PDF, DOC, DOCX, JPG, PNG, TIFF, BMP"
            )

        original_headers = self.session.headers.copy()
        self.session.headers.pop("Content-Type", None)

        try:
            files = {"document": (filename, document, mime_type)}
            response = self.session.post(f"{self.base_url}/index/create", files=files)
            response_data = self._handle_response(response)
            return TaskResponse(data=response_data["data"])

        finally:
            self.session.headers = original_headers

    def add_document(
        self, index_id: str, document: BinaryIO, filename: str
    ) -> TaskResponse:
        mime_type = get_mime_type(filename)

        supported_types = {
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
            "image/tiff",
            "image/bmp",
        }

        if mime_type not in supported_types:
            raise ValueError(
                f"Unsupported file type: {mime_type}. "
                "Supported types are: PDF, DOC, DOCX, JPG, PNG, TIFF, BMP"
            )

        original_headers = self.session.headers.copy()
        self.session.headers.pop("Content-Type", None)

        try:
            files = {"document": (filename, document, mime_type)}
            response = self.session.post(
                f"{self.base_url}/index/add-document",
                data={"index": index_id},
                files=files,
            )
            response_data = self._handle_response(response)
            return TaskResponse(data=response_data["data"])

        finally:
            self.session.headers = original_headers

    def create_index_and_poll(
        self,
        document: BinaryIO,
        filename: str,
        max_retries: int = 5,
        poll_interval: int = 5,
    ) -> Tuple[TaskResponse, TaskStatus]:
        response = self.create_index(document, filename)
        task_id = response.data.task_id

        retries = 0
        while retries < max_retries:
            status = self.get_task_status(task_id)
            if status.status == "completed":
                return response, status
            elif status.status == "failed":
                raise APIError(f"Task failed with status: {status.status}")

            time.sleep(poll_interval)
            retries += 1

        raise APIError(
            f"Maximum retries ({max_retries}) reached while polling task status"
        )

    def add_document_and_poll(
        self,
        index_id: str,
        document: BinaryIO,
        filename: str,
        max_retries: int = 5,
        poll_interval: int = 5,
    ) -> Tuple[TaskResponse, TaskStatus]:
        response = self.add_document(index_id, document, filename)
        task_id = response.data.task_id

        retries = 0
        while retries < max_retries:
            status = self.get_task_status(task_id)
            if status.status == "completed":
                return response, status
            elif status.status == "failed":
                raise APIError(f"Task failed with status: {status.status}")

            time.sleep(poll_interval)
            retries += 1

        raise APIError(
            f"Maximum retries ({max_retries}) reached while polling task status"
        )

    def get_task_status(self, task_id: str) -> TaskStatus:
        response = self.session.get(
            f"{self.base_url}/create-index/task-status/{task_id}"
        )
        data = self._handle_response(response)
        return TaskStatus(**data)

    def chat(self, index_id: str, query: str) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/index/retrieve", json={"index": index_id, "query": query}
        )
        return self._handle_response(response)

    def search(self, index_id: str, query: str) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/index/search", json={"index": index_id, "query": query}
        )
        return self._handle_response(response)

    def delete_document(self, index_id: str, document_id: str) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/index/delete-document",
            json={"index": index_id, "document": document_id},
        )
        return self._handle_response(response)

    def create_instant_rag(self, context: str) -> InstantRagResponse:
        response = self.session.post(
            f"{self.base_url}/index/instant/create", json={"context": context}
        )
        data = self._handle_response(response)
        return InstantRagResponse(**data)

    def query_instant_rag(self, index_id: str, query: str) -> InstantRagQueryResponse:
        response = self.session.post(
            f"{self.base_url}/index/instant/query",
            json={"index": index_id, "query": query},
        )
        data = self._handle_response(response)
        return InstantRagQueryResponse(**data)

    def list_webhooks(self) -> WebhookListResponse:
        response = self.session.get(f"{self.base_url}/webhooks")
        data = self._handle_response(response)
        return WebhookListResponse(**data)

    def create_webhook(
        self, url: str, name: str, secret: str, enabled: str
    ) -> WebhookResponse:
        payload = {
            "url": url,
            "name": name,
            "enabled": enabled,
            "secret": secret,
        }
        response = self.session.post(f"{self.base_url}/webhooks", json=payload)
        data = self._handle_response(response)
        return WebhookResponse(**data)

    def update_webhook(
        self, webhook_id: str, url: str, name: str, enabled: str
    ) -> WebhookResponse:
        payload = {
            "webhook_id": webhook_id,
            "url": url,
            "name": name,
            "enabled": enabled,
        }
        response = self.session.post(f"{self.base_url}/webhooks/update", json=payload)
        data = self._handle_response(response)
        return WebhookResponse(**data)

    def delete_webhook(self, webhook_id: str) -> WebhookDeleteResponse:
        payload = {"webhook_id": webhook_id}
        response = self.session.post(f"{self.base_url}/webhooks/delete", json=payload)
        data = self._handle_response(response)
        return WebhookDeleteResponse(**data)
