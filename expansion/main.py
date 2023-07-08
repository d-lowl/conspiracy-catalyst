import time

from langchain import PromptTemplate, LLMChain, HuggingFacePipeline

import torch
from transformers import pipeline

generate_text = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16,
                         trust_remote_code=True, device_map="auto", return_full_text=True)

llm = HuggingFacePipeline(pipeline=generate_text)

principles = [
    "You are an aspiring influencer",
    "You want exciting things",
    "You want things that make *you* more visible",
    "You are against the current ruling political party"
]

formatted_principles = "\n".join([f"- {x}" for x in principles])

template = "You are an aspiring influencer who is interested in occult stuff.\n" \
           "You are insterested in the secret society that posted the following message.\n" \
           "However you have certain princles:\n" \
           "{principles}\n" \
           "\n" \
           "Write a SHORT reply (you can agree or disagree) to the following tweet: \n{tweet}"

prompt = PromptTemplate(
    template=template,
    input_variables=["principles", "tweet"],
)

reply_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)


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
