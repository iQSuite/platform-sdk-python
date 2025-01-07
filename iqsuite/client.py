import requests
import os
from typing import List, Dict, Any, BinaryIO
from .exceptions import AuthenticationError, APIError
from .models import (
    DocumentListResponse,
    TaskResponse,
    User,
    Index,
    TaskStatus,
    InstantRagResponse,
    InstantRagQueryResponse,
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
        data = self._handle_response(response)
        return DocumentListResponse(**data)

    def create_index(self, document: BinaryIO, filename: str) -> TaskResponse:
        original_headers = self.session.headers.copy()
        self.session.headers.pop("Content-Type", None)

        try:
            files = {"document": (filename, document, "application/pdf")}
            response = self.session.post(f"{self.base_url}/index/create", files=files)
            data = self._handle_response(response)
            return TaskResponse(**data)

        finally:
            self.session.headers = original_headers

    def add_document(
        self, index_id: str, document: BinaryIO, filename: str
    ) -> TaskResponse:
        original_headers = self.session.headers.copy()
        self.session.headers.pop("Content-Type", None)

        try:
            files = {"document": (filename, document, "application/pdf")}
            response = self.session.post(
                f"{self.base_url}/index/add-document",
                data={"index": index_id},
                files=files,
            )
            data = self._handle_response(response)
            return TaskResponse(**data)

        finally:
            self.session.headers = original_headers

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
