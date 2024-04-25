import os

from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import ChatOpenAI
from langsmith.run_helpers import traceable
import streamlit as st


@traceable()
def weather_app():
    os.environ["OPENAI_API_KEY"] = "<YOUR_API_KEY>"
    os.environ["SERPER_API_KEY"] = "<YOUR_API_KEY>"
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "<YOUR_API_KEY>"
    os.environ["LANGCHAIN_API_KEY"] = "<YOUR_API_KEY>"
    os.environ["LANGCHAIN_PROJECT"] = "<YOUR_PROJECT_NAME>"

    prompt = hub.pull("hwchase17/react")
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
    search = GoogleSerperAPIWrapper()
    tools = [
        Tool(
            name="Immediate Answer",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    st.write("Weather App")
    response_input = st.text_input(label='Ask about a weather related question')
    if response_input:
        response = agent_executor.invoke({"input": response_input})
        st.write(response['output'])


weather_app()
