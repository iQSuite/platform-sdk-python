# IQSuite Python SDK

A Python SDK for interacting with the IQSuite API.

## Installation

```bash
pip install iqsuite  # From PyPI
# or
pip install git+https://github.com/blue-hex/iqsuite-platform-py-sdk.git  # From GitHub
```

## Quick Examples

```python
from iqsuite import IQSuiteClient

# Initialize (for development/testing)
client = IQSuiteClient('your-api-key', verify_ssl=False)

# Get user info
user = client.get_user()

# List all indexes
indexes = client.list_indexes()

# Create new index
with open('document.pdf', 'rb') as f:
    task = client.create_index(f, 'document.pdf')
    print(f"Task ID: {task.task_id}")

# Check task status
status = client.get_task_status(task.task_id)

# Add document to index
with open('new_document.pdf', 'rb') as f:
    task = client.add_document(index_id, f, 'new_document.pdf')

# Get all documents in an index
documents = client.get_documents(index_id)

# Chat with documents
response = client.chat(index_id, "What is machine learning?")

# Search documents
results = client.search(index_id, "neural networks")

# Delete a document
client.delete_document(index_id, document_id)
```

## Detailed Sample Snippets

```python
# Get user information
user = client.get_user()
print(f"Logged in as: {user.email}")

# List all indexes
indexes = client.list_indexes()
for index in indexes:
    print(f"Index: {index.id}")
```

### Creating a New Index

```python
# Create a new index with initial document
with open('document.pdf', 'rb') as f:
    task = client.create_index(f, 'document.pdf')
    print(f"Task ID: {task.task_id}")
    print(f"Message: {task.message}")
    print(f"Status URL: {task.check_status}")

    # Check task status
    status = client.get_task_status(task.task_id)
    print(f"Task status: {status.status}")
```

### Adding Documents to an Index

```python
# Add document to existing index
index_id = "your-index-id"  # Get this from list_indexes() or create_index()
with open('new_document.pdf', 'rb') as f:
    task = client.add_document(index_id, f, 'new_document.pdf')
    print(f"Task ID: {task.task_id}")
    print(f"Message: {task.message}")
    print(f"Status check URL: {task.check_status}")

    # Check task status
    status = client.get_task_status(task.task_id)
    print(f"Task status: {status.status}")
```

### Working with Documents and Search

```python
# Get all documents in an index
documents = client.get_documents(index_id)
for doc in documents:
    print(f"Document: {doc.filename}")

# Chat with your documents
response = client.chat(
    index_id=index_id,
    query="What is machine learning?"
)
print(f"Chat response: {response}")

# Search through documents
results = client.search(
    index_id=index_id,
    query="neural networks"
)
print(f"Search results: {results}")

# Delete a document
client.delete_document(
    index_id=index_id,
    document_id="document-id-to-delete"
)
```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/blue-hex/iqsuite-platform-py-sdk.git
cd iqsuite-platform-py-sdk
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Support

If you encounter any problems or have any questions, please:

1. Check the [GitHub Issues](https://github.com/blue-hex/iqsuite-platform-py-sdk/issues) for existing problems and solutions
2. Create a new issue if your problem is not already reported
3. Contact support for additional help