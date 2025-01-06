import requests
from typing import List, Dict, Any, BinaryIO
from .exceptions import AuthenticationError, APIError
from .models import DocumentListResponse, TaskResponse, User, Index, Document, TaskStatus
import warnings
import urllib3


class IQSuiteClient:
    """
    Python client for the IQSuite API.

    Args:
        api_key (str): Your IQSuite API key
        base_url (str, optional): Base URL for the API. Defaults to production URL.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://iqsuite.test/api/v1",
        verify_ssl: bool = True,
        verbose: bool = False,
    ):
        """
        Initialize the IQSuite client.

        Args:
            api_key (str): Your IQSuite API key
            base_url (str, optional): Base URL for the API. Defaults to production URL.
            verify_ssl (bool, optional): Whether to verify SSL certificates.
                                         Set to False for testing with self-signed certificates.
                                         Default is True.
            verbose (bool, optional): Whether to suppress SSL verification warnings.
                                               Only applicable when verify_ssl is False.
                                               Default is False.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.verify = verify_ssl

        if not verify_ssl and not verbose:
            warnings.filterwarnings(
                "ignore", category=urllib3.exceptions.InsecureRequestWarning
            )

        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions"""
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
                return data["data"]

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
        """Get current user information"""
        response = self.session.get(f"{self.base_url}/user")
        data = self._handle_response(response)
        return User(**data)

    def list_indexes(self) -> List[Index]:
        """List all available indexes"""
        response = self.session.get(f"{self.base_url}/index")
        data = self._handle_response(response)
        return [Index(**index) for index in data]

    def get_documents(self, index_id: str) -> DocumentListResponse:
        """
        Get all documents from an index
        
        Args:
            index_id (str): ID of the index
            
        Returns:
            DocumentListResponse: Contains list of documents and index information
        """
        response = self.session.get(
            f"{self.base_url}/index/get-all-documents",
            params={'index': index_id}
        )
        data = self._handle_response(response)
        return DocumentListResponse(**data)

    def create_index(self, document: BinaryIO, filename: str) -> TaskResponse:
        """
        Create a new index with an initial document

        Args:
            document (BinaryIO): File object of the document
            filename (str): Name of the file

        Returns:
            TaskResponse: Object containing task_id, message and check_status URL
        """
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
        """
        Add a document to an existing index

        Args:
            index_id (str): ID of the index
            document (BinaryIO): File object of the document
            filename (str): Name of the file

        Returns:
            TaskResponse: Object containing task_id, message and check_status URL
        """
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
        """
        Check the status of a task

        Args:
            task_id (str): ID of the task
        """
        response = self.session.get(
            f"{self.base_url}/create-index/task-status/{task_id}"
        )
        data = self._handle_response(response)
        return TaskStatus(**data)

    def chat(self, index_id: str, query: str) -> Dict[str, Any]:
        """
        Chat with an index

        Args:
            index_id (str): ID of the index
            query (str): Query string
        """
        response = self.session.post(
            f"{self.base_url}/index/retrieve", json={"index": index_id, "query": query}
        )
        return self._handle_response(response)

    def search(self, index_id: str, query: str) -> Dict[str, Any]:
        """
        Perform hybrid search on an index

        Args:
            index_id (str): ID of the index
            query (str): Search query
        """
        response = self.session.post(
            f"{self.base_url}/index/search", json={"index": index_id, "query": query}
        )
        return self._handle_response(response)

    def delete_document(self, index_id: str, document_id: str) -> Dict[str, Any]:
        """
        Delete a document from an index

        Args:
            index_id (str): ID of the index
            document_id (str): ID of the document to delete
        """
        response = self.session.post(
            f"{self.base_url}/index/delete-document",
            json={"index": index_id, "document": document_id},
        )
        return self._handle_response(response)
