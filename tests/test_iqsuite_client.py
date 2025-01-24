import pytest
import requests
from unittest.mock import patch, MagicMock
from io import BytesIO
from iqsuite.client import IQSuiteClient
from iqsuite.exceptions import AuthenticationError, APIError
from iqsuite.models import (
    User,
    Index,
    TaskResponse,
    TaskStatus,
    DocumentListResponse,
    InstantRagResponse,
    InstantRagQueryResponse,
    WebhookDeleteResponse,
    WebhookListResponse,
    WebhookResponse,
)


API_KEY = "iq-DPV8hP3oxbbu8i2jzA7Qvkrl9QWhymNm0CcJ329Le77f6e13"
BASE_URL = "https://staging.iqsuite.ai/api/v1"


@pytest.fixture
def client():
    return IQSuiteClient(api_key=API_KEY, base_url=BASE_URL)


def mock_response(status=200, json_data=None, raise_for_status=None):
    mock_resp = MagicMock()
    mock_resp.status_code = status
    mock_resp.json.return_value = json_data
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    else:
        mock_resp.raise_for_status = MagicMock()
    return mock_resp


def test_init(client):
    assert client.api_key == API_KEY
    assert client.base_url == BASE_URL
    assert client.session.headers["Authorization"] == f"Bearer {API_KEY}"
    assert client.session.headers["Accept"] == "application/json"
    assert client.session.headers["Content-Type"] == "application/json"


# Test get_user
@patch("requests.Session.get")
def test_get_user_success(mock_get, client):
    user_data = {
        "id": 2,
        "name": "admin",
        "email": "admin@localhost.com",
        "email_verified_at": "2025-01-18T06:21:43.000000Z",
        "created_at": "2025-01-06T18:36:42.000000Z",
        "updated_at": "2025-01-18T06:21:43.000000Z",
        "notification_channels": ["webhook"],
    }
    mock_get.return_value = mock_response(json_data={"data": user_data})

    user = client.get_user()
    print(user)
    assert isinstance(user, User)
    mock_get.assert_called_once_with(f"{BASE_URL}/user")


@patch("requests.Session.get")
def test_get_user_api_error(mock_get, client):
    mock_get.return_value = mock_response(
        status=400, json_data={"error": "Bad Request"}
    )

    with pytest.raises(APIError) as exc_info:
        client.get_user()
    assert "API error: Bad Request" in str(exc_info.value)
    mock_get.assert_called_once_with(f"{BASE_URL}/user")


# Test list_indexes
@patch("requests.Session.get")
def test_list_indexes_success(mock_get, client):
    indexes_data = [
        {"id": "index_1", "name": "Index One"},
        {"id": "index_2", "name": "Index Two"},
    ]
    mock_get.return_value = mock_response(json_data={"data": indexes_data})

    indexes = client.list_indexes()
    assert isinstance(indexes, list)
    assert len(indexes) == 2
    assert indexes[0].id == "index_1"
    assert indexes[0].name == "Index One"
    mock_get.assert_called_once_with(f"{BASE_URL}/index")


@patch("requests.Session.get")
def test_list_indexes_api_error(mock_get, client):
    mock_get.return_value = mock_response(
        status=500, json_data={"error": "Server Error"}
    )

    with pytest.raises(APIError) as exc_info:
        client.list_indexes()
    assert "API error: Server Error" in str(exc_info.value)
    mock_get.assert_called_once_with(f"{BASE_URL}/index")


# Test get_documents
@patch("requests.Session.get")
def test_get_documents_success(mock_get, client):
    documents_data = {
        "documents": [
            {"id": "doc1", "title": "Document 1", "content": "Content 1"},
            {"id": "doc2", "title": "Document 2", "content": "Content 2"},
        ],
        "index": "54a7e942-366b-42d2-9672-69fc460c2752",
        "total": 2,
        "page": 1,
        "per_page": 10,
    }
    mock_get.return_value = mock_response(json_data={"data": documents_data})

    response = client.get_documents("54a7e942-366b-42d2-9672-69fc460c2752")
    assert isinstance(response, DocumentListResponse)
    assert len(response.data.documents) == 2
    assert response.data.documents[0].id == "doc1"
    mock_get.assert_called_once_with(
        f"{BASE_URL}/index/get-all-documents",
        params={"index": "54a7e942-366b-42d2-9672-69fc460c2752"},
    )


