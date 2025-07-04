from models import State, Route
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

router = llm.with_structured_output(Route)

# Nodes
def write_story(state: State):
    """Write a story"""

    print("Write a story")
    result = llm.invoke("Write a story based on this topic: " + state["input"])
    return {"output": result.content}


def write_joke(state: State):
    """Write a joke"""

    print("Write a joke")
    result = llm.invoke("Write a joke based on this topic: " + state["input"])
    return {"output": result.content}


def write_poem(state: State):
    """Write a poem"""

    print("Write a poem")
    result = llm.invoke("Write a poem based on this topic: " + state["input"])
    return {"output": result.content}


def route_decision(state: State):
    """Route the input to the appropriate node"""

    # Run the augmented LLM with structured output to serve as routing logic
    result = router.invoke(
        [
            SystemMessage(
                content="Route the input to story, joke, or poem based on the user's request."
            ),
            HumanMessage(content=state["input"]),
        ]
    )

    return {"decision": result.step}


# Function to determine the next node based on the routing decision
def get_next_node(state: State):
    # Return the node name you want to visit next
    if state["decision"] == "story":
        return "write_story"
    elif state["decision"] == "joke":
        return "write_joke"
    elif state["decision"] == "poem":
        return "write_poem"
    
