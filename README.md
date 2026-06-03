# DeepSeek-V3.1 sur RunPod Serverless (quantization 1-bit)

Handler RunPod serverless minimal pour faire tourner DeepSeek-V3.1 
(671B paramètres, quantizé en TQ1_0 via Unsloth dynamic quants) 
avec llama.cpp.

## Pourquoi
Je voulais expérimenter le déploiement de modèles frontier sur du 
hardware accessible. Les quants 1-bit d'Unsloth font tenir DeepSeek-V3.1 
dans ~150 Go, ce qui le rend exécutable sur un seul nœud H100/A100 
avec les experts MoE offloadés sur CPU.

## Comment ça marche
- `llama-server` (llama.cpp) sert le modèle sur le port 8080
- Les experts FFN du MoE sont offloadés sur CPU (`-ot ffn_.*_exp=CPU`) 
  pour tenir dans la VRAM
- Le handler RunPod proxy les requêtes au format OpenAI (chat/completion)
- Fallback sur Qwen2.5-0.5B-Instruct pour tester en local quand le 
  volume DeepSeek n'est pas monté

## Statut
POC fonctionnel. Pas production-grade (pas de streaming, pas de batching, 
gestion d'erreurs minimaliste si llama-server crash).

## Stack
- RunPod serverless
- llama.cpp (llama-server)
- DeepSeek-V3.1 UD-TQ1_0 quants (Unsloth)
