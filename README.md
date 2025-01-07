# IQSuite Python SDK

IQ Suite Platform is a powerful Retrieval Augmented Generation (RAG) and Hybrid Search service that allows you to:

- Create searchable document indices from PDF, images and word documents
- Perform hybrid search across your documents
- Chat with your documents using natural language
- Create instant RAG systems from text content
- Build production-ready document Q&A systems

The platform handles all the complexity of document processing, embedding generation, and vector search, allowing you to focus on building your application.

## Getting Started

### 1. Sign Up and Get Access Token

1. Visit [https://iqsuite.ai](https://iqsuite.ai)
2. Click "Sign Up" and create your account
3. After logging in, go to "API Keys" in your dashboard
4. Click "Create New API Key"
5. Copy your API key - you'll need this to use the SDK

### 2. Installation

#### Production Installation (PyPI)
```bash
pip install iqsuite
```

#### Development Installation (GitHub) (Only for internal testing)
```bash
pip install git+https://github.com/blue-hex/iqsuite-platform-py-sdk.git
```

### 3. Basic Setup

```python
from iqsuite import IQSuiteClient

client = IQSuiteClient('your-api-key')

# Or use custom base URL via environment variable
# IQSUITE_BASE_URL=https://custom.iqsuite.ai/api/v1
```

## Available APIs

The SDK provides two main types of functionality:

1. Document-based RAG Indices
   - Create indices from PDF, images and word documents
   - Add/remove documents
   - Chat in natural language
   - Perform hybrid search accross documents
   
2. Instant RAG
   - Create quick RAG systems from text content
   - Useful for smaller content (max 8000 tokens ≈ 32,000 characters)
   - Immediate availability (no processing time)

### Document-based RAG APIs

#### 1. Creating an Index

First, create an index with an initial document:

```python
# Create index with initial document
try:
    with open('document.pdf', 'rb') as f:
        task = client.create_index(f, 'document.pdf')
        print(f"Task ID: {task.task_id}")
        print(f"Status URL: {task.check_status}")

    # Poll for task completion (Optional)
    while True:
        status = client.get_task_status(task.task_id)
        print(f"Status: {status.status}")
        if status.status == 'completed':
            break
        elif status.status == 'failed':
            raise Exception("Index creation failed")
        time.sleep(5)  # Wait 5 seconds before checking again

except APIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

⚠️ Important: Document processing takes time. Always check task status before proceeding.

#### 2. Managing Documents

List all available indices:
```python
try:
    indices = client.list_indexes()
    for index in indices:
        print(f"Index ID: {index.id}")
        print(f"Name: {index.name}")
        print(f"Document Count: {index.document_count}")
except APIError as e:
    print(f"Error listing indices: {e}")
```

Add more documents to an existing index:
```python
try:
    with open('new_document.pdf', 'rb') as f:
        task = client.add_document(index_id, f, 'new_document.pdf')
        
    # Poll for completion
    while True:
        status = client.get_task_status(task.task_id)
        if status.status == 'completed':
            print("Document added successfully")
            break
        elif status.status == 'failed':
            raise Exception("Document addition failed")
        time.sleep(5)
        
except APIError as e:
    print(f"Error adding document: {e}")
```

List documents in an index:
```python
try:
    doc_list = client.get_documents(index_id)
    for doc in doc_list.documents:
        print(f"Document ID: {doc.id}")
        print(f"Created: {doc.created_at}")
except APIError as e:
    print(f"Error listing documents: {e}")
```

Delete a document:
```python
try:
    result = client.delete_document(index_id, document_id)
    print("Document deleted successfully")
except APIError as e:
    print(f"Error deleting document: {e}")
```

#### 3. Chatting and Searching

Chat with your documents:
```python
try:
    response = client.chat(
        index_id=index_id,
        query="What is the main topic of these documents?"
    )
    print(f"Response: {response}")
except APIError as e:
    print(f"Chat error: {e}")
```

Perform hybrid search:
```python
try:
    results = client.search(
        index_id=index_id,
        query="neural networks"
    )
    print(f"Search results: {results}")
except APIError as e:
    print(f"Search error: {e}")
```

### Instant RAG APIs

Instant RAG allows you to create quick RAG systems from text content without document processing delays.

#### 1. Creating Instant RAG

```python
try:
    # Create instant RAG from text
    context = """Your text content here... (max 8000 tokens)"""
    result = client.create_instant_rag(context)
    
    print(f"Instant RAG ID: {result.id}")
    print(f"Query URL: {result.query_url}")
    
except APIError as e:
    print(f"Error creating instant RAG: {e}")
```

#### 2. Querying Instant RAG

```python
try:
    # Query the instant RAG
    response = client.query_instant_rag(
        index_id=result.id,
        query="What is this text about?"
    )
    
    print(f"Response: {response.data.retrieval_response}")
    print(f"Tokens used: {response.data.total_tokens}")
    print(f"Credits cost: {response.data.credits_cost}")
    
except APIError as e:
    print(f"Error querying instant RAG: {e}")
```

## Error Handling

The SDK uses custom exceptions for better error handling:

- `AuthenticationError`: Raised when API key is invalid
- `APIError`: Raised for other API-related errors

Always wrap API calls in try-except blocks to handle potential errors gracefully.

## Best Practices

1. **Document Processing**
   - Always implement polling for task status
   - Use appropriate timeouts for your use case
   - Handle failure states appropriately

2. **Resource Management**
   - Properly close file handles using `with` statements
   - Delete unused indices and documents
   - Monitor token usage for instant RAG

3. **Error Handling**
   - Implement proper error handling for all API calls
   - Handle network errors and timeouts
   - Log errors appropriately in production

4. **Rate Limiting**
   - Implement appropriate delays between API calls
   - Handle rate limit errors gracefully
   - Consider implementing exponential backoff for retries

## Need Help?

- Visit [https://docs.iqsuite.ai/](https://docs.iqsuite.ai/) for detailed documentation
