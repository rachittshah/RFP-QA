# Document Question-Answering System

This document explains the design and functionality of a Document-based Question-Answering system, powered by OpenAI's LLMs. This system allows users to upload documents, which are then processed and utilized to provide responses to queries based on the content of those documents.

## Architecture

The system is built on the Flask web framework, creating an interface for users to interact with the system through HTTP requests. It primarily uses OpenAI's GPT-3 model and various other modules from the Langchain library to handle the document processing and question-answering functionality. 

## Modules and Functionality

The system is organized into three main parts: 

1. **Document Uploading:** Users can upload files to the server via an HTML form. Upon receiving the files, the system saves them locally and processes them to create a database of vectorized representations of the documents' contents.

2. **Query Processing:** The system receives a user query, searches for relevant parts of the uploaded documents, and uses a pre-set question-answering chain to formulate an answer based on the documents' content.

3. **Answer Generation:** It produces an output, including the answer to the query and reference context from the documents.

The helper functions `process_docs()`, `setup_qa_chain()`, and `getanswer()` handle the various stages of this pipeline.

## Endpoints

The system exposes three HTTP endpoints:

- **`/health`**: Returns the status of the system.
- **`/upload`**: Handles document uploads and processes them for the question-answering functionality.
- **`/docqna`**: Handles POST requests with a query and returns an answer generated from the uploaded documents.

## Helpers

The `helpers` module consists of the core functionalities:

- **`process_docs`**: This function loads the documents from the 'docs' directory, splits them into chunks, creates embeddings for these chunks using the OpenAI API, and stores the embeddings in a FAISS (Facebook AI Similarity Search) index for efficient similarity search. 
  - For more document types, I've used Directoryloader from [Langchain](https://python.langchain.com/docs/modules/data_connection/document_loaders/how_to/file_directory)

- **`setup_qa_chain`**: This function sets up the question-answering chain, which includes a prompt template, an output parser, and an instance of the OpenAI model. The chain is responsible for processing a query and generating an answer.
  - I've used map_rerank chain as I wished to reduce hallucinations to a minimum while reducing API costs. The tradeoff is a more factual sounding answer than a conversational chain.

- **`getanswer`**: This function receives a query, finds the most relevant chunks of text from the uploaded documents, feeds these chunks and the query into the QA chain, and formats the output.

## Application improvements and shortcomings

- The application doesn't support png/jpeg files yet. This was due to a pytesseract error on my machine and was able to test it out.
- Adding Prompt Caching: Cache requests and store them in a vectorstore. This will reduce the LLM API call cost since we can just return cached requests. Proposed library to use is [GPTCache](https://github.com/zilliztech/GPTCache)
- Key rotation and fallback LLMs: due to a lack of API keys, i wasn't able to apply fallback keys and LLMs. This approach will improve the reliablity of the application, and allow the user to experience lower downtime then usual, and i wished to [BerriAI](https://github.com/BerriAI/reliableGPT) for the same.
- OSS embeddings: reduce the cost for embeddings generation via using OSS embeddings which can reduce costs further.
- Evals: Inspite of using map_rerank, the application can benefit massively from using evals which can help improve user experience further.
- Adding a NoSQL database to store user conversations and documents.
- Use a temp S3 bucket instead of local docs hosting to save on compute and improve bandwith. Downside is increase in compute and hosting costs.
- Support for OSS LLMs: for enterprise data localization, using OSS LLMs is better choice.
- Adding Logging: I tried to apply logging via [Portkey.ai](https://portkey.ai/), but i will continue to explore this or Langsmith to allow more visibilty on the performance of the model.

## Running the App

Clone the repo
```shell
git clone https://github.com/rachittshah/RFP-QA.git
```
Create a virtual environment and perform a requirements.txt install
```shell
pip install -r requirements.txt
```

The system uses the environment variable `OPENAI_API_KEY` for API authentication and `PORT` to set the port number for the Flask server. Set your OpenAI key in the .env file

To run the system, execute the main Flask app script. 
```shell
python main.py
```

You can then interact with the system through the exposed HTTP endpoints.

---

Please ensure to have all the dependencies installed before running the application. 

This README should serve as a basic guide to understanding and running the system. Feel free to explore the codebase for a deeper understanding.

---

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
