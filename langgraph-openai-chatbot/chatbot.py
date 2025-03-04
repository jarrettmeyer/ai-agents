import os

from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from typing import Annotated
from typing_extensions import TypedDict
from uuid import uuid4


load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

# Define a search tool. The LLM can use this to query the web.
search_results = TavilySearchResults(
    max_results=int(os.getenv("TAVILY_MAX_RESULTS", "2")),
)

# Define the LLM.
llm = ChatOpenAI(
    model=os.getenv("LLM_MODEL"),
)

# Attach tools to the LLM.
llm_with_tools = llm.bind_tools([search_results])


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[search_results])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

memory_config = {"configurable": {"thread_id": str(uuid4())}}


def stream_graph_updates(user_input: str):
    events = graph.stream(
        input={"messages":  [{"role": "user", "content": user_input}]},
        config=memory_config,
        stream_mode="values",
    )
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()


def main():
    while True:
        try:
            user_input = input("\nUser (q to quit): ")
            if user_input.lower() in ["exit", "q", "quit"]:
                print("Goodbye!")
                return None

            stream_graph_updates(user_input)
        except Exception as e:
            print("Error:", e)
            return None


if __name__ == "__main__":
    main()
