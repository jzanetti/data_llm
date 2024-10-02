from os import system

from llama_index.core import (
    ServiceContext,
    Settings,
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms.openai import OpenAI

from model import load_embedding_model, load_llama_index_llm_model

data_src = {
    "report2022.pdf": "https://www.esr.cri.nz/media/v5pdmehg/esr-annual-report-2022.pdf",
    "report2023.pdf": "https://www.esr.cri.nz/media/cjnl4e0j/2023-annual-report-esr.pdf",
}

# download pdf
# for pdf_name in data_src:
#    cmd = f"wget {data_src[pdf_name]} -O {pdf_name}"
#    system(cmd)


report2022 = SimpleDirectoryReader(input_files=["report2022.pdf"]).load_data()
report2023 = SimpleDirectoryReader(input_files=["report2023.pdf"]).load_data()


llm = load_llama_index_llm_model(
    llm_model_name="llama3/Meta-Llama-3-8B.gguf", max_new_tokens=1024
)
Settings.llm = llm
embed_model = load_embedding_model()
service_context = ServiceContext.from_defaults(
    chunk_size=1024, llm=llm, embed_model=embed_model
)
report2022_index = VectorStoreIndex.from_documents(
    report2022, service_context=service_context
)
report2023_index = VectorStoreIndex.from_documents(
    report2023, service_context=service_context
)

report2022_engine = report2022_index.as_query_engine(similarity_top_k=3)
report2023_engine = report2023_index.as_query_engine(similarity_top_k=3)

query_engine_tools = [
    QueryEngineTool(
        query_engine=report2022_engine,
        metadata=ToolMetadata(
            name="r1",
            description=("Provides information for 2022 year"),
        ),
    ),
    QueryEngineTool(
        query_engine=report2023_engine,
        metadata=ToolMetadata(
            name="dfd",
            description=("Provides information for 2023 year"),
        ),
    ),
]
print("creating querying")
s_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=query_engine_tools)

print("start querying")
response = s_engine.query(
    "What's the number of peer-reviewed publications for ESR for 2022, and how about 2023"
)

print(response)
