# Research Assistant 🤖📚

This Streamlit-based application serves as an AI-powered Research Assistant, capable of performing a quick research on any given topic.

![main](https://github.com/ranveer0323/Research-Assistance-AI-Crew/assets/105062270/fecaa284-57a1-438f-9b58-4f78fca5d64c)

## About the Program

The Research Assistant uses a crew of AI agents to conduct thorough research:

1. 🔍 **Researcher**: Gathers comprehensive information on the topic.
2. ✅ **Fact Checker**: Verifies the accuracy of collected information.
3. 📝 **Summarizer**: Creates concise summaries of the information.
4. 🗂️ **Organizer**: Structures and categorizes the research information.
5. 📓 **Note Taker**: Compiles clear, concise notes in markdown format.

These agents work together using the CrewAI framework to produce a well-researched, organized, and summarized output on the given topic.

## The Crew Concept 👥

The application leverages the concept of a "crew" - a team of AI agents with distinct roles and responsibilities. Each agent in the crew is specialized in a particular aspect of the research process. By working together, they can accomplish complex research tasks more effectively than a single, general-purpose AI.

The crew approach allows for:
- Specialized focus on different aspects of research
- Cross-verification and fact-checking
- Structured organization of information
- Comprehensive yet concise final output

## Running the Application 🚀

To run the Streamlit app, use the following command in your terminal:
streamlit run crew_app.py

This will start the Streamlit server, and you can access the Research Assistant through your web browser.

## Usage 📋

1. Enter your research topic in the provided text field.
2. Click "Start Research" to begin the process.
3. Wait for the agents to complete their tasks.
4. Review the results, including agent thoughts and organized content.
5. Download the markdown notes for a complete record of the research.

Note: Ensure you have set up the necessary environment variables and dependencies before running the application.
