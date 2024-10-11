# data_llm


## Creating the data_llm environment
```
conda env create -f env.yml
```

## Start the application
```
python app.py
```

## Building and run docker:
Alternatively, a docker container can be used:

The container can be built using:
```
docker build -t data_llm_app .
```

Then the app can be viewed through:
```
docker run -p 8050:8050 -e OPENAI_API_KEY=*** data_llm_app
```
where `OPENAI_API_KEY` must be set if the OpenAI model to be used. Otherwise the local LLM must be set:
```
docker run -p 8050:8050 -v <LOCAL_LLM_DIR>:/app/hf_models data_llm_app
```
where `LOCAL_LLM_DIR` is the directory with all downloaded models. For example, `docker run -p 8050:8050 -v /Users/sijinzhang/Github/data_llm/hf_models:/app/hf_models data_llm_app`

The container can be debugged via: 
```
docker run -it -v hf_models:/app/hf_models --rm data_llm_app /bin/bash
```



## Choosing a LLM model
You can choose using an OpenAI model (by default, `gpt-4o-mini` is used) or a set of local models.

### Using OpenAI API
Using a local LLM model demands substantial computational resources. However, this package also supports the use of models like OpenAI's GPT-4. It's important to note that the OpenAI model will only be utilized to generate code for extracting insights from the data; it does not interact directly with the data itself, ensuring that data privacy remains fully protected.

In order to use OpenAI model, the environment variable `OPENAI_API_KEY` must be set.

### Using local LLAMA model

If `OPENAI_API_KEY` is not set, local LLAMA models must be provided.

The script is provided to download and postprocess any HF models at ``etc/download_hf_models/download_models.py``

Note that you will have to download ``https://github.com/ggerganov/llama.cpp`` to convert the downloaded model to the `GGUF` format

By default, the following models will be downloaded (can be edttied within ``download_models.py``):

- BAAI/bge-small-en-v1.5
- codellama/CodeLlama-7b-Instruct-hf
- meta-llama/Llama-3.2-3B-Instruct

The environment variable ``HF_TOKEN`` must be set in order to download any models from Huggingface, e.g., ``export HF_TOKEN=xxxx``. 

Note that you will have to download ``https://github.com/ggerganov/llama.cpp`` to convert the downloaded model to the `GGUF` format. 
The repository path must be set through ``export LLAMA_CPP_DIR=xxx``.

In a nutshell, the local LLAMA model can be set up by:

```
export HF_TOKEN=***
export LLAMA_CPP_DIR=***
download_models.py --download_model --convert_odel
```
