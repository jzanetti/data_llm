from huggingface_hub import snapshot_download
from os import getenv, makedirs, system
from os.path import join, exists
from argparse import ArgumentParser, BooleanOptionalAction


MODELS = [
    #"BAAI/bge-small-en-v1.5",
    #"codellama/CodeLlama-7b-Instruct-hf"
    "meta-llama/Llama-3.2-3B-Instruct"
]

def download_models(workdir: str):
    for model_id in MODELS:
        proc_dir = join(workdir, model_id)

        if not exists(proc_dir):
            makedirs(proc_dir)

        print(f"Start downloading: {model_id}")
        snapshot_download(
            repo_id=model_id,
            local_dir=proc_dir,
            local_dir_use_symlinks=False,
            revision="main",
            token=getenv("HF_TOKEN"),
        )


def convert_model(workdir: str, llama_cpp_dir: str="etc/llama.cpp"):
    script_path = join(llama_cpp_dir, "convert-hf-to-gguf.py")
    for model_id in MODELS:
        proc_cmd = f"{script_path} --model {join(workdir, model_id)} --outfile {join(workdir, model_id) + '.gguf'}"
        print(proc_cmd)
        system(proc_cmd)



if __name__ == "__main__":
    parser = ArgumentParser(description="Creating NZ data")

    parser.add_argument(
        "--workdir",
        type=str,
        required=False,
        default="hf_models",
        help="Working directory",
    )

    parser.add_argument("--download_model", action=BooleanOptionalAction)
    parser.add_argument("--convert_model", action=BooleanOptionalAction)

    args = parser.parse_args(["--download_model", "--convert_model"])  

    if args.download_model:
        download_models(args.workdir)

    if args.convert_model:
        convert_model(args.workdir)
