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

### Building docker:
Build the container:
```
docker build -t data_llm_app .
```

View the container:
```
docker run -p 8050:8050 my_dash_app
```
