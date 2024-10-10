# data_llm


### Creating the data_llm environment
```
conda env create -f env.yml
```

### Start the application
```
python app.py
```

### Using local LLAMA model
The script is provided to download and postprocess any HF models at ``etc/download_hf_models/download_models.py``

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

### Using OpenAI API
Using a local LLM model demands substantial computational resources. However, this package also supports the use of models like OpenAI's GPT-4. It's important to note that the OpenAI model will only be utilized to generate code for extracting insights from the data; it does not interact directly with the data itself, ensuring that data privacy remains fully protected.

