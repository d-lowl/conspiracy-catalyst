from typing import List

from pydantic import BaseModel

from expansion.follower.follower import blogger, FollowerResponse


class TurnResults(BaseModel):
    message_id: int
    responses: List[FollowerResponse]
    total_follower_gain: int
    followers: int

class Game:
    followers: int = 3

    def __init__(self):
        ...

    def make_turn(self, message_id: int, tweet: str):
        responses = [blogger.simulate(tweet) for i in range(3)]
        total_follower_gain = sum([response.follower_gain for response in responses])
        total_followers = self.followers + total_follower_gain
        if total_followers < 1:
            self.followers = 1
        else:
            self.followers = total_followers

        return TurnResults(
            message_id=message_id,
            responses=responses,
            total_follower_gain=total_follower_gain,
            followers=self.followers
        )