@patch("requests.Session.get")
def test_get_documents_api_error(mock_get, client):
    mock_get.return_value = mock_response(
        status=404, json_data={"error": "Not Found"}
    )

    with pytest.raises(APIError) as exc_info:
        client.get_documents("invalid_index")
    assert "API error: Not Found" in str(exc_info.value)
    mock_get.assert_called_once_with(
        f"{BASE_URL}/index/get-all-documents", params={"index": "invalid_index"}
    )


# Test create_index
@patch("requests.Session.post")
def test_create_index_success(mock_post, client):
    task_response_data = {
        "task_id": "task_123",
        "message": "Index creation started",
        "check_status": "pending"
    }
    mock_post.return_value = mock_response(json_data={"data": task_response_data})

    document = BytesIO(b"Dummy PDF content")
    filename = "document.pdf"

    task_response = client.create_index(document, filename)
    assert isinstance(task_response, TaskResponse)
    assert task_response.data.task_id == "task_123"
    assert task_response.data.message == "Index creation started"
    assert task_response.data.check_status == "pending"

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == f"{BASE_URL}/index/create"
    assert "files" in kwargs
    assert kwargs["files"]["document"][0] == filename


@patch("requests.Session.post")
def test_create_index_unsupported_file_type(mock_post, client):
    document = BytesIO(b"Dummy content")
    filename = "document.exe"

    with pytest.raises(APIError) as exc_info:
        client.create_index(document, filename)
    assert "Unsupported file type" in str(exc_info.value)
    mock_post.assert_not_called()


@patch("requests.Session.post")
def test_create_index_api_error(mock_post, client):
    mock_post.return_value = mock_response(
        status=400, json_data={"error": "Invalid Document"}
    )

    document = BytesIO(b"Dummy PDF content")
    filename = "document.pdf"

    with pytest.raises(APIError) as exc_info:
        client.create_index(document, filename)
    assert "API error: Invalid Document" in str(exc_info.value)
    mock_post.assert_called_once()


# Test add_document
@patch("requests.Session.post")
def test_add_document_success(mock_post, client):
    task_response_data = {
        "task_id": "task_456",
        "message": "Document addition started",
        "check_status": "pending"
    }
    mock_post.return_value = mock_response(json_data={"data": task_response_data})

    index_id = "index_123"
    document = BytesIO(b"Dummy DOCX content")
    filename = "document.docx"

    task_response = client.add_document(index_id, document, filename)
    assert isinstance(task_response, TaskResponse)
    assert task_response.data.task_id == "task_456"
    assert task_response.data.message == "Document addition started"
    assert task_response.data.check_status == "pending"

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == f"{BASE_URL}/index/add-document"
    assert kwargs["data"]["index"] == index_id
    assert kwargs["files"]["document"][0] == filename


@patch("requests.Session.post")
def test_add_document_unsupported_file_type(mock_post, client):
    index_id = "index_123"
    document = BytesIO(b"Dummy content")
    filename = "image.gif"

    with pytest.raises(APIError) as exc_info:
        client.add_document(index_id, document, filename)
    assert "Unsupported file type" in str(exc_info.value)
    mock_post.assert_not_called()



# Test get_task_status
@patch("requests.Session.get")
def test_get_task_status_success(mock_get, client):
    task_status_data = {"status": "completed"}
    mock_get.return_value = mock_response(json_data={"data": task_status_data})

    task_id = "task_123"
    status = client.get_task_status(task_id)
    assert isinstance(status, TaskStatus)
    assert status.status == "completed"

    mock_get.assert_called_once_with(f"{BASE_URL}/create-index/task-status/{task_id}")


