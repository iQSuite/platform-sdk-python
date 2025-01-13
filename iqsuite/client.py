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

import logging

logger = logging.getLogger(__name__)


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

    def _handle_response(self, response: requests.Response) -> Any:
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
                logger.debug(f"Response data: {data['data']}")
                return data["data"]  # Return only the 'data' part

            logger.debug(f"Response data: {data}")
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
        except Exception as e:
            raise APIError(f"Unexpected error: {str(e)}") from e

    def get_user(self) -> User:
        try:
            response = self.session.get(f"{self.base_url}/user")
            data = self._handle_response(response)
            return User(**data)
        except Exception as e:
            raise APIError(f"Error in get_user: {str(e)}") from e

    def list_indexes(self) -> List[Index]:
        try:
            response = self.session.get(f"{self.base_url}/index")
            data = self._handle_response(response)
            return [Index(**index) for index in data]
        except Exception as e:
            raise APIError(f"Error in list_indexes: {str(e)}") from e

    def get_documents(self, index_id: str) -> DocumentListResponse:
        try:
            response = self.session.get(
                f"{self.base_url}/index/get-all-documents", params={"index": index_id}
            )
            response_data = self._handle_response(response)
            return DocumentListResponse(data=response_data)
        except Exception as e:
            raise APIError(f"Error in get_documents: {str(e)}") from e

    def create_index(self, document: BinaryIO, filename: str) -> TaskResponse:
        try:
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
                response = self.session.post(
                    f"{self.base_url}/index/create", files=files
                )
                response_data = self._handle_response(response)
                return TaskResponse(data=response_data)

            finally:
                self.session.headers = original_headers
        except Exception as e:
            raise APIError(f"Error in create_index: {str(e)}") from e

    def add_document(
        self, index_id: str, document: BinaryIO, filename: str
    ) -> TaskResponse:
        try:
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
                return TaskResponse(data=response_data)

            finally:
                self.session.headers = original_headers
        except Exception as e:
            raise APIError(f"Error in add_document: {str(e)}") from e

    def create_index_and_poll(
        self,
        document: BinaryIO,
        filename: str,
        max_retries: int = 5,
        poll_interval: int = 5,
    ) -> Tuple[TaskResponse, TaskStatus]:
        try:
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
        except Exception as e:
            raise APIError(f"Error in create_index_and_poll: {str(e)}") from e

    def add_document_and_poll(
        self,
        index_id: str,
        document: BinaryIO,
        filename: str,
        max_retries: int = 5,
        poll_interval: int = 5,
    ) -> Tuple[TaskResponse, TaskStatus]:
        try:
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
        except Exception as e:
            raise APIError(f"Error in add_document_and_poll: {str(e)}") from e

    def get_task_status(self, task_id: str) -> TaskStatus:
        try:
            response = self.session.get(
                f"{self.base_url}/create-index/task-status/{task_id}"
            )
            data = self._handle_response(response)
            return TaskStatus(**data)
        except Exception as e:
            raise APIError(f"Error in get_task_status: {str(e)}") from e

    def retrieve(self, index_id: str, query: str) -> Dict[str, Any]:
        try:
            response = self.session.post(
                f"{self.base_url}/index/retrieve",
                json={"index": index_id, "query": query},
            )
            return self._handle_response(response)
        except Exception as e:
            raise APIError(f"Error in retrieve: {str(e)}") from e

    def search(self, index_id: str, query: str) -> Dict[str, Any]:
        try:
            response = self.session.post(
                f"{self.base_url}/index/search",
                json={"index": index_id, "query": query},
            )
            return self._handle_response(response)
        except Exception as e:
            raise APIError(f"Error in search: {str(e)}") from e

    def delete_document(self, index_id: str, document_id: str) -> Dict[str, Any]:
        try:
            response = self.session.post(
                f"{self.base_url}/index/delete-document",
                json={"index": index_id, "document": document_id},
            )
            return self._handle_response(response)
        except Exception as e:
            raise APIError(f"Error in delete_document: {str(e)}") from e

    def create_instant_rag(self, context: str) -> InstantRagResponse:
        try:
            response = self.session.post(
                f"{self.base_url}/index/instant/create", json={"context": context}
            )
            data = self._handle_response(response)
            return InstantRagResponse(**data)
        except Exception as e:
            raise APIError(f"Error in create_instant_rag: {str(e)}") from e

    def query_instant_rag(self, index_id: str, query: str) -> InstantRagQueryResponse:
        try:
            response = self.session.post(
                f"{self.base_url}/index/instant/query",
                json={"index": index_id, "query": query},
            )
            data = self._handle_response(response)
            return InstantRagQueryResponse(**data)
        except Exception as e:
            raise APIError(f"Error in query_instant_rag: {str(e)}") from e

    def list_webhooks(self) -> WebhookListResponse:
        try:
            response = self.session.get(f"{self.base_url}/webhooks")
            data = self._handle_response(response)
            return data
        except Exception as e:
            raise APIError(f"Error in list_webhooks: {str(e)}") from e

    def create_webhook(
        self, url: str, name: str, secret: str, enabled: str
    ) -> WebhookResponse:
        try:
            logger.debug("Creating a new webhook.")
            payload = {
                "url": url,
                "name": name,
                "enabled": enabled,
                "secret": secret,
            }
            response = self.session.post(f"{self.base_url}/webhooks", json=payload)
            response_data = self._handle_response(response)
            return response_data.get('webhook')

        except Exception as e:
            logger.exception(f"Error in create_webhook: {str(e)}")
            raise APIError(f"Error in create_webhook: {str(e)}") from e

    def update_webhook(
        self, webhook_id: str, url: str, name: str, enabled: str
    ) -> WebhookResponse:
        try:
            payload = {
                "webhook_id": webhook_id,
                "url": url,
                "name": name,
                "enabled": enabled,
            }
            response = self.session.post(
                f"{self.base_url}/webhooks/update", json=payload
            )
            data = self._handle_response(response)
            return data
        except Exception as e:
            raise APIError(f"Error in update_webhook: {str(e)}") from e

    def delete_webhook(self, webhook_id: str) -> WebhookDeleteResponse:
        try:
            payload = {"webhook_id": webhook_id}
            response = self.session.post(
                f"{self.base_url}/webhooks/delete", json=payload
            )
            data = self._handle_response(response)
            return data
        except Exception as e:
            raise APIError(f"Error in delete_webhook: {str(e)}") from e
