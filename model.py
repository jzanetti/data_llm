from base64 import b64encode
from io import BytesIO

from llama_cpp import Llama
from llama_index.core import ServiceContext, set_global_service_context
from llama_index.core.query_engine import PandasQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.llama_cpp.llama_utils import (
    completion_to_prompt,
    messages_to_prompt,
)
from matplotlib.pyplot import close as plt_close
from pandas import DataFrame

from model import CODELLM_PATH, LLM_PATH

from model import EMBEDDING_PATH


def create_img(df: DataFrame, pandas_instruction_str: str, verbose: bool = True):

    if verbose:
        print(pandas_instruction_str)
    fig = eval(pandas_instruction_str)

    # Convert the figure to a Dash image using BytesIO
    output_buffer = BytesIO()
    fig.figure.savefig(output_buffer, format="png")  # Access the figure object
    plt_close(fig.figure)
    image_data = output_buffer.getvalue()

    # Convert the image_data to base64
    image_base64 = b64encode(image_data).decode("utf-8")

    # Construct the source URL for the image
    return f"data:image/png;base64,{image_base64}"


def create_dataframe_engine(df: DataFrame, verbose: bool = True):
    return PandasQueryEngine(df=df, verbose=verbose)


def load_service(llm_model, embed_model, chunk_size: int = 1024):
    service_context = ServiceContext.from_defaults(
        llm=llm_model,
        chunk_size=chunk_size,
        embed_model=embed_model,
    )
    set_global_service_context(service_context)


def load_embedding_model():
    """The model can be chosen from:
        - "BAAI/bge-large-en-v1.5": "BAAI General Embedding Model (large) v1.5",
        - "BAAI/bge-small-en-v1.5": "BAAI General Embedding Model (small) v1.5",

    Args:
        embedding_model_name (str, optional): _description_. Defaults to "BAAI/bge-small-en-v1.5".

    Returns:
        _type_: _description_
    """
    return HuggingFaceEmbedding(model_name=EMBEDDING_PATH)


def load_llama_index_llm_model(
    llm_model_name: str = CODELLM_PATH,
    temperature: float = 0.1,
    max_new_tokens: int = 1024,
    context_window: int = 5000,
    generate_kwargs: dict = {},
    model_kwargs: dict = {"n_gpu_layers": 30, "repetition_penalty": 1.5},
    verbose: bool = True,
):
    """The model we can choose from are:
        - /home/zhangs/Github/llm-abm/llama3-Instruct/Meta-Llama-3-8B-Instruct.gguf
        - CodeLlama-34b-Instruct/CodeLlama-34b-Instruct.gguf
        - codellama-7b-instruct.Q8_0.gguf.2

    Args:
        llm_model_name (str, optional): llm model name. default is codellama-7b-instruct.Q8_0.gguf.2

    Returns:
        _type_: _description_
    """

    return LlamaCPP(
        model_path=llm_model_name,
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        context_window=context_window,
        generate_kwargs=generate_kwargs,
        model_kwargs=model_kwargs,
        messages_to_prompt=messages_to_prompt,
        completion_to_prompt=completion_to_prompt,
        verbose=True,
    )


def load_llama_cpp_llm_model(llm_model_name: str = LLM_PATH, verbose: bool = False):
    return Llama(
        model_path=llm_model_name,
        verbose=verbose,
    )
