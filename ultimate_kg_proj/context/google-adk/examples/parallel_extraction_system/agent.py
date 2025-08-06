# Conceptual Code: Parallel Information Gathering
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent, BaseAgent
from google.adk.tools.agent_tool import AgentTool
from kg_broker_agent_facts.agent import root_agent as kg_broker_facts_agent
from kg_broker_agent_gaps.agent import root_agent as kg_broker_gaps_agent
from .schemas import FactsGapsOutput


fact_extractor_agent = LlmAgent(
    name="fact_extractor",
    instruction="""
    Extract all clear, verifiable facts from the user's message. 
    Return only a JSON array of strings, with each string being a single fact.
    Do not include any explanation, metadata, or formatting outside the array.

    Example:
    Input: "Ilya is 34 and lives in Tel Aviv. I want to buy a vineyard."
    Output: ["Ilya is 34", "Ilya lives in Tel Aviv", "User wants to buy a vineyard"]
    """,
    output_key="facts",
    output_schema=FactsGapsOutput,
    model="gemini-2.5-flash"
)

fact_handling_workflow = SequentialAgent(
    name="FactHandlingWorkflow",
    sub_agents=[fact_extractor_agent, kg_broker_facts_agent]
)

gaps_extractor = LlmAgent(
    name="gaps_extractor",
    instruction="""
Your role is to identify **knowledge gaps** in the user's message—things we don't yet know, but would help us better understand the context, extract more useful data, or enrich the user's knowledge graph.

Return a **JSON array of gaps**, each targeting a specific piece of missing or unclear information that would help us:

❗Format:
Only return a **valid JSON array** of questions.
No explanation. No extra text. Output **must start with `[` and end with `]`**.

Example:
Input: "I met Ilya to talk about Hydra."
Output:
[
  "Who is Ilya to the user?",
  "What is Hydra about?",
  "When did this meeting take place?",
  "Where did they meet?",
  "Did anyone else join the meeting?"
]

Be thorough. Ask everything that might be useful to a system that wants to learn as much as possible about the user and their world.
""",
    output_key="gaps",
    output_schema=FactsGapsOutput,
    model="gemini-2.0-flash"
)

gaps_handling_workflow = SequentialAgent(
    name="GapsHandlingWorkflow",
    sub_agents=[gaps_extractor, kg_broker_gaps_agent]
)

gather_concurrently = ParallelAgent(
    name="ConcurrentFetch",
    sub_agents=[fact_handling_workflow, gaps_handling_workflow]
)

synthesizer = LlmAgent(
    name="Synthesizer",
    instruction=(
        "Combine results from state keys {facts}, and {gaps}. Gaps are the result of a search for the answer to the questions in a graph database - "
        "Return the combined an d nicely arranged list of facts and gaps for the orchestrator agent to use in its reply to the user."
    ),
    include_contents="default",
    model="gemini-2.5-flash"
)

overall_processing_workflow = SequentialAgent(
    name="FetchAndSynthesize",
    sub_agents=[gather_concurrently, synthesizer]  # Run parallel fetch, then synthesize
)

root_agent = overall_processing_workflow
processing_agent_tool = AgentTool(agent=root_agent)

# fetch_api1 and fetch_api2 run concurrently, saving to state.
# synthesizer runs afterwards, reading state['api1_data'] and state['api2_data'].