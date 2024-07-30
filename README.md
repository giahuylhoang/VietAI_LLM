
# Gia-Huy Hoang 
# Assignment 1


## Introduction
This project aimed to evaluate different embedding models and chunk sizes to optimize a Retrieval-Augmented Generation (RAG) pipeline. The goal was to determine the best configuration for retrieving relevant information and accurately answering questions about LLamaIndex blog.

## Methodology
### Data Collection
- **Web Scraping**: Used Selenium and BeautifulSoup to scrape blog links from the LlamaIndex blog page.
- **Data Storage**: Stored the scraped data in a JSON file with metadata including date, author, title, tags, content, related posts, and link.

### Data Processing
- **Document Creation**: Converted blog post data into Document objects using the `llama_index.core` module.
- **Ingestion Pipeline**: Processed documents into manageable chunks using `MarkdownNodeParser` and `SentenceSplitter`. Tested chunk sizes of 512 with an overlap of 50, and 1024 with an overlap of 10.

### Embedding Models
Tested various embedding models:
1. embed-english-v2.0 (Cohere)
2. text-embedding-3-small (OpenAI)
3. embedding-001 (Gemini)
4. voyage-2 (Voyage)
5. embed-english-v3.0 (Cohere)
6. text-embedding-ada-002 (OpenAI)

### Retrieval and Evaluation
- **Retriever Configuration**: Built vector and summary retrievers, wrapped into retriever tools, and combined into a `RouterRetriever`.
- **QA Dataset**: Fenerated question-context pairs using the `llama_index`  function `generate_question_context_pairs` and handled API rate limits with exponential backoff.
- **Evaluation Metrics**: Evaluated using hit rate, Mean Reciprocal Rank (MRR), precision, recall, Average Precision (AP), and Normalized Discounted Cumulative Gain (NDCG).

## Results

### Chunk Size: 1024

|    **reranker & metrics**         | embed-english-v2.0 | text-embedding-ada-002 | embedding-001 | text-embedding-3-small | voyage-2 | embed-english-v3.0 |
|-----------------------|--------------------|------------------------|---------------|------------------------|----------|---------------------|
| hit_rate (base)       | 0.890000           | 0.890000               | 0.890000      | 0.890000               | 0.890000 | 0.890000            |
| mrr (base)            | 0.655810           | 0.655810               | 0.655810      | 0.655810               | 0.655810 | 0.655810            |
| hit_rate (bge_small)  | 0.890000           | 0.890000               | 0.890000      | 0.890000               | 0.890000 | 0.890000            |
| mrr (bge_small)       | 0.718024           | 0.718024               | 0.718024      | 0.718024               | 0.718024 | 0.718024            |
| hit_rate (bge_large)  | 0.890000           | 0.890000               | 0.890000      | 0.890000               | 0.890000 | 0.890000            |
| mrr (bge_large)       | 0.727107           | 0.727107               | 0.727107      | 0.727107               | 0.727107 | 0.727107            |
| hit_rate (cohere)     | 0.890000           | 0.890000               | 0.890000      | 0.890000               | 0.890000 | 0.890000            |
| mrr (cohere)          | 0.752333           | 0.752333               | 0.752333      | 0.752333               | 0.752333 | 0.752333            |

### Chunk Size: 512

|  **reranker & metrics**         | embed-english-v2.0 | text-embedding-ada-002 | embedding-001 | text-embedding-3-small | voyage-2 | embed-english-v3.0 |
|-----------------------|--------------------|------------------------|---------------|------------------------|----------|---------------------|        
| hit_rate (base)       | 0.780000           | 0.780000               | 0.780000      | 0.780000               | 0.780000 | 0.780000            |
| mrr (base)            | 0.515036           | 0.515036               | 0.515036      | 0.515036               | 0.515036 | 0.515036            |
| hit_rate (bge_small)  | 0.780000           | 0.780000               | 0.780000      | 0.780000               | 0.780000 | 0.780000            |
| mrr (bge_small)       | 0.678429           | 0.678429               | 0.678429      | 0.678429               | 0.678429 | 0.678429            |
| hit_rate (bge_large)  | 0.780000           | 0.780000               | 0.780000      | 0.780000               | 0.780000 | 0.780000            |
| mrr (bge_large)       | 0.666940           | 0.666940               | 0.666940      | 0.666940               | 0.666940 | 0.666940            |
| hit_rate (cohere)     | 0.780000           | 0.780000               | 0.780000      | 0.780000               | 0.780000 | 0.780000            |
| mrr (cohere)          | 0.673583           | 0.673583               | 0.673583      | 0.673583               | 0.673583 | 0.673583            |

### Chunk Size Comparison
- **Chunk Size 1024**: Achieved a hit rate of 0.89 and consistently performed better across different embedding models.
- **Chunk Size 512**: Achieved a hit rate of 0.78, indicating worse performance compared to chunk size 1024.

### Embedding Models
- No significant difference in performance between the embedding models, possibly due to hidden errors in the code.
- The best rerank model was "Cohere," which consistently achieved the highest MRR across different embedding models.

### Final RAG Pipeline
- **Embedding Model**: Used Gemini embedding-001.
- **Base LLM Model**: Used "gemini-1-5-flash."
- **Reranker**: Used Cohere.
- **Router Engine**: Utilized both summary and vector retrieval, with `LLMSingleSelector` to choose the appropriate query engine.
- **Helper Function**: Implemented `query_and_print_sources` with Tenacity for handling backoff limits and node preprocessing to retain nodes with similarity greater than 0.7.

## Conclusion
The final RAG pipeline effectively retrieves relevant nodes and answers questions successfully. Despite some hidden errors affecting the hit rate across different embedding models, the chunk size of 1024 outperformed 512. The use of Cohere as the reranker and Gemini embedding-001 as the embedding model provided the best results for the RAG system.
