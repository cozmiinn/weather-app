import os

from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import ChatOpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = "<YOUR-API-KEY-HERE>"
os.environ["SERPER_API_KEY"] = "<YOUR-API-KEY-HERE>"

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
