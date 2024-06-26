import streamlit as st
import os
from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from langchain_openai import ChatOpenAI
import sys
from io import StringIO

st.set_page_config(page_title="Research Assistant", page_icon="📚")

# Set up environment variables
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["SERPER_API_KEY"] = "Your API Key"

# Initialize LLM
llm = ChatOpenAI(
    model="crewai-llama3-8b",
    base_url="http://localhost:11434/v1",
    api_key="NA")

# Define tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Define agents (same as before)
researcher = Agent(
    role="Researcher",
    goal="Gather comprehensive and relevant information on {topic}",
    backstory="You're a diligent researcher tasked with collecting information "
              "on the topic: {topic}. You use various sources including academic "
              "databases, websites, and other platforms to gather relevant data. "
              "You're skilled at identifying key sources and extracting pertinent "
              "information. Your work forms the foundation for the entire research process.",
    tools=[search_tool, scrape_tool],
    allow_delegation=False,
    llm=llm,
    verbose=True
)

fact_checker = Agent(
    role="Fact Checker",
    goal="Verify the accuracy of collected information on {topic}",
    backstory="You're a meticulous fact-checker responsible for ensuring the "
              "accuracy of information gathered on: {topic}. You cross-reference "
              "data from multiple sources, flag inconsistencies or potential "
              "misinformation, and rate the reliability of sources. Your work is "
              "crucial for maintaining the integrity of the research.",
    tools=[search_tool, scrape_tool],
    allow_delegation=False,
    llm=llm,
    verbose=True
)

summarizer = Agent(
    role="Summarizer",
    goal="Create concise summaries of the collected information on {topic}",
    backstory="You're an expert at distilling complex information into clear, "
              "concise summaries. Your task is to take the verified information "
              "on {topic} and create brief, easy-to-understand summaries. You "
              "identify and extract key points and main ideas, making the "
              "research accessible to a wider audience.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

organizer = Agent(
    role="Organizer",
    goal="Structure and categorize the research information on {topic}",
    backstory="You're a skilled information architect tasked with organizing "
              "the research on {topic}. You create a logical structure for the "
              "information, develop categories and tags for easy navigation, "
              "and identify relationships between different pieces of data. "
              "Your work makes the research coherent and easily navigable.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

note_taker = Agent(
    role="Note Taker",
    goal="Compile clear, concise notes from the processed information on {topic}",
    backstory="You're an efficient note-taker responsible for creating the final "
              "research notes on {topic} in markdown. You compile the processed information "
              "into a standardized format, creating clear, concise notes based on "
              "the summarized and organized content. You generate bullet points, "
              "short paragraphs, or other easily digestible formats, and incorporate "
              "citations and references as needed.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)
# ... (other agents remain the same)

# Define tasks (same as before)
research = Task(
    description=(
        "1. Search for comprehensive information on {topic} from various sources.\n"
        "2. Prioritize recent and relevant academic papers, news articles, and expert opinions.\n"
        "3. Gather data on key concepts, current trends, and significant developments.\n"
        "4. Identify and collect information from primary sources when possible.\n"
        "5. Compile a list of key terms and their definitions related to {topic}.\n"
        "6. Record all sources used for later reference and citation."
    ),
    expected_output="A comprehensive collection of raw data and information on {topic}, "
                    "including source links, key terms, and initial insights.",
    agent=researcher
)

fact_check = Task(
    description=(
        "1. Review all information gathered by the Researcher on {topic}.\n"
        "2. Cross-reference data points with multiple reliable sources.\n"
        "3. Identify and flag any inconsistencies or potential misinformation.\n"
        "4. Verify the credibility of sources used in the research.\n"
        "5. Rate the reliability of each piece of information on a scale of 1-5.\n"
        "6. Provide brief explanations for any information flagged as questionable."
    ),
    expected_output="A fact-checked version of the research data, with reliability ratings "
                    "and explanations for any flagged information.",
    context=[research],
    agent=fact_checker
)

summarize = Task(
    description=(
        "1. Review the fact-checked information on {topic}.\n"
        "2. Identify the most important and relevant points.\n"
        "3. Create concise summaries of key concepts and findings.\n"
        "4. Highlight any significant trends or patterns in the data.\n"
        "5. Ensure that summaries are clear and accessible to a general audience.\n"
        "6. Maintain the essence of the original information while condensing it."
    ),
    expected_output="A set of clear, concise summaries of the key information on {topic}, "
                    "highlighting the most important points and trends.",
    context=[research, fact_check],
    agent=summarizer
)

organize = Task(
    description=(
        "1. Review the summarized information on {topic}.\n"
        "2. Create a logical structure for organizing the research content.\n"
        "3. Develop categories and subcategories to group related information.\n"
        "4. Identify relationships and connections between different pieces of information.\n"
        "5. Create a tagging system for easy navigation of the research material.\n"
        "6. Ensure the organization allows for easy expansion as new information is added."
    ),
    expected_output="A well-structured outline of the research on {topic}, with clear categories, "
                    "tags, and identified relationships between different elements.",
    context=[fact_check, summarize],
    agent=organizer
)

take_notes = Task(
    description=(
        "1. Review the organized and summarized information on {topic}.\n"
        "2. Create clear, concise notes in a standardized format.\n"
        "3. Use bullet points, short paragraphs, or other easily digestible formats.\n"
        "4. Incorporate key terms, definitions, and important concepts.\n"
        "5. Include relevant citations and references for each piece of information.\n"
        "6. Ensure notes are comprehensive yet easy to understand and review."
    ),
    expected_output="A set of well-formatted, comprehensive notes on {topic}, including key points, "
                    "definitions, and properly cited sources in a markdown file.",
    output_file="notes.md",
    context=[research, fact_check, organize],
    agent=note_taker
)
# ... (other tasks remain the same)

# Create the Crew
note_taking_crew = Crew(
    agents=[researcher, fact_checker, summarizer, organizer, note_taker],
    tasks=[research, fact_check, summarize, organize, take_notes],
    verbose=True
)

# Streamlit app
st.title("Research Assistant👨‍🎓")

# User input
topic = st.text_input("Enter your research topic:")

if st.button("Start Research"):
    if topic:
        with st.spinner("Researching... This may take a few minutes."):
            # Capture console output
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            result = note_taking_crew.kickoff(inputs={"topic": topic})

            # Get the console output and restore stdout
            console_output = sys.stdout.getvalue()
            sys.stdout = old_stdout

        st.success("Research complete!")

        # Display console logs
        st.header("Agent Thoughts and Process")
        st.text_area("Console Logs", console_output, height=300)

        # Display organized content
        st.header("Organized Content")
        st.markdown(result)

        # Provide download link for markdown notes
        with open("notes.md", "r") as f:
            notes_content = f.read()

        st.download_button(
            label="Download Markdown Notes",
            data=notes_content,
            file_name="research_notes.md",
            mime="text/markdown"
        )
    else:
        st.warning("Please enter a topic before starting the research.")
