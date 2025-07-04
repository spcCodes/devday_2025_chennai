from typing_extensions import TypedDict


# Graph state
class State(TypedDict):

    topic: str
    joke: str
    story: str
    poem: str
    combined_output: str