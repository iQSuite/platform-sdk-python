# IQSuite Python SDK

IQ Suite Platform is a powerful Retrieval Augmented Generation (RAG) and Hybrid Search service that allows you to:

- Create searchable document indices from PDF, images and word documents
- Perform hybrid search across your documents
- Chat with your documents using natural language
- Create instant RAG systems from text content
- Build production-ready document Q&A systems

The platform handles all the complexity of document processing, embedding generation, and vector search, allowing you to focus on building your application.

## Getting Started

### Sign Up for API Key

1. Visit [https://iqsuite.ai](https://iqsuite.ai)
2. Click "Sign Up" and create your account
3. Go to "API Keys" in your dashboard
4. Create a new API key

### Installation

```bash
# From PyPI
pip install iqsuite

# From GitHub (Only for internal testing)
pip install git+https://github.com/blue-hex/iqsuite-platform-py-sdk.git
```

### Basic Setup

```python
from iqsuite import IQSuiteClient
from iqsuite.exceptions import APIError, AuthenticationError

client = IQSuiteClient('your-api-key')

# Optional: Set custom base URL via parameter (Only for internal testing)
client = IQSuiteClient('your-api-key', base_url="https://staging.iqsuite.ai/api/v1")
```

## API Reference

### Get Current User

Retrieve information about the authenticated user.

```python
try:
    user = client.get_user()
    print(f"User ID: {user.id}")
    print(f"Email: {user.email}")
except AuthenticationError:
    print("Invalid API key")
except APIError as e:
    print(f"API Error: {e}")
```

### Create Index

Create a new index with an initial document. Supports PDF, DOC(X), and PPT(X) files.

```python
import time

try:
    with open('document.pdf', 'rb') as f:
        response = client.create_index(f, 'document.pdf')
    print(f"Task ID: {response.data.task_id}")
    print(f"Status URL: {response.data.check_status}")
except APIError as e:
    print(f"Error: {e}")
```

## Create Index with Polling

Create a new index with an initial document and wait for completion. This method handles the polling automatically.

```python
try:
    with open('document.pdf', 'rb') as f:
        response, status = client.create_index_and_poll(
            document=f,
            filename='document.pdf',
            max_retries=5,  # Optional: Maximum number of polling attempts
            poll_interval=5   # Optional: Seconds between polling attempts
        )

    print(f"Task ID: {response.data.task_id}")
    print(f"Final Status: {status.status}")

except APIError as e:
    print(f"Error: {e}")
```

### Add Document to Index

Add a new document to an existing index. (NOTE: To use this function, you already should have an existing index)

```python
try:
    with open('new_document.docx', 'rb') as f:
        response = client.add_document(
            index_id='your-index-id',
            document=f,
            filename='new_document.docx'
        )
    print(f"Task ID: {response.data.task_id}")

except APIError as e:
    print(f"Error: {e}")
```

## Add Document to Index with Polling
Add a new document to an existing index. (NOTE: To use this function, you already should have an existing index)

```python
try:
    with open('new_document.docx', 'rb') as f:
        response, status = client.add_document_and_poll(
            index_id='your-index-id',
            document=f,
            filename='new_document.docx',
            max_retries=5,  # Optional: Maximum number of polling attempts
            poll_interval=5   # Optional: Seconds between polling attempts
        )

    print(f"Task ID: {response.data.task_id}")
    print(f"Final Status: {status.status}")

except APIError as e:
    print(f"Error: {e}")
```

### List All Indices

Get a list of all available indices.

```python
try:
    indices = client.list_indexes()
    for index in indices:
        print(f"Index ID: {index.id}")
        print(f"Document Count: {index.document_count}")
except APIError as e:
    print(f"Error: {e}")
```

### Get Documents in Index

List all documents in a specific index.

```python
try:
    doc_list = client.get_documents('your_index_id')
    for doc in doc_list.data.documents:
        print(f"Document ID: {doc.id}")
    print(f"Index ID: {doc_list.data.index}")
except APIError as e:
    print(f"Error: {e}")
```

### Delete Document from Index

Remove a document from an index.

```python
try:
    result = client.delete_document(
        index_id='your-index-id',
        document_id='document-id-to-delete'
    )
    print("Document deleted successfully")
except APIError as e:
    print(f"Error: {e}")
```

### Chat with Documents

Ask questions about your documents in natural language.

```python
try:
    response = client.chat(
        index_id='your-index-id',
        query="What are the main points discussed?"
    )
    print(f"Response: {response}")
except APIError as e:
    print(f"Error: {e}")
```

### Search Documents

Perform hybrid semantic search across your documents.

```python
try:
    results = client.search(
        index_id='your-index-id',
        query="neural networks"
    )
    print(f"Search results: {results}")
except APIError as e:
    print(f"Error: {e}")
```

### Instant RAG

#### Create Instant RAG

Create a quick RAG system from text content (max 8000 tokens).

```python
try:
    context = "Your text content here... (max 8000 tokens)"
    response = client.create_instant_rag(context)

    print(f"Instant RAG ID: {response.data.id}")
    print(f"Query URL: {response.data.query_url}")
except APIError as e:
    print(f"Error: {e}")
```

#### Query Instant RAG

Ask questions about your instant RAG content.

```python
try:
    response = client.query_instant_rag(
        index_id='your-instant-rag-id',
        query="What is this text about?"
    )

    print(f"Response: {response.data.retrieval_response}")
    print(f"Tokens Used: {response.data.total_tokens}")
    print(f"Credits Cost: {response.data.credits_cost}")
except APIError as e:
    print(f"Error: {e}")
```

### Task Status

#### Check Task Status

Monitor the status of document processing tasks.

```python
try:
    status = client.get_task_status('your-task-id')
    print(f"Status: {status.status}")
except APIError as e:
    print(f"Error: {e}")

# Poll for task completion (Optional)
while True:
    status = client.get_task_status('your-task-id')
    print(f"Status: {status.status}")
    if status.status == 'completed':
        break
    elif status.status == 'failed':
        raise Exception("Index creation failed")
    time.sleep(5)  # Wait 5 seconds before checking again
```

## Supported Document Types

The following document types are supported:

- PDF (.pdf)
- Microsoft Word (.doc, .docx)
- Microsoft PowerPoint (.ppt, .pptx)

## Error Handling

The SDK uses two main exception types:

- `AuthenticationError`: Invalid API key
- `APIError`: Other API-related errors

## Need Help?

- Visit [https://docs.iqsuite.ai/](https://docs.iqsuite.ai/) for detailed documentation