@patch("requests.Session.get")
def test_get_task_status_api_error(mock_get, client):
    mock_get.return_value = mock_response(
        status=404, json_data={"error": "Task Not Found"}
    )

    with pytest.raises(APIError) as exc_info:
        client.get_task_status("invalid_task")
    assert "API error: Task Not Found" in str(exc_info.value)
    mock_get.assert_called_once_with(
        f"{BASE_URL}/create-index/task-status/invalid_task"
    )


# Test create_index_and_poll
@patch("requests.Session.post")
@patch("requests.Session.get")
def test_create_index_and_poll_success(mock_get, mock_post, client):
    task_response_data = {
        "task_id": "task_789",
        "message": "Index creation started",
        "check_status": "pending"
    }
    mock_post.return_value = mock_response(json_data={"data": task_response_data})
    task_status_data = {"status": "completed"}
    mock_get.return_value = mock_response(json_data={"data": task_status_data})

    document = BytesIO(b"Dummy PDF content")
    filename = "document.pdf"

    response, status = client.create_index_and_poll(document, filename)
    assert response.data.task_id == "task_789"
    assert status.status == "completed"

    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/create",
        files={"document": (filename, document, "application/pdf")}
    )
    mock_get.assert_called_once_with(f"{BASE_URL}/create-index/task-status/task_789")


@patch("requests.Session.post")
@patch("requests.Session.get")
def test_create_index_and_poll_failure(mock_get, mock_post, client):
    task_response_data = {
        "task_id": "task_789",
        "message": "Index creation started",
        "check_status": "pending"
    }
    mock_post.return_value = mock_response(json_data={"data": task_response_data})
    task_status_data = {"status": "failed"}
    mock_get.return_value = mock_response(json_data={"data": task_status_data})

    document = BytesIO(b"Dummy PDF content")
    filename = "document.pdf"

    with pytest.raises(APIError) as exc_info:
        client.create_index_and_poll(document, filename)
    assert "Task failed with status: failed" in str(exc_info.value)

    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/create",
        files={"document": (filename, document, "application/pdf")}
    )
    mock_get.assert_called_once_with(f"{BASE_URL}/create-index/task-status/task_789")


@patch("requests.Session.post")
@patch("requests.Session.get")
def test_create_index_and_poll_max_retries(mock_get, mock_post, client):
    task_response_data = {
        "task_id": "task_789",
        "message": "Index creation started",
        "check_status": "pending"
    }
    mock_post.return_value = mock_response(json_data={"data": task_response_data})
    task_status_data = {"status": "pending"}
    mock_get.return_value = mock_response(json_data={"data": task_status_data})

    document = BytesIO(b"Dummy PDF content")
    filename = "document.pdf"

    with patch("time.sleep", return_value=None):
        with pytest.raises(APIError) as exc_info:
            client.create_index_and_poll(
                document, filename, max_retries=3, poll_interval=0
            )
    assert "Maximum retries (3) reached while polling task status" in str(
        exc_info.value
    )

    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/create",
        files={"document": (filename, document, "application/pdf")}
    )
    assert mock_get.call_count == 3


