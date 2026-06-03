FROM nvidia/cuda:12.8.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential cmake git python3 python3-pip libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Créer le lien symbolique vers libcuda stub AVANT le build
RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/libcuda.so.1

RUN git clone https://github.com/ggerganov/llama.cpp && \
    cd llama.cpp && \
    cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=120 && \
    cmake --build build --target llama-server -j$(nproc) && \
    cp build/bin/llama-server /usr/local/bin/ && \
    rm -rf /llama.cpp && \
    rm /usr/local/cuda/lib64/libcuda.so.1

RUN pip3 install runpod requests

COPY handler.py /handler.py

CMD ["python3", "/handler.py"]
