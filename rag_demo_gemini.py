from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

gemini_pro_api_key = "Input your key here"

# load documents
documents = SimpleDirectoryReader(input_files=["attention.pdf"]).load_data()
print(f"Loaded {len(documents)} documents.")

# split documents into nodes
splitter = SentenceSplitter(chunk_size=1024)
nodes = splitter.get_nodes_from_documents(documents)
print(f"Created {len(nodes)} nodes.")

# load the model
Settings.llm = Gemini(api_key=gemini_pro_api_key, model="models/gemini-pro")  
Settings.embed_model = GeminiEmbedding(api_key=gemini_pro_api_key, model="models/embedding-001") 
print("Loaded the embed model.")

# create the indexes
summary_index = SummaryIndex(nodes)
vector_index = VectorStoreIndex(nodes)
print("Created the indexes.")

# create the query engines
summary_query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize",
    use_async=True,
)
vector_query_engine = vector_index.as_query_engine()
print("Created the query engines.")

# create the tools for the query engines
summary_tool = QueryEngineTool.from_defaults(
    query_engine=summary_query_engine,
    description=(
        "Useful for summarization questions related to any topic in the Deep Learning book."
    ),
)
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description=(
        "Useful for retrieving specific context from the Deep Learning book."
    ),
)
print("Created the tools.")

# create the router query engine
query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[
        summary_tool,
        vector_tool,
    ],
    verbose=True
)
print("Created the router query engine.")


print ("\n\nNow querying...")
# Query  ---------------------------------------------
question1 = "What is the summary of the paper?"
print (f"Querying: {question1}")
response = query_engine.query(question1)
print(str(response))
# Query  ---------------------------------------------
question2 = "What is evaluation result of Transformer compared to other models? Which page do you get this information? Can you tell me why it's better than others?"
print (f"\nQuerying: {question2}")
response = query_engine.query(question2)
print(str(response))