# Test add_document_and_poll
@patch("requests.Session.post")
@patch("requests.Session.get")
def test_add_document_and_poll_success(mock_get, mock_post, client):
    task_response_data = {
        "task_id": "task_456",
        "message": "Document addition started",
        "check_status": "pending"
    }
    mock_post.return_value = mock_response(json_data={"data": task_response_data})
    task_status_data_pending = {"status": "pending"}
    task_status_data_completed = {"status": "completed"}
    mock_get.side_effect = [
        mock_response(json_data={"data": task_status_data_pending}),
        mock_response(json_data={"data": task_status_data_completed}),
    ]

    index_id = "index_123"
    document = BytesIO(b"Dummy DOCX content")
    filename = "document.docx"

    with patch("time.sleep", return_value=None):
        response, status = client.add_document_and_poll(
            index_id, document, filename, max_retries=5, poll_interval=0
        )
    assert response.data.task_id == "task_456"
    assert status.status == "completed"

    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/add-document",
        data={"index": index_id},
        files={"document": (filename, document, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    )
    assert mock_get.call_count == 2


@patch("requests.Session.post")
@patch("requests.Session.get")
def test_add_document_and_poll_failure(mock_get, mock_post, client):
    task_response_data = {
        "task_id": "task_456",
        "message": "Document addition started",
        "check_status": "pending"
    }
    mock_post.return_value = mock_response(json_data={"data": task_response_data})
    task_status_data = {"status": "failed"}
    mock_get.return_value = mock_response(json_data={"data": task_status_data})

    index_id = "index_123"
    document = BytesIO(b"Dummy DOCX content")
    filename = "document.docx"

    with patch("time.sleep", return_value=None):
        with pytest.raises(APIError) as exc_info:
            client.add_document_and_poll(index_id, document, filename)
    assert "Task failed with status: failed" in str(exc_info.value)

    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/add-document",
        data={"index": index_id},
        files={"document": (filename, document, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    )
    mock_get.assert_called_once_with(f"{BASE_URL}/create-index/task-status/task_456")


# Test retrieve
@patch("requests.Session.post")
def test_retrieve_success(mock_post, client):
    retrieve_data = {"result": "Some retrieved data"}
    mock_post.return_value = mock_response(json_data={"data": retrieve_data})

    index_id = "index_123"
    query = "sample query"
    document_id = "doc_456"

    response = client.retrieve(index_id, query, document_id)
    assert response == retrieve_data

    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/retrieve",
        json={
            "index": index_id,
            "query": query,
            "document_id": document_id,
        },
    )


@patch("requests.Session.post")
def test_retrieve_optional_document_id(mock_post, client):
    retrieve_data = {"result": "Some retrieved data"}
    mock_post.return_value = mock_response(json_data={"data": retrieve_data})

    index_id = "index_123"
    query = "sample query"
    document_id = ""

    response = client.retrieve(index_id, query, document_id)
    assert response == retrieve_data

    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/retrieve",
        json={
            "index": index_id,
            "query": query,
            "document_id": "",
        },
    )


@patch("requests.Session.post")
def test_retrieve_api_error(mock_post, client):
    mock_post.return_value = mock_response(
        status=401, json_data={"error": "Unauthorized"}
    )

    with pytest.raises(APIError) as exc_info:
        client.retrieve("index_123", "query", "doc_456")
    assert "API error: Unauthorized" in str(exc_info.value)
    mock_post.assert_called_once()


# Test search
@patch("requests.Session.post")
def test_search_success(mock_post, client):
    search_data = {"results": ["result1", "result2"]}
    mock_post.return_value = mock_response(json_data={"data": search_data})

    index_id = "index_123"
    query = "search query"

    response = client.search(index_id, query)
    assert response == search_data

    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/search",
        json={"index": index_id, "query": query},
    )


@patch("requests.Session.post")
def test_search_api_error(mock_post, client):
    mock_post.return_value = mock_response(
        status=500, json_data={"error": "Server Error"}
    )

    with pytest.raises(APIError) as exc_info:
        client.search("index_123", "query")
    assert "API error: Server Error" in str(exc_info.value)
    mock_post.assert_called_once()


# Test delete_document
@patch("requests.Session.post")
def test_delete_document_success(mock_post, client):
    delete_data = {"status": "deleted"}
    mock_post.return_value = mock_response(json_data={"data": delete_data})

    index_id = "index_123"
    document_id = "doc_456"

    response = client.delete_document(index_id, document_id)
    assert response == delete_data

    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/delete-document",
        json={"index": index_id, "document": document_id},
    )


