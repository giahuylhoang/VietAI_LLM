#%%
from llama_index.core import Document
import json

with open('data/blog_contents.json') as f:
    data = json.load(f)['blog_posts']

def create_document(content):
    return Document(
        text=content["content"],
        metadata={
            "title": content["title"],
            "date": content["date"],
            "author": content["author"],
            "tags": content["tags"],
            "related_posts": content["related_posts"],
            # "link": content["link"],

        }
    )

documents = [create_document(content) for content in data]



#load the model and the embedding
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings

gemini_pro_api_key = "AIzaSyDa-RmgQUEvsEN-oeExl31Se9apTVEFdY8"

Settings.llm = Gemini(api_key=gemini_pro_api_key, model="models/gemini-pro")
Settings.embed_model = GeminiEmbedding(api_key=gemini_pro_api_key)

# %%


from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
)

# %%


#%%
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core import VectorStoreIndex
import time
import nest_asyncio

nest_asyncio.apply()

parser = SentenceSplitter(chunk_size=1024, chunk_overlap=10)
summary_extractor = SummaryExtractor(nodes=2)
qa_extractor = QuestionsAnsweredExtractor(questions=3)

transformations = [parser, summary_extractor, qa_extractor]

pipeline = IngestionPipeline(transformations=transformations)

# time this block code 
time_start = time.time()


nodes = pipeline.run(documents=documents[0:2])
time_end = time.time()
print(f"Indexing took {time_end - time_start} seconds")

#approximate time taken: 0.2 minutes per document, 155 documents ~ 31 minutes
# %%

# LlamaIndex Newsletter 2024-03-05
# Mastering PDFs: Extracting Sections, Headings, Paragraphs, and Tables with Cutting-Edge Parser

# indexing 

from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

vector_index = VectorStoreIndex(nodes)
summary_index = SummaryIndex(nodes)


#%%
#query engines

list_query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize", use_async=True
)
vector_query_engine = vector_index.as_query_engine(
    response_mode="tree_summarize", use_async=True
)

list_tool = QueryEngineTool.from_defaults(
    query_engine=list_query_engine,
    description="Useful for questions asking specific questions about the blogs of llama-index.",
)
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description=(
        "Useful for retrieving specific snippets from the blog post of llama-index."
    ),
)
query_engine = RouterQueryEngine(
    verbose=True,
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[
        list_tool,
        vector_tool,
    ],
)
# %%
from llama_index.core.tools import RetrieverTool
from llama_index.core.retrievers import RouterRetriever

summary_retrevier = summary_index.as_retriever()
vector_retriever = vector_index.as_retriever()

# initialize tools
vector_tool = RetrieverTool.from_defaults(
    retriever=vector_retriever,
    description="Useful for retrieving specific context from Paul Graham essay on What I Worked On.",
)
list_tool = RetrieverTool.from_defaults(
    retriever=summary_retrevier,
    description="Useful for retrieving specific context from Paul Graham essay on What I Worked On (using entities mentioned in query)",
)

# This isn't work yet! 
# define retriever
retriever = RouterRetriever(
    verbose=True,
    selector=LLMSingleSelector.from_defaults(llm=Settings.llm),
    retriever_tools=[
        vector_tool,
        list_tool,
    ],
)
# %%
