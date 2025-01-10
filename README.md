# iQ Suite Python SDK

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/iqsuite/iqsuite-python)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/iqsuite)](https://pypi.org/project/iqsuite/)
[![CI](https://github.com/iqsuite/iqsuite-python/actions/workflows/ci.yml/badge.svg)](https://github.com/iqsuite/iqsuite-python/actions/workflows/ci.yml)

## Overview

Welcome to the **iQ Suite Python SDK**! This Software Development Kit (SDK) allows you to seamlessly integrate with the **iQ Suite Platform**, a comprehensive Retrieval Augmented Generation as a Service (RAGaaS). Whether you're a seasoned developer or just starting your coding journey, this guide will help you harness the power of iQ Suite to enhance your applications with advanced search and data processing capabilities.

### What is Retrieval Augmented Generation (RAG)?

**Retrieval Augmented Generation (RAG)** is a powerful approach that combines traditional information retrieval techniques with advanced language models. It enables applications to fetch relevant information from large datasets and generate insightful, contextually accurate responses. In simpler terms, RAG helps your applications understand and process data more intelligently, providing users with precise and meaningful answers based on the content they interact with.

### Key Features

- **Multi-Format Document Support:** Easily handle PDFs, Word documents, PowerPoint presentations, and raw text.
- **Hybrid Semantic Search:** Combine keyword searches with semantic understanding for more accurate results.
- **Natural Language Interaction:** Engage with your documents through conversational queries.
- **Instant RAG:** Perform on-the-fly analysis without the need for persistent indexing.
- **Asynchronous Processing:** Manage tasks efficiently using webhooks.
- **Real-Time Notifications:** Receive immediate updates on task statuses.
- **Secure API Authentication:** Protect your data with robust authentication mechanisms.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Authentication](#authentication)
  - [Document-based RAG](#document-based-rag)
    - [Create Index](#create-index)
    - [Create Index with Polling](#create-index-with-polling)
    - [Add Document to Index](#add-document-to-index)
    - [Add Document with Polling](#add-document-with-polling)
    - [List Indices](#list-indices)
    - [List Documents](#list-documents)
    - [Delete Document](#delete-document)
    - [Retrieve](#retrieve)
    - [Search](#search)
    - [Task Status](#task-status)
  - [Instant RAG](#instant-rag)
    - [Create Instant RAG](#create-instant-rag)
    - [Query Instant RAG](#query-instant-rag)
  - [Webhooks](#webhooks)
    - [Create Webhook](#create-webhook)
    - [List Webhooks](#list-webhooks)
    - [Update Webhook](#update-webhook)
    - [Delete Webhook](#delete-webhook)
- [Supported Documents](#supported-documents)
- [Error Handling](#error-handling)
- [Support](#support)
- [License](#license)

## Installation

Installing the iQ Suite Python SDK is straightforward. Follow the steps below to get started.

### Prerequisites

- **Python Version:** Ensure you have Python 3.6 or higher installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).
- **pip:** Python's package installer should be available. It's typically included with Python installations.

### Steps to Install

1. **Open Your Terminal or Command Prompt:**

   - **Windows:** Press `Win + R`, type `cmd`, and hit `Enter`.
   - **macOS/Linux:** Open the Terminal application.

2. **Install the SDK Using pip:**

   Enter the following command and press `Enter`:

   ```bash
   pip install iqsuite
   ```

   This command downloads and installs the latest version of the iQ Suite Python SDK from the Python Package Index (PyPI).

3. **Verify Installation:**

   To ensure the SDK was installed correctly, you can try importing it in a Python shell:

   ```python
   import iqsuite
   print(iqsuite.__version__)
   ```

   If no errors occur and the version number is displayed, the installation was successful.

## Features

The iQ Suite Python SDK offers a wide range of features designed to make data retrieval and processing efficient and effective. Here's a detailed look at what you can do:

- 📄 **Multi-Format Document Support:** Easily ingest and process various document types, including PDFs, Word documents, PowerPoint presentations, and raw text files.

- 🔍 **Hybrid Semantic Search:** Combines traditional keyword-based search with advanced semantic understanding to deliver more accurate and relevant search results.

- 💬 **Natural Language Chat:** Interact with your documents using conversational queries, making data exploration intuitive and user-friendly.

- 🚀 **Instant RAG:** Perform immediate analysis on your data without the need to create and maintain persistent indices.

- 🔄 **Asynchronous Processing:** Handle long-running tasks efficiently using webhooks, allowing your application to remain responsive.

- ⚡ **Real-Time Notifications:** Receive instant updates on the status of your tasks, ensuring you're always informed about ongoing processes.

- 🔒 **Secure API Authentication:** Protect your data and ensure secure interactions with robust API key management.

## Quick Start

This section will guide you through the initial steps to get your application up and running with the iQ Suite Python SDK. Whether you're setting up for the first time or integrating it into an existing project, these instructions will help you get started quickly.

### Step 1: Obtain Your API Key

Before you can interact with the iQ Suite Platform, you'll need an API key. This key authenticates your requests and ensures secure access to your data.

> **⚠️ Important:** *Never expose your API key in version control systems (like GitHub) or unsecured environments. Always use environment variables or secure key management systems to store your API keys.*

#### How to Get Your API Key

1. **Visit the iQ Suite Platform:**

   Open your web browser and navigate to the [iQ Suite Platform](https://iqsuite.ai).

2. **Sign Up or Log In:**

   - **New Users:** Click on the **Sign Up** button and create an account using your email address or GitHub account.
   - **Existing Users:** Click on **Log In** and enter your credentials.

3. **Navigate to API Keys:**

   Once logged in, locate the **API Keys** section in the sidebar menu. This section manages all your API keys.

4. **Create a New API Key:**

   - Click on the **Create API Key** button.
   - Provide a **name** for your API key (e.g., "Development Key" or "Production Key") to help you identify its purpose.
   - Click **Create**.

5. **Store Your API Key Securely:**

   - After creation, the API key will be displayed **only once**. Make sure to **copy and save** it in a secure location.
   - **Do not** share your API key publicly or commit it to version control repositories.

### Step 2: Initialize the Client

With your API key in hand, you can now initialize the iQ Suite client in your Python application.

#### Using Environment Variables (Recommended)

Storing your API key in an environment variable enhances security by keeping sensitive information out of your codebase.

1. **Set the Environment Variable:**

   - **Windows:**

     ```bash
     set IQSUITE_API_KEY=your_api_key_here
     ```

   - **macOS/Linux:**

     ```bash
     export IQSUITE_API_KEY=your_api_key_here
     ```

2. **Initialize the Client in Python:**

   ```python
   import os
   from iqsuite import IQSuiteClient
   from iqsuite.exceptions import APIError, AuthenticationError

   # Retrieve the API key from environment variables
   api_key = os.getenv("IQSUITE_API_KEY")

   # Initialize the iQ Suite client
   client = IQSuiteClient(api_key)
   ```

### Step 3: Verify Your Setup

Ensure that your client is correctly authenticated by fetching your user details.

```python
try:
    user = client.get_user()
    print(f"Authenticated as: {user.email}")
except AuthenticationError:
    print("Authentication failed: Invalid API key.")
except APIError as e:
    print(f"API Error: {e}")
```

- **Expected Output:**

  If the API key is valid, you'll see an output similar to:

  ```
  Authenticated as: your_email@example.com
  ```

- **Error Handling:**

  - **AuthenticationError:** Indicates an invalid or expired API key.
  - **APIError:** Covers other API-related issues, such as server errors.

## Usage

The iQ Suite Python SDK offers a variety of functionalities to help you interact with the iQ Suite Platform effectively. This section provides detailed instructions and examples to guide you through different use cases, ensuring that even those new to coding can implement these features with ease.

### Authentication

Before accessing any of the platform's features, you must authenticate using your API key. This process ensures that your requests are secure and authorized.

#### Example: Retrieve Current User Information

This example demonstrates how to verify your authentication by fetching details about the currently authenticated user.

```python
try:
    # Attempt to retrieve the authenticated user's information
    user = client.get_user()
    print(f"Authenticated as: {user.email}")
except AuthenticationError:
    # Handle invalid or expired API keys
    print("Authentication failed: Invalid API key.")
except APIError as e:
    # Handle other API-related errors
    print(f"API Error: {e}")
```

**Explanation:**

- **client.get_user():** Sends a request to the iQ Suite Platform to retrieve information about the authenticated user.
- **AuthenticationError:** Catches errors related to invalid or expired API keys.
- **APIError:** Catches other general API errors.

**Output:**

If successful, the script will print the authenticated user's email address. Otherwise, it will display an appropriate error message.

### Document-based RAG

Document-based RAG involves creating indices from your documents and performing operations like searching, retrieving content, and managing documents within these indices. This section guides you through the various operations you can perform.

#### Create Index

Creating an index allows the platform to process and understand your documents, enabling advanced search and retrieval capabilities.

> **ℹ️ Information:** *Creating an index is an asynchronous operation. This means the process runs in the background, and you'll receive a task ID to monitor its progress.*

##### Example: Create a New Index from a Document

```python
# Open the document you want to index in binary read mode
with open('document.pdf', 'rb') as file:
    # Send a request to create an index with the provided document
    response = client.create_index(document=file, filename='document.pdf')
    # Print the received Task ID to monitor progress
    print(f"Task ID: {response.data.task_id}")
```

**Explanation:**

- **open('document.pdf', 'rb'):** Opens the PDF file in binary read mode.
- **client.create_index():** Initiates the index creation process.
- **response.data.task_id:** Receives a unique identifier to track the status of the indexing task.

**Next Steps:**

Use the `Task ID` to monitor the progress of the index creation using polling or webhooks.

#### Create Index with Polling

Polling allows your application to regularly check the status of an asynchronous task until it completes.

##### Example: Create Index and Wait for Completion

```python
try:
    # Open the file in binary mode
    with open('document.pdf', 'rb') as file:
        # Initiate index creation and wait for it to complete
        response, status = client.create_index_and_poll(
            document=file,          # Pass the binary file object
            filename='document.pdf',# Provide the filename
            poll_interval=20,       # Time in seconds between each poll
            max_retries=10          # Maximum number of polling attempts
        )
    # Print the Index ID once creation is complete
    print(f"Index ID: {response.data.task_id}")
except APIError as e:
    print(f"An error occurred: {e}")
```

**Explanation:**

- **client.create_index_and_poll():** Combines index creation and polling into a single step.
- **poll_interval:** Defines how frequently the client checks the task status.
- **max_retries:** Limits the number of polling attempts to prevent indefinite waiting.

**Output:**

Once the index is successfully created, the script will display the `Index ID`, which you can use for further operations.

#### Add Document to Index

Adding documents to an existing index allows you to expand the knowledge base your application can query.

> **ℹ️ Information:** *Adding documents is also an asynchronous process. Ensure that the index you are adding to already exists.*

##### Example: Add a New Document to an Existing Index

```python
try:
    # Open the new document you want to add in binary read mode
    with open('document.pdf', 'rb') as file:
        # Send a request to add the document to the specified index
        response = client.add_document(
            index_id='your_index_id',      # Use the valid index_id obtained earlier
            document=file,                 # Pass the binary file object
            filename='document.pdf'        # Provide the filename
        )
        # Print the received Task ID to monitor progress
        print(f"Task ID: {response.data.task_id}")
except APIError as e:
    print(f"An error occurred while adding the document: {e}")

```

**Explanation:**

- **index_id='your_index_id':** Replace `'your_index_id'` with your actual Index ID.
- **client.add_document():** Sends a request to add the new document to the specified index.

**Next Steps:**

Use the `Task ID` to monitor the progress of the document addition using polling or webhooks.

#### Add Document with Polling

Wait for the document addition process to complete by periodically checking its status.

##### Example: Add Document and Wait for Completion

```python
try:
    with open('document.pdf', 'rb') as file:
        response, status = client.add_document_and_poll(
            index_id='your_index_id',
            document=file,               # Pass the binary file object
            filename='document.pdf',     # Provide the filename
            poll_interval=20,            # Time in seconds between each poll
            max_retries=10               # Maximum number of polling attempts
        )

    document_id = getattr(status, 'document_id', None)

    print("Document indexing completed")
    print(f"Status Details: {status}")
        
except APIError as e:
    print(f"An API error occurred while adding the document: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

**Explanation:**

- **client.add_document_and_poll():** Combines document addition and polling into a single step.
- **document='document.pdf':** Specifies the document to add.
- **poll_interval & max_retries:** Control the polling behavior.

**Output:**

Once the document is successfully added, the script will display the `Document ID`.

#### List Indices

Retrieve a list of all indices you have created. This is useful for managing and selecting the correct index for your operations.

##### Example: List All Indices

```python
try:
    indices = client.list_indexes()
    if not indices:
        print("No indices found.")
    else:
        for index in indices:
            index_id = getattr(index, 'id', None)
            if index_id:
                print(f"Index ID: {index_id}")
            else:
                print("Encountered an index without an ID.")
                
except APIError as e:
    print(f"An API error occurred while listing indexes: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

**Explanation:**

- **client.list_indices():** Sends a request to retrieve all indices.
- **indices.data:** Contains the list of indices returned by the API.

**Output:**

The script will print the `Index ID` and `Name` of each index, helping you identify which one to use.

#### List Documents

Retrieve all documents within a specific index. This helps you understand the contents and manage the documents effectively.

##### Example: List All Documents in an Index

```python
try:
    documents = client.get_documents('your_index_id')
    for doc in documents.data.documents:
        print(f"Document ID: {doc.id}")
        print(f"Created At: {doc.created_at}")
        print(f"Updated At: {doc.updated_at}")
        print(f"Index ID: {documents.data.index}")
        print("---")
except (APIError, Exception) as e:
    print({'error': str(e)})
```

**Explanation:**

- **client.get_documents('your_index_id'):** Fetches all documents within the specified index.
- **documents.data.documents:** Contains the list of documents returned by the API.

**Output:**

The script will print the `Document ID` and `Filename` for each document, aiding in document management.

#### Delete Document

Remove a specific document from an index. This action is irreversible, so proceed with caution.

> **⚠️ Important:** *Deleting a document permanently removes it from the index and cannot be undone.*

##### Example: Delete a Document from an Index

```python
try:
    # Attempt to delete the specified document from the index
    client.delete_document(index_id='your-index-id', document_id='document-id-to-delete')
    print("Document deleted successfully.")
except APIError as e:
    # Handle any API-related errors
    print(f"Error deleting document: {e}")
```

**Explanation:**

- **index_id='your-index-id':** Replace with your actual Index ID.
- **document_id='document-id-to-delete':** Replace with the Document ID you wish to delete.
- **client.delete_document():** Sends a request to delete the specified document.

**Output:**

If successful, the script will confirm the deletion. Otherwise, it will display an error message.

### Retrieve

Engage in natural language conversations with your indexed documents. This feature allows you to ask questions and receive answers based on the content of your documents.

> **💡 Tip:** *Formulate clear and specific questions to get the most accurate responses.*

##### Example: Query with Your Index

```python
try:
    # Send a natural language query to the specified index
    response = client.retrieve(
        index_id='your-index-id',
        query="What are the main points discussed in the document?"
    )
    # Print the response from the platform
    print(f"Response: {response}")
except APIError as e:
    # Handle any API-related errors
    print(f"Error: {e}")
```

**Explanation:**

- **index_id='your-index-id':** Replace with your actual Index ID.
- **query="...":** The natural language question you want to ask.
- **client.retrieve():** Sends the query to the platform and retrieves the response.

**Output:**

The script will display the response generated based on the content of your indexed documents.

### Search

Perform precise and accurate searches within your indexed documents. This feature leverages both keyword and semantic understanding to deliver relevant results.

##### Example: Perform a Search Query

```python
try:
    results = client.search(
        index_id='your_index_id',
        query="neural networks"
    )
    print(results)
        
except APIError as e:
    print(f"Error: {e}")
```

**Explanation:**

- **query="neural networks":** The search term you want to look for within your documents.
- **client.search():** Sends the search query to the platform.
- **results:** Contains the list of search results returned by the API.

**Output:**

The script will print each document that matches the search query along with a relevance score, indicating how closely the document matches the query.

#### Task Status

Monitor the progress of any asynchronous operation, such as creating an index or adding a document. This helps you manage long-running tasks effectively.

##### Example: Check Task Status

```python
try:
    # Replace 'your-task-id' with the actual Task ID you received earlier
    status = client.get_task_status('your-task-id')
    print(f"Task Status: {status.status}")
except APIError as e:
    # Handle any API-related errors
    print(f"Error: {e}")

# Optional: Polling until the task is complete
import time

while True:
    try:
        status = client.get_task_status('your-task-id')
        print(f"Status: {status.status}")
        if status.status == 'completed':
            print("Task completed successfully.")
            break
        elif status.status == 'failed':
            print("Task failed.")
            break
        time.sleep(5)  # Wait for 5 seconds before checking again
    except APIError as e:
        print(f"Error: {e}")
        break
```

**Explanation:**

- **client.get_task_status('your-task-id'):** Fetches the current status of the specified task.
- **Polling Loop:** Continuously checks the task status every 5 seconds until it completes or fails.

**Output:**

The script will print the current status of the task. Once completed, it will confirm the success or indicate if the task failed.

### Instant RAG

Instant RAG allows you to perform quick, one-time analyses on your text content without the need to create and maintain persistent indices. This is ideal for extracting key insights from smaller or temporary datasets.

> **ℹ️ Note:** *Instant RAG supports up to 8,000 tokens, approximately 32,000 characters or 26 pages of content.*

#### Create Instant RAG

##### Example: Initiate an Instant RAG Session

```python
# Define the context text you want to analyze
context = """
Your extensive text content goes here. This can be a comprehensive document
that you need to analyze or query immediately without creating a persistent index.
"""

# Send a request to create an Instant RAG session
response = client.create_instant_rag(context=context)

print(f"Message: {response.message}")
print(f"ID: {response.id}")
```

**Explanation:**

- **context:** The text content you want to analyze.
- **client.create_instant_rag():** Initiates an Instant RAG session with the provided context.

**Output:**

The script will display the `Instant RAG ID`, which you can use to perform queries.

#### Query Instant RAG

##### Example: Query Your Instant RAG Session

```python
response = client.query_instant_rag(
        index_id='your_index_id',
        query='your search query'
)
# Print the response from the platform
print(f"Response: {response}")
```

**Explanation:**

- **rag_id="your_index_id":** The Instant RAG ID obtained from the previous step.
- **query="...":** The question you want to ask based on the provided context.
- **client.query_instant_rag():** Sends the query to the Instant RAG session and retrieves the response.

**Output:**

The script will display the response generated based on the context provided during the Instant RAG session.

### Webhooks

Webhooks are essential for handling asynchronous operations efficiently. They allow your application to receive real-time notifications about events, such as task completions, without the need to continuously poll the API.

> **💡 Tip:** *Webhooks are recommended for production environments to improve scalability and reduce unnecessary API calls.*

#### Create Webhook

Set up a webhook to receive notifications about specific events from the iQ Suite Platform.

##### Example: Create a New Webhook

```python

webhook = client.create_webhook(
    url="https://your-domain.com/webhook",   # Your custom domain where the events notifications will be sent
    name="Processing Events",                # Webhook name
    enabled="true",                          # Webhook Enabled (true/false)
    secret="your-webhook-secret"             # Add a layer of security with secret 
)

print(webhook)
```

**Explanation:**

- **url:** The endpoint in your application that will receive webhook notifications. Ensure this endpoint is publicly accessible.
- **name:** A name to help you identify the webhook.
- **enabled:** Whether the webhook is active.
- **secret:** A secret key used to verify the authenticity of incoming webhook requests.

**Output:**

The script will display the `Webhook ID`, which you can use for managing the webhook.

#### List Webhooks

Retrieve a list of all webhooks you have set up. This helps you manage and review your webhook configurations.

##### Example: List All Webhooks

```python
try:
    webhooks = client.list_webhooks()
    print("\n=== Webhooks List ===")
    print(f"{'ID':<6} {'Name':<30} {'URL':<40} {'Status':<10} {'Created At'}")
    print("-" * 96)
    
    for webhook in webhooks:
        status = "Enabled" if webhook['enabled'] else "Disabled"
        print(f"{webhook['id']:<6} {webhook['name']:<30} {webhook['url']:<40} {status:<10} {webhook['created_at']}")

except Exception as e:
    print(f"Error getting webhooks: {str(e)}")
```

**Explanation:**

- **client.list_webhooks():** Sends a request to retrieve all webhooks.
- **webhooks.data:** Contains the list of webhooks returned by the API.

**Output:**

The script will print the `Webhook ID`, `URL`, and `Enabled` status for each webhook, aiding in webhook management.

#### Update Webhook

Modify the configuration of an existing webhook. This is useful if you need to change the endpoint URL, name, or other settings.

##### Example: Update an Existing Webhook

```python
updated_webhook = client.update_webhook(
    webhook_id="whk_abc123",                                    # The ID of the webhook to update
    url="https://your-domain.com/new-endpoint",                 # The new endpoint URL
    name="Updated Webhook Name",                                # The new name for the webhook
    enabled="true"                                              # Whether the webhook should be enabled (true/false)
)
# Print the updated webhook details
print(f"Updated Webhook: {updated_webhook}")
```

**Explanation:**

- **webhook_id="whk_abc123":** Replace with the actual Webhook ID you wish to update.
- **client.update_webhook():** Sends a request to update the webhook's configuration.

**Output:**

The script will display the updated webhook details, confirming the changes.

#### Delete Webhook

Remove a webhook from your account. This stops all notifications to the specified endpoint immediately.

> **⚠️ Important:** *Deleting a webhook is irreversible and will immediately cease all notifications to the associated endpoint.*

##### Example: Delete a Webhook

```python
try:
    # Attempt to delete the specified webhook
    client.delete_webhook(webhook_id="your_webhook_id")
    print("Webhook deleted successfully.")
except APIError as e:
    # Handle any API-related errors
    print(f"Error deleting webhook: {e}")
```

**Explanation:**

- **webhook_id="your_webhook_id":** Replace with the actual Webhook ID you wish to delete.
- **client.delete_webhook():** Sends a request to delete the specified webhook.

**Output:**

If successful, the script will confirm the deletion. Otherwise, it will display an error message.

#### Webhook Events

When specific events occur, the iQ Suite Platform sends POST requests to your webhook endpoint with relevant information. Here's what a typical webhook payload looks like:

```json
{
  "event": "index_creation_complete",
  "task_id": "2dca8de9-8a51-497a-9a45-cc6541d4a7bc",
  "index": "08c9ab9f-1b1c-4fc8-8679-a63387654893",
  "status": "completed"
}
```

**Explanation of Payload Fields:**

- **event:** The type of event that triggered the webhook (e.g., `index_creation_complete`).
- **task_id:** The unique identifier for the task associated with the event.
- **index_id:** The unique identifier for the index associated with the event.
- **status:** The current status of the task (e.g., `completed`, `failed`).

> **🔒 Important:** *Always verify webhook signatures in production environments to ensure that incoming requests are genuinely from the iQ Suite Platform and not malicious actors.*

## Supported Documents

The iQ Suite Platform supports a variety of document formats, ensuring flexibility in handling different types of data. Additionally, documents are automatically processed with Optical Character Recognition (OCR) when applicable, enabling the extraction of text from images or scanned documents.

### Supported Formats

1. **PDF Files (.pdf):**
   - **Text-based PDFs:** PDFs that contain selectable text.
   - **Scanned PDFs with OCR Support:** Image-based PDFs that require OCR to extract text.

2. **Microsoft Word Documents:**
   - **Modern Format (.docx):** The current standard format for Word documents.
   - **Legacy Format (.doc):** Older Word document format.

3. **Microsoft PowerPoint Presentations:**
   - **Modern Format (.pptx):** The current standard format for PowerPoint presentations.
   - **Legacy Format (.ppt):** Older PowerPoint presentation format.

### Best Practices for Document Preparation

- **Ensure Proper Formatting:** Well-structured documents with clear headings, subheadings, and consistent formatting improve processing accuracy.
- **Clear and Legible Text:** Especially important for scanned documents, as OCR accuracy depends on text clarity.
- **Avoid Complex Layouts:** Extremely intricate layouts may pose challenges during text extraction.
- **Password Management:** For password-protected PDFs, ensure you have the necessary permissions and provide the correct password during upload.

> **💡 Tip:** *Review your documents for any sensitive information before uploading, especially when dealing with password-protected files.*

## Error Handling

Robust error handling is crucial for building reliable and user-friendly applications. The iQ Suite Python SDK provides specific exceptions to handle various error scenarios effectively.

### Exception Types

- **`AuthenticationError`:** Raised when API authentication fails due to invalid or expired API keys.
- **`RateLimitError`:** Raised when the number of requests exceeds the allowed rate limit.
- **`ValidationError`:** Raised when input parameters are invalid or malformed.
- **`APIError`:** General API-related errors that don't fall under other specific categories.
- **`NetworkError`:** Raised when there are connectivity issues or network-related problems.

### Example: Comprehensive Error Handling

```python
from iqsuite.exceptions import (
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError,
    NetworkError
)

try:
    # Attempt to create an index with a document
    result = client.create_index(document='file.pdf')
except AuthenticationError as e:
    # Handle invalid or expired API keys
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    # Handle rate limit exceeding
    print(f"Rate limit exceeded. Try again at: {e.reset_at}")
except ValidationError as e:
    # Handle invalid input parameters
    print(f"Invalid input: {e.errors}")
except APIError as e:
    # Handle general API errors
    print(f"API error: {e.message} (Status Code: {e.status_code})")
except NetworkError as e:
    # Handle connectivity issues
    print(f"Network error: {e}")
```

**Explanation:**

- **try-except Blocks:** Each exception type is caught and handled individually to provide specific error messages.
- **Descriptive Messages:** Informative messages help in understanding the nature of the error and possible remediation steps.

### Common HTTP Status Codes

Understanding HTTP status codes can aid in diagnosing issues when interacting with the API.

- **`400 Bad Request`:** The server could not understand the request due to invalid syntax. *Action:* Check your input parameters.
- **`401 Unauthorized`:** Authentication failed. *Action:* Verify your API key.
- **`403 Forbidden`:** You don't have the necessary permissions to access the resource. *Action:* Check your account permissions.
- **`404 Not Found`:** The requested resource does not exist. *Action:* Ensure the resource ID is correct.
- **`429 Too Many Requests`:** You've exceeded the allowed rate limit. *Action:* Wait before making more requests.
- **`500 Internal Server Error`:** The server encountered an unexpected condition. *Action:* Contact support.

> **⚠️ Warning:** *Always implement proper error handling in your application to manage unexpected scenarios gracefully and enhance user experience.*

## Support

We're dedicated to helping you make the most of the iQ Suite Platform. Whether you need technical assistance, want to provide feedback, or are looking for resources to learn more, our support channels are here for you.

### Documentation

Comprehensive documentation is available to guide you through every aspect of the iQ Suite Platform and the Python SDK.

- 📚 [API Documentation](https://docs.iqsuite.ai/)
- 🔧 [SDK Reference](https://docs.iqsuite.ai/sdk/python)
- 📖 [Tutorials & Guides](https://docs.iqsuite.ai/tutorials)

### Getting Help

If you encounter issues or have questions, reach out through the following channels:

- 📧 [Email Support](mailto:support@iqsuite.ai): Contact our support team directly via email for personalized assistance.
- 💬 [Discord Community](https://discord.gg/iqsuite): Join our Discord server to interact with other users and developers, share experiences, and get real-time help.
- 🐛 [GitHub Issues](https://github.com/iqsuite/iqsuite-python/issues): Report bugs or request new features by opening an issue on our GitHub repository.

### Best Practices

Adhering to best practices ensures that you build robust and efficient applications with the iQ Suite Python SDK.

- ✅ **Keep SDK Updated:** Regularly update to the latest SDK version to benefit from new features, improvements, and security patches.

  ```bash
  pip install --upgrade iqsuite
  ```

- 📝 **Enable Logging:** Activate logging during development to facilitate debugging and monitor application behavior.

  ```python
  import logging

  logging.basicConfig(level=logging.INFO)
  ```

- 🔄 **Implement Retries:** Use retry mechanisms to handle transient errors gracefully, especially when dealing with network-related issues or rate limits.

  ```python
  import time

  max_retries = 5
  for attempt in range(max_retries):
      try:
          response = client.create_index(document='file.pdf')
          break  # Exit loop if successful
      except RateLimitError:
          print("Rate limit exceeded. Retrying...")
          time.sleep(2 ** attempt)  # Exponential backoff
  else:
      print("Failed to create index after multiple attempts.")
  ```

- 🔒 **Secure Your API Keys:** Follow security best practices to protect your API credentials, such as using environment variables and avoiding hardcoding sensitive information.

*© 2025 iQ Suite. All rights reserved.*

> **💡 Tip:** *Engage with the community and stay updated with the latest developments to maximize the benefits of the iQ Suite Platform.*

---

*If you have any suggestions or feedback on this documentation, please feel free to [open an issue](https://github.com/iqsuite/iqsuite-python/issues) on our GitHub repository.*
