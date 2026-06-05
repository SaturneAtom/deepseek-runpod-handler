# DeepSeek-V3.1 on RunPod Serverless (1-bit Quantized)

Minimal RunPod Serverless deployment for DeepSeek-V3.1 (671B parameters), quantized using Unsloth Dynamic Quants (TQ1_0) and served through llama.cpp.

## Why

This project explores whether frontier-scale Mixture-of-Experts models can be deployed on accessible GPU infrastructure using aggressive quantization and CPU expert offloading.

The goal was to minimize hardware requirements while keeping the model usable through a standard OpenAI-compatible API.

## Architecture

* `llama-server` (llama.cpp) serves the model on port 8080.
* MoE FFN experts are offloaded to CPU using:

  * `-ot ffn_.*_exp=CPU`
* A lightweight RunPod Serverless handler proxies requests to the model.
* OpenAI-compatible `/chat/completions` interface.
* Development to `Qwen2.5-0.5B-Instruct` when the DeepSeek volume is not mounted.

## Technical Notes

This project explores the practical limits of serving frontier-scale MoE models through aggressive quantization and CPU expert offloading.

## Status

Proof of Concept (POC).

Current limitations:

* No streaming support
* No batching
* Minimal crash recovery if `llama-server` exits
* No production monitoring

## Stack

* RunPod Serverless
* llama.cpp (`llama-server`)
* DeepSeek-V3.1 UD-TQ1_0 (Unsloth Dynamic Quants)
* OpenAI-compatible API wrapper

