# For each agent: 
#   1. Role
#   2. Goal
#   3. Backstory = Context

# https://docs.crewai.com/en/concepts/tools

# serper api key : for google seaarch into many websites
#                 https://serper.dev/api-keys

# llama-3.3-70b-versatile: open-source llm
#                 https://console.groq.com/playground?model=llama-3.3-70b-versatile

from dotenv import load_dotenv
import os
# from langchain_groq import ChatGroq
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

load_dotenv()

llm = LLM(
            model="groq/llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
                    )

search_tool = SerperDevTool()

researcher = Agent(
    role="Senior Research Analyst",
    
    goal="Extract the most important points about a given topic and retrieve the top 10 insights",
    
    backstory="""You are an expert researcher at 3AI Company.
                You have years of experience searching the internet,
                filtering the most credible sources,
                and extracting key insights from complex topics.""",
                
    llm = llm,
    tools = [search_tool]
)

writer = Agent(
    role="Professional Content Writer",
    
    goal="Write a well-organized report about a given topic based on research findings",
    
    backstory="""You are a skilled writer at 3AI Company.
                You specialize in transforming raw research into 
                clear, engaging, and beautifully structured reports.""",
    
    llm = llm,
)

# الـ writer هيكتب التقرير بناءً على إيه؟
# ← على المعلومات اللي جمعها الـ researcher!

def run_research_crew(task: str, output_format: str):
    search = Task(
        description = f'Search and research about {task}',
        expected_output = 'Top 10 key insights about the topic',
        agent = researcher
    )

    write = Task(
        description = f'Write a {output_format} about {task}',
        expected_output = 'Well-organized report based on research',
        agent = writer,
        output_file = 'reports/report.md',
        context = [search],
    )

    crew = Crew(
        agents = [researcher, writer],
        tasks = [search, write]
    )
    
    return crew.kickoff()

