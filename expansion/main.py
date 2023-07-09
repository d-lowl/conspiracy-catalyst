import time

from langchain import PromptTemplate, LLMChain, HuggingFacePipeline, HuggingFaceHub
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint

import torch
from transformers import pipeline

# generate_text = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16,
#                          trust_remote_code=True, device_map="auto", return_full_text=True)
#
# llm = HuggingFacePipeline(pipeline=generate_text)

# llm = HuggingFaceHub(repo_id="databricks/dolly-v2-3b")
llm = HuggingFaceEndpoint(
    endpoint_url="https://mm0houka94uuvk3b.eu-west-1.aws.endpoints.huggingface.cloud",
    task="text-generation",
    model_kwargs={
        "return_full_text": True,
        "max_new_tokens": 256,
        "temperature": 0.7,
        "repetition_penalty": 2.0,
        "length_penalty": -1.0,
        # "diversity_penalty": 0.0,
        # "typical_p": 1.0,
        "top_p": 0.92,
        "top_k": 5,
        "eos_token_id": 50277,
    }
)

principles = [
    "You are an aspiring influencer",
    "You want exciting things",
    "You want things that make *you* more visible",
    "You are against the current ruling political party"
]

formatted_principles = "\n".join([f"- {x}" for x in principles])

template = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n" \
           "### Instruction:\n" \
           "You are an aspiring influencer who is interested in occult stuff.\n" \
           "You are potentially interested in the secret society that was posted on Critter (the social media website).\n" \
           "However you have certain principles:\n" \
           "{principles}\n" \
           "\n" \
           "Write a SHORT reply (you can agree or disagree) to the following forum post: \n{tweet}\n" \
           "### Response:\n"

prompt = PromptTemplate(
    template=template,
    input_variables=["principles", "tweet"],
)

reply_chain = LLMChain(prompt=prompt, llm=llm, verbose=False)


def simulate(tweet: str):
    start_time = time.time()
    print(f"Cult: {tweet}")
    reply = reply_chain.run(
        tweet=tweet,
        principles=formatted_principles
    )
    print(f"Reply: {reply}")
    finish_time = time.time()
    print(f"Generated in {int(finish_time-start_time)} seconds.")
    print()


def test():
    simulate("We do our rites every Wed, do not miss out!")
    simulate("We must bring the head of the mayor as a sacrifice for our needs!")
    simulate("To bring THE SOCIETY forward, you must hide yourself and never show your face")
    simulate("""Ready to unlock the mysteries of the universe? Discover the secrets that lie beyond the ordinary? Become part of a hidden lineage that has shaped history? Look no further! Join the #Illuminati and embrace your journey of enlightenment. 🌟✨

💡 Gain access to ancient knowledge.
💪 Harness your true potential.
🌍 Influence global affairs.
🔒 Secrecy is our shield.""")
    simulate("""Looking to waste your time with cryptic symbols and secret handshakes? Want to be part of a shadowy organization that keeps you in the dark? Look elsewhere! The #Illuminati offers nothing but empty promises and nonsensical rituals. 👎👀

❌ No real power or influence.
❌ No ancient secrets revealed.
❌ No path to enlightenment.
❌ No significance in global affairs.""")


if __name__ == '__main__':
    test()