@patch("requests.Session.post")
def test_delete_document_api_error(mock_post, client):
    mock_post.return_value = mock_response(
        status=400, json_data={"error": "Document Not Found"}
    )

    with pytest.raises(APIError) as exc_info:
        client.delete_document("index_123", "invalid_doc")
    assert "API error: Document Not Found" in str(exc_info.value)
    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/delete-document",
        json={"index": "index_123", "document": "invalid_doc"},
    )


# Test create_instant_rag
@patch("requests.Session.post")
def test_create_instant_rag_success(mock_post, client):
    rag_data = {
        "message": "Instant RAG created",
        "id": "rag_123",
        "context": "Sample context",
        "query_url": "https://example.com/query"
    }
    mock_post.return_value = mock_response(json_data={"data": rag_data})

    context = "Sample context"

    response = client.create_instant_rag(context)
    assert isinstance(response, InstantRagResponse)
    assert response.message == "Instant RAG created"
    assert response.id == "rag_123"
    assert response.context == "Sample context"
    assert response.query_url == "https://example.com/query"

    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/instant/create",
        json={"context": context},
    )


@patch("requests.Session.post")
def test_create_instant_rag_api_error(mock_post, client):
    mock_post.return_value = mock_response(
        status=400, json_data={"error": "Invalid Context"}
    )

    with pytest.raises(APIError) as exc_info:
        client.create_instant_rag("")
    assert "API error: Invalid Context" in str(exc_info.value)
    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/instant/create",
        json={"context": ""},
    )


# Test query_instant_rag
@patch("requests.Session.post")
def test_query_instant_rag_success(mock_post, client):
    query_data = {
        "uuid": "uuid_123",
        "total_tokens": 150,
        "answer": "Sample response",
        "source_documents": [
            {"id": "doc1", "file_name": "document1.pdf"},
            {"id": "doc2", "file_name": "document2.pdf"}
        ]
    }
    mock_post.return_value = mock_response(json_data={"data": query_data})

    index_id = "rag_123"
    query = "Sample query"

    response = client.query_instant_rag(index_id, query)
    assert isinstance(response, InstantRagQueryResponse)
    assert response.uuid == "uuid_123"
    assert response.total_tokens == 150
    assert response.answer == "Sample response"
    assert len(response.source_documents) == 2
    assert response.source_documents[0].id == "doc1"
    assert response.source_documents[0].file_name == "document1.pdf"

    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/instant/query",
        json={"index": index_id, "query": query},
    )


@patch("requests.Session.post")
def test_query_instant_rag_api_error(mock_post, client):
    mock_post.return_value = mock_response(
        status=500, json_data={"error": "Server Error"}
    )

    with pytest.raises(APIError) as exc_info:
        client.query_instant_rag("rag_123", "query")
    assert "API error: Server Error" in str(exc_info.value)
    mock_post.assert_called_once_with(
        f"{BASE_URL}/index/instant/query",
        json={"index": "rag_123", "query": "query"},
    )


# Test list_webhooks
@patch("requests.Session.get")
def test_list_webhooks_success(mock_get, client):
    webhooks_data = [
        {
            "id": 2,
            "name": "testing_1",
            "url": "https://iqsuite.test",
            "enabled": True,
            "created_at": "2025-01-09T09:09:29.000000Z",
            "updated_at": "2025-01-09T09:09:29.000000Z",
            "secret": "secret1",
        },
        {
            "id": 6,
            "name": "Processing Events",
            "url": "https://test.com/webhook",
            "enabled": True,
            "created_at": "2025-01-09T12:33:22.000000Z",
            "updated_at": "2025-01-09T12:33:22.000000Z",
        },
    ]
    mock_get.return_value = mock_response(json_data={"data": webhooks_data})

    response = client.list_webhooks()
    assert isinstance(response, WebhookListResponse)
    assert len(response.data) == 2
    assert response.data[0].id == 2
    assert response.data[0].name == "testing_1"
    assert response.data[0].url == "https://iqsuite.test"
    assert response.data[0].enabled is True

    mock_get.assert_called_once_with(f"{BASE_URL}/webhooks")

