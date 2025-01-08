# iQSuite Python SDK

iQ Suite Platform is a powerful Retrieval Augmented Generation as a service (RAGAAS) and Hybrid Search that allows you to:

- Create semantically and keyword-based searchable indices from unstructured sources such as PDF, Microsoft Word, PowerPoint and raw text chunks.
- Quickly perform vector-based semantic retrieval augmented generation with precision and persistent performance.
- Chat with your documents using natural language.
- Instantly extract insights from raw unstructured text chunks, emails, domain-specific text data code.
- Build production-ready document Q&A systems, natural-language-based analytics, key-value pair extractions, classifications, and etc.

The platform handles all the complexity of document processing, embedding generation, contextualized chunking, reranking and vector search, allowing you to focus on building your application.

## Getting Started

### Get API Key

1. Visit [iQ Suite Platform](https://iqsuite.ai)
2. Sign up with your emial or GitHub to create an account.
3. Once logged in, click on "API Keys" nav menu item in the sidebar, fill in API key name and click `Create API Key` to create a new key.
4. Copy the key and store it somewhere safe as **it'll not be shown again**.

### Installation

```bash
# From PyPI
pip install iqsuite
```

### Basic Setup

```python
import os
from iqsuite import IQSuiteClient
from iqsuite.exceptions import APIError, AuthenticationError

os.env["IQSUITE_API_KEY"]

client = IQSuiteClient(os.env["IQSUITE_API_KEY"])
```

## API Reference

### Get Current User

Retrieve information about the authenticated user. This is to ensure that you're successfully authenticated with iQ.

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

Create a new index with an initial document. Supports pdf, doc, docx, ppt, and pptx files.

```python
try:
    with open('document.pdf', 'rb') as f:
        response = client.create_index(f, 'document.pdf')
    print(f"Task ID: {response.data.task_id}")
    print(f"Status URL: {response.data.check_status}")
except APIError as e:
    print(f"Error: {e}")
```
> [!IMPORTANT]
> iQ's `create_index` method is an **asynchronous** process. Once submitted, iQ will respond with `task_id` and `check_status` URL to allow you to check the progress of the current indexing task. However, we recommend that you setup `webhooks` to ensure that your system is robust or maybe you can use our polling method `create_index_and_poll`, but this could create a blocking experience for your user, hence, dealer's choice!

### Webhooks
```
```

### Create Index with Polling

Create a new index with an initial document and wait for completion. This method handles the polling automatically and will return the `index_id` once the polling is completed.

```python
try:
    with open('document.pdf', 'rb') as f:
        response, status = client.create_index_and_poll(
            document=f,
            max_retries=6,      #  Maximum number of polling attempts
            poll_interval=20    #  Seconds between polling attempts
        )

    print(f"Task ID: {response.data.task_id}")
    print(f"Index ID: {response.data.index_id}")
    print(f"Final Status: {status.status}")

except APIError as e:
    print(f"Error: {e}")
```

### Add Document to Index

Add a new document to an existing index. (NOTE: We need an existing index with valid `index_id` to use this.)

```python
try:
    with open('new_document.docx', 'rb') as f:
        response = client.add_document(
            index_id='your-index-id',
            document=f,
        )
    print(f"Task ID: {response.data.task_id}")

except APIError as e:
    print(f"Error: {e}")
```

> [!IMPORTANT]
> Simlar to iQ's `create_index` method is, `add_document` method is also an **asynchronous** process. Once submitted, iQ will respond with `task_id` and `check_status` URL for you to check the progress of the current indexing task. However, we recommend that you setup `webhooks` to ensure that your system is robust or maybe you can use our polling method `add_document_and_poll`, but this could create a blocking experience for your user, hence once again, dealer's choice!


### Add Document to Index with Polling
Add a new document to an existing index. (NOTE: To use this function, you already should have an existing index.)

```python
try:
    with open('new_document.docx', 'rb') as f:
        response, status = client.add_document_and_poll(
            index_id='your-index-id',
            document=f,
            filename='new_document.docx',
            max_retries=6,      # Maximum number of polling attempts
            poll_interval=20    # Seconds between polling attempts
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
>[!IMPORTANT]
> Please note that deleting a document is irreversible process. 

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

Create an instant RAG system from raw text chunk (max 8000 tokens).

>[!IMPORTANT]
> `create_instant_rag` process is a sync/blocking process. Depending on the context length, it can take upto 30 seconds, and `instant_rag` doesn't work with our `Webhook` implementations.

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

Generate instant retrieval from `Instant RAG` index.

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

## Supported Document Types

The following document types are supported:

- PDF (.pdf)
- Microsoft Word (.doc, .docx)
- Microsoft PowerPoint (.ppt, .pptx)

## Error Handling

The SDK uses two main exception types:

- `AuthenticationError`: Invalid API key.
- `APIError`: Other API-related errors.

## Need more help?

- Please visit [Documentation](https://docs.iqsuite.ai/) for detailed documentation.

## Contact Us
- Please reach out to us at [iQ Support](mailto:support@iqsuite.ai) for any other help.