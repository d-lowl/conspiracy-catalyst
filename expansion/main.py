import time

from loguru import logger

from expansion.follower.follower import blogger
from expansion.game import Game

game = Game()

def simulate(tweet: str):
    try:
        start_time = time.time()
        turn = game.make_turn(tweet)
        print(turn)
        finish_time = time.time()
        print(f"Generated in {int(finish_time-start_time)} seconds.")
        print()
    except ValueError as e:
        if "Bad Gateway" in str(e):
            logger.error("Inference endpoint is down, wait for 1 minute.")
            raise Exception("Inference endpoint is down, wait for 1 minute.")

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
    simulate("Bloggers are stupid")


if __name__ == '__main__':
    test()
