import requests
from typing import Optional, List, Dict, Any, BinaryIO
from .exceptions import AuthenticationError, APIError
from .models import User, Index, Document, TaskStatus

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
        verify_ssl: bool = True
    ):
        """
        Initialize the IQSuite client.
        
        Args:
            api_key (str): Your IQSuite API key
            base_url (str, optional): Base URL for the API. Defaults to production URL.
            verify_ssl (bool, optional): Whether to verify SSL certificates. 
                                       Set to False for testing with self-signed certificates.
                                       Default is True.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            raise APIError(
                f"HTTP {response.status_code} error: {str(e)}",
                status_code=response.status_code,
                response=response
            )
        except ValueError:
            raise APIError("Invalid JSON response from API")

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

    def get_documents(self, index_id: str) -> List[Document]:
        """
        Get all documents from an index
        
        Args:
            index_id (str): ID of the index
        """
        response = self.session.get(
            f"{self.base_url}/index/get-all-documents",
            params={'index': index_id}
        )
        data = self._handle_response(response)
        return [Document(**doc) for doc in data]

    def create_index(self, document: BinaryIO, filename: str) -> TaskStatus:
        """
        Create a new index with an initial document
        
        Args:
            document (BinaryIO): File object of the document
            filename (str): Name of the file
        """
        files = {
            'document': (filename, document, 'application/pdf')
        }
        response = self.session.post(
            f"{self.base_url}/index/create",
            files=files
        )
        data = self._handle_response(response)
        return TaskStatus(**data)

    def add_document(self, index_id: str, document: BinaryIO, filename: str) -> TaskStatus:
        """
        Add a document to an existing index
        
        Args:
            index_id (str): ID of the index
            document (BinaryIO): File object of the document
            filename (str): Name of the file
        """
        files = {
            'document': (filename, document, 'application/pdf')
        }
        response = self.session.post(
            f"{self.base_url}/index/add-document",
            data={'index': index_id},
            files=files
        )
        data = self._handle_response(response)
        return TaskStatus(**data)

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
            f"{self.base_url}/index/retrieve",
            json={
                'index': index_id,
                'query': query
            }
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
            f"{self.base_url}/index/search",
            json={
                'index': index_id,
                'query': query
            }
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
            json={
                'index': index_id,
                'document': document_id
            }
        )
        return self._handle_response(response)