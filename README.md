# Conspiracy Catalyst
This repo is for the game made for the [Open Source AI Game Jam](https://itch.io/jam/open-source-ai-game-jam).

Itch.io page: [https://dlowl.itch.io/conspiracy-catalyst](https://dlowl.itch.io/conspiracy-catalyst)

Important notes:
* This repo is unlikely to be updated, the project will persist as is after the jam is finished
* I'm paying for the inference endpoint out of my own pocket -> I will bring it down, when the costs build up too much

## Requirements
* python 3.11
* poetry>=1.5.1

## How to run it
### LLM
To run the game, you need a deployed Huggingface Inference Endpoints (see [their documentation](https://huggingface.co/docs/inference-endpoints/index) on how to do it). The live version uses:
* [Fork of dolly-v2-3b](https://huggingface.co/dlowl/dolly-v2-3b-endpoint) model, that works with Inference Endpoints
* GPU small instance on Inference Endpoints

The link *is hardcoded* [here](https://github.com/d-lowl/conspiracy-catalyst/blob/8e5b110079c329d6f5c51d5d22b3ccad1f46f137/expansion/follower/follower.py#L36)

### Local server
Run:
```
poetry install
HUGGINGFACEHUB_API_TOKEN=<your token> python expansion/socketio/server.py
```

Visit [http://0.0.0.0:8000/](http://0.0.0.0:8000/)
