import math
from typing import List

from loguru import logger

from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFaceEndpoint
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

template = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n" \
           "### Instruction:\n" \
           "You are potentially interested in the secret society " \
           "that is posting on Critter (the social media website).\n" \
           "{description}\n" \
           "You have certain needs:\n" \
           "{principles}\n" \
           "\n" \
           "Write a SHORT reply (you can agree or disagree) to the following forum post: \n{tweet}\n" \
           "### Response:\n"


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class FollowerResponse(BaseModel):
    reply: str
    sentiment: float
    follower_gain: int


class Follower:
    def __init__(self, description: str, principles: List[str]):
        self.llm = HuggingFaceEndpoint(
            endpoint_url="https://mm0houka94uuvk3b.eu-west-1.aws.endpoints.huggingface.cloud",
            task="text-generation",
            model_kwargs={
                "return_full_text": True,
                "max_new_tokens": 32,
                "temperature": 0.9,
                "repetition_penalty": 2.0,
                # "length_penalty": -2.0,
                "top_p": 0.92,
                "top_k": 5,
                # "eos_token_id": 50277,
            }
        )
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["description", "principles", "tweet"],
        )
        self.reply_chain = LLMChain(prompt=self.prompt, llm=self.llm, verbose=False)

        self.sentiment_analyser = SentimentIntensityAnalyzer()

        self.short_description = description
        self.formatted_principles = "\n".join([f"- {x}" for x in principles])

    def simulate(self, tweet: str) -> FollowerResponse:
        logger.info(f"Post: {tweet}")
        reply = self.reply_chain.run(
            tweet=tweet,
            description=self.short_description,
            principles=self.formatted_principles
        ).split("\n\n")[0].strip() + "..."
        logger.info(f"Reply: {reply}")
        sentiment = self.sentiment_analyser.polarity_scores(reply)["compound"]
        logger.info(f"Sentiment: {sentiment}")
        follower_gain = int(10*(sigmoid(5*(sentiment - 0.6))-0.5))
        logger.info(f"Follower gain: {follower_gain}")
        return FollowerResponse(
            reply=reply,
            sentiment=sentiment,
            follower_gain=follower_gain
        )


blogger = Follower(
    description="You are an aspiring blogger who is interested in occult stuff.",
    principles=[
        "You are an aspiring blogger",
        "You want exciting things",
        "You want things that make *you* more visible",
        "You are up for everything hype-generating"
    ]
)