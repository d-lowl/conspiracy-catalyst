from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenLLM

server_url = "http://localhost:3000"

llm = OpenLLM(server_url=server_url)

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
           "Write a reply (positive or negative you decide) to the following tweet: {tweet}"

prompt = PromptTemplate(template=template, input_variables=["principles", "tweet"])

reply_chain = LLMChain(prompt=prompt, llm=llm)


def simulate(tweet: str):
    print(f"Cult: {tweet}")
    reply = reply_chain.run(
        tweet=tweet,
        principles=formatted_principles
    )
    print(f"Reply: {reply}")
    print()


def test():
    simulate("We do our rites every Wed, do not miss out!")
    simulate("We must bring the head of the mayor as a sacrifice for our needs!")
    simulate("To bring THE SOCIETY forward, you must hide yourself and never show your face")


if __name__ == '__main__':
    test()