@patch("requests.Session.get")
def test_list_webhooks_api_error(mock_get, client):
    mock_get.return_value = mock_response(
        status=401, json_data={"error": "Unauthorized"}
    )

    with pytest.raises(APIError) as exc_info:
        client.list_webhooks()
    assert "API error: Unauthorized" in str(exc_info.value)
    mock_get.assert_called_once_with(f"{BASE_URL}/webhooks")


# Test create_webhook
@patch("requests.Session.post")
def test_create_webhook_success(mock_post, client):
    webhook_response_data = {
        "webhook": {
            "id": 123,
            "url": "https://example.com/webhook",
            "name": "Test Webhook",
            "enabled": True,
            "secret": "secret_key",
            "created_at": "2025-01-05T12:00:00Z",
            "updated_at": "2025-01-06T12:00:00Z",
        }
    }
    mock_post.return_value = mock_response(json_data={"data": webhook_response_data})

    url = "https://example.com/webhook"
    name = "Test Webhook"
    secret = "secret_key"
    enabled = "true"

    response = client.create_webhook(url, name, secret, enabled)
    assert isinstance(response, WebhookResponse)
    assert response.webhook.id == 123
    assert response.webhook.url == "https://example.com/webhook"
    assert response.webhook.name == "Test Webhook"
    assert response.webhook.enabled is True
    assert response.webhook.secret == "secret_key"
    mock_post.assert_called_once_with(
        f"{BASE_URL}/webhooks",
        json={
            "url": url,
            "name": name,
            "enabled": enabled,
            "secret": secret,
        },
    )

@patch("requests.Session.post")
def test_create_webhook_api_error(mock_post, client):
    mock_post.return_value = mock_response(
        status=400, json_data={"error": "Invalid URL"}
    )

    with pytest.raises(APIError) as exc_info:
        client.create_webhook("", "name", "secret", "true")
    assert "API error: Invalid URL" in str(exc_info.value)
    mock_post.assert_called_once_with(
        f"{BASE_URL}/webhooks",
        json={
            "url": "",
            "name": "name",
            "enabled": "true",
            "secret": "secret",
        },
    )



@patch("requests.Session.post")
def test_update_webhook_api_error(mock_post, client):
    mock_post.return_value = mock_response(
        status=404, json_data={"error": "Webhook Not Found"}
    )

    with pytest.raises(APIError) as exc_info:
        client.update_webhook("invalid_wh", "url", "name", "true")
    assert "API error: Webhook Not Found" in str(exc_info.value)
    mock_post.assert_called_once_with(
        f"{BASE_URL}/webhooks/update",
        json={
            "webhook_id": "invalid_wh",
            "url": "url",
            "name": "name",
            "enabled": "true",
        },
    )


# Test delete_webhook
@patch("requests.Session.post")
def test_delete_webhook_success(mock_post, client):
    delete_response_data = {"message": "Webhook deleted."}
    mock_post.return_value = mock_response(json_data={"data": delete_response_data})

    webhook_id = "wh_123"

    response = client.delete_webhook(webhook_id)
    assert isinstance(response, WebhookDeleteResponse)
    assert response.data["message"] == "Webhook deleted."

    mock_post.assert_called_once_with(
        f"{BASE_URL}/webhooks/delete",
        json={"webhook_id": webhook_id},
    )


@patch("requests.Session.post")
def test_delete_webhook_success(mock_post, client):
    delete_response_data = {"message": "Webhook deleted."}
    mock_post.return_value = mock_response(json_data={"data": delete_response_data})

    webhook_id = "wh_123"

    response = client.delete_webhook(webhook_id)
    assert isinstance(response, WebhookDeleteResponse)
    assert response.data["message"] == "Webhook deleted."

    mock_post.assert_called_once_with(
        f"{BASE_URL}/webhooks/delete",
        json={"webhook_id": webhook_id},
    )
