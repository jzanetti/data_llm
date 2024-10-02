# data_llm


### Creating the data_llm environment
```
conda env create -f env.yml
```

### Start the application
```
python app.py
```

### Download local LLAMA model
The script is provided to download and postprocess any HF models at ``etc/download_hf_models/download_models.py``

Note that you will have to download ``https://github.com/ggerganov/llama.cpp`` to convert the downloaded model to the `GGUF` format