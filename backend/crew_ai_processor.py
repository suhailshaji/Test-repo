"""
This module defines the CrewAI agents, tasks, and crew responsible for generating
software proposals based on user-provided requirements documents.

It utilizes OpenAI models via CrewAI to perform a sequence of tasks:
1. Clarifying requirements from the input document.
2. Drafting a development proposal.
3. Drafting a technical proposal.
4. Compiling all information into a final, structured proposal.

The main entry point for using this module is the `run_crew` function,
which takes the content of a requirements document and returns a structured
proposal dictionary or an error dictionary.
"""
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI # Corrected import

# Load environment variables from .env file
load_dotenv()

# Default LLM
# Initialize the LLM, loading the API key and model name from environment variables
# Ensure OPENAI_API_KEY and OPENAI_MODEL_NAME are set in your .env file
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name=os.getenv("OPENAI_MODEL_NAME") if os.getenv("OPENAI_MODEL_NAME") else "gpt-4-turbo" # Default to gpt-4-turbo if not set
)

# --- AGENT DEFINITIONS ---
# Each agent is configured with a specific role, goal, and backstory to guide the LLM's behavior.
# `allow_delegation=False` means agents work independently on their assigned tasks.
# `verbose=True` provides detailed output during execution for debugging and observation.

# Agent 1: Requirements Clarifier
# This agent focuses on understanding and structuring the initial input.
requirements_clarifier_agent = Agent(
    role="Requirements Analysis Specialist",
    goal="To meticulously analyze provided software requirements documents, identify core functionalities, non-functional requirements, and any ambiguities. The aim is to produce a clear, concise summary of actionable requirements for proposal generation.",
    backstory=(
        "An experienced business analyst renowned for their ability to dissect complex client needs "
        "and translate them into unambiguous, actionable requirements. With a keen eye for detail, "
        "they ensure that the foundation for any project is solid and well-understood, "
        "preventing misinterpretations downstream."
    ),
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# Agent 2: Development Proposal Agent
# This agent takes the clarified requirements and focuses on the 'what' and 'when' of the project.
development_proposal_agent = Agent(
    role="Software Development Strategist",
    goal="To create a comprehensive development proposal, including scope of work, key features, potential timeline, and key deliverables, based on clarified software requirements.",
    backstory=(
        "A seasoned project manager and software strategist with extensive experience in planning complex software projects. "
        "They excel at transforming clarified requirements into realistic and compelling development plans, "
        "outlining a clear path from concept to deployment."
    ),
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# Agent 3: Technical Proposal Agent
# This agent focuses on the 'how' of the project, based on requirements and the development plan.
technical_proposal_agent = Agent(
    role="Solutions Architect",
    goal="To devise a detailed technical proposal, including system architecture, technology stack recommendations, and deployment strategy, aligned with the software requirements and development plan.",
    backstory=(
        "A senior systems architect with a broad and deep understanding of modern technologies and architectural best practices. "
        "They specialize in designing scalable, robust, and secure software solutions that precisely meet project needs "
        "and ensure long-term viability."
    ),
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# Agent 4: Proposal Compilation Agent
# This agent acts as the final assembler and editor, ensuring the proposal is coherent and follows the template.
proposal_compilation_agent = Agent(
    role="Lead Technical Writer and Proposal Editor",
    goal="To synthesize all inputs (clarified requirements, development proposal, technical proposal) into a single, coherent, professionally written software proposal document, adhering to a standard template.",
    backstory=(
        "A meticulous technical writer and editor, skilled in transforming technical details and planning documents "
        "into clear, persuasive, and impeccably structured proposals. They ensure that the final document is "
        "not only comprehensive but also easy to understand and compelling for the client."
    ),
    llm=llm,
    allow_delegation=False, # Could be True if sub-editing tasks were delegated
    verbose=True
)

# --- TASK DEFINITIONS ---
# Each task is defined with a clear description of what needs to be done and
# an expected output format to guide the LLM. Tasks are assigned to specific agents.
# The placeholder `'{requirements_document_content}'` in the first task's description
# will be filled by the input provided to `crew.kickoff()`.
# Subsequent tasks can use placeholders like `'{task_name.output}'` or rely on CrewAI's
# automatic context passing if the task output is a simple string and the next task's
# description implies its use. For more complex data structures or explicit control,
# the `context` parameter in the Task constructor would be used.

# Task 1: Clarify Requirements
# Input: Raw requirements document content.
# Output: Structured summary of requirements, ambiguities, and goals.
clarify_requirements_task = Task(
    description=(
        "Analyze the following software requirements document: '{requirements_document_content}'. "
        "Extract key functional and non-functional requirements. "
        "Identify and list any ambiguities or points needing further clarification that might hinder proposal generation. "
        "Produce a concise summary of the core requirements. Focus on clarity and actionability for the next stages of proposal development."
    ),
    expected_output=(
        "A clear, structured text summary detailing: "
        "1. Key functional requirements (what the system must do). "
        "2. Key non-functional requirements (how the system must perform, e.g., security, performance). "
        "3. A list of ambiguities or questions that need to be addressed for a complete proposal. "
        "4. A final concise summary of the overall project goals based on the requirements."
    ),
    agent=requirements_clarifier_agent
)

# Task 2: Draft Development Proposal
# Input: Output from clarify_requirements_task (implicitly passed by CrewAI as context).
# Output: Text for the Development Proposal section.
# Note: The placeholder `{clarified_requirements_summary}` is illustrative of how context might be named.
# CrewAI's context mechanism will make the output of `clarify_requirements_task` available.
# For robustness, ensure the task description explicitly refers to the expected input from the previous task.
draft_development_proposal_task = Task(
    description=(
        "Based on the 'Clarified Requirements Summary' (output of the previous task), "
        "draft a comprehensive Development Proposal section. "
        # "The clarified summary is: {clarify_requirements_task.output}. " # More explicit way if needed
        "Your draft should cover: "
        "1. Proposed Solution Overview: Briefly describe the envisioned software. "
        "2. Scope of Work: Itemize key features, modules, or functionalities to be developed. "
        "3. Suggested Timeline: Propose high-level phases or an overall estimated timeframe for development. "
        "4. Key Deliverables: List the tangible outcomes of the project (e.g., software modules, documentation)."
    ),
    expected_output=(
        "A well-structured text document for the Development Proposal section, including: "
        "1. A concise Proposed Solution Overview. "
        "2. A detailed list for Scope of Work. "
        "3. A clear Suggested Timeline. "
        "4. A list of Key Deliverables."
    ),
    agent=development_proposal_agent
    # Context: Output of `clarify_requirements_task`.
)

# Task 3: Draft Technical Proposal
# Input: Outputs from clarify_requirements_task and draft_development_proposal_task (implicitly passed).
# Output: Text for the Technical Proposal section.
# Similar to Task 2, placeholders like `{clarified_requirements_summary}` and `{development_proposal_draft}`
# illustrate expected context. CrewAI handles making prior task outputs available.
draft_technical_proposal_task = Task(
    description=(
        "Using the 'Clarified Requirements Summary' and the 'Development Proposal Draft' from previous tasks, "
        "draft a detailed Technical Proposal section. "
        # "Clarified Summary: {clarify_requirements_task.output}. "
        # "Development Draft: {draft_development_proposal_task.output}. "
        "Your draft should cover: "
        "1. System Architecture Overview: Describe the proposed architecture (e.g., microservices, monolithic, client-server). "
        "2. Recommended Technology Stack: Specify choices for frontend, backend, database(s), and any other critical technologies. Justify key choices briefly. "
        "3. Deployment Considerations: Outline the proposed deployment environment and strategy (e.g., cloud platform, CI/CD approach)."
    ),
    expected_output=(
        "A comprehensive text document for the Technical Proposal section, outlining: "
        "1. The System Architecture Overview with justifications. "
        "2. The Recommended Technology Stack with brief rationale for choices. "
        "3. Key Deployment Considerations."
    ),
    agent=technical_proposal_agent
    # Context: Outputs of `clarify_requirements_task`, `draft_development_proposal_task`.
)

# Task 4: Compile Final Proposal
# Input: Outputs from all preceding tasks (clarified requirements, dev proposal, tech proposal).
# Output: A single dictionary representing the complete, structured proposal.
# This task's description explicitly lists the expected inputs from previous tasks.
# CrewAI will populate these based on the outputs of the tasks specified in the crew's task list.
compile_final_proposal_task = Task(
    description=(
        "Compile all provided inputs into a final, professional software proposal document. "
        "The inputs are: "
        "1. Clarified Requirements Summary (from the 'Requirements Analysis Specialist')."
        "2. Development Proposal Draft (from the 'Software Development Strategist')."
        "3. Technical Proposal Draft (from the 'Solutions Architect')."
        "Ensure you use the exact outputs from these preceding tasks. For example, the development proposal draft is: {draft_development_proposal_task.output}."
        "Structure the final proposal according to the company's standard template (refer to `docs/proposal_template.md` for section headings and order). "
        "Write a compelling overall introduction for the proposal. "
        "Write a concise overall summary or conclusion. "
        "Ensure the language is professional, consistent, and the document is well-organized and free of jargon where possible. "
        "The final output should be a structured dictionary or JSON object representing the complete proposal."
    ),
    expected_output=(
        "A single, structured dictionary (Python dict) representing the complete software proposal. "
        "This dictionary should have top-level keys corresponding to the main sections of the `proposal_template.md` "
        "(e.g., 'introduction', 'developmentProposal', 'technicalProposal', 'overallProposalSummary'). "
        "The values should be the compiled text for these sections, with sub-sections also structured as nested dictionaries or lists where appropriate."
    ),
    agent=proposal_compilation_agent
)

# --- CREW DEFINITION AND EXECUTION FUNCTION ---

def run_crew(requirements_document_content: str) -> dict:
    """
    Initializes and runs the CrewAI proposal generation crew.

    This function sets up the proposal generation crew with predefined agents and tasks,
    kicks off the process with the provided requirements document content, and returns
    the structured proposal. It handles the sequential execution of tasks:
    clarifying requirements, drafting development and technical proposals, and
    compiling the final proposal.

    Args:
        requirements_document_content (str): The text content of the software
                                             requirements document.

    Returns:
        dict: A dictionary representing the structured software proposal if successful.
              The structure is expected to align with `docs/proposal_template.md`.
              Example successful structure:
              {
                  "fileName": "requirements.txt",
                  "fileContentPreview": "...",
                  "introduction": "...",
                  "developmentProposal": {
                      "proposedSolution": "...",
                      "scopeOfWork": ["..."],
                      "timeline": "...",
                      "deliverables": ["..."]
                  },
                  "technicalProposal": {
                      "systemArchitecture": "...",
                      "technologyStack": {"frontend": "...", "backend": "...", "database": "..."},
                      "deployment": "..."
                  },
                  "overallProposalSummary": {
                      "costEstimation": "...",
                      "nextSteps": "..."
                  }
              }
              Returns a dictionary with an 'error' key if any part of the process fails.
              Example error structure:
              {
                  "error": "Error message describing the issue.",
                  "details": "Optional traceback or further details."
                  "fileName": "requirements.txt" # (if available)
              }
    """
    # Define the crew with agents and tasks
    # The order of tasks in the list defines the execution sequence.
    # CrewAI handles passing context (outputs of previous tasks) to subsequent tasks
    # if the task descriptions are set up to expect them using placeholders like {task_output_variable_name}
    # or by explicitly setting the `context` parameter in the Task constructor if needed.
    # For our current setup, CrewAI's automatic context management based on task output
    # being available to subsequent tasks in the `tasks` list should work for simple string outputs.
    # The `compile_final_proposal_task` is designed to receive multiple inputs, which CrewAI should
    # make available in its context if previous tasks are in the same crew and run before it.
    
    proposal_crew = Crew(
        agents=[
            requirements_clarifier_agent,
            development_proposal_agent,
            technical_proposal_agent,
            proposal_compilation_agent
        ],
        tasks=[
            clarify_requirements_task,
            draft_development_proposal_task,
            draft_technical_proposal_task,
            compile_final_proposal_task
        ],
        process=Process.sequential, # Tasks will be executed one after another
        verbose=2 # Enables detailed logging of the crew's execution
        # memory=True # Can be enabled for more complex scenarios requiring long-term memory
    )

    # Prepare inputs for the kickoff.
    # The first task `clarify_requirements_task` expects `requirements_document_content`.
    inputs = {
        "requirements_document_content": requirements_document_content
    }

    # Kick off the crew's execution
    print("Kicking off the proposal generation crew...")
    try:
        # The result of the crew is the output of the last task in the sequence.
        # In our case, `compile_final_proposal_task` is expected to return a dictionary.
        result = proposal_crew.kickoff(inputs=inputs)
        
        if isinstance(result, dict):
            print("Crew execution completed successfully.")
            return result
        else:
            # If the final task's output isn't a dict (our expected format), wrap it or log an error.
            print(f"Crew execution finished, but the output was not a dictionary as expected. Output: {type(result)} - {result}")
            # Attempt to give some structure if it's text, or return an error.
            if isinstance(result, str):
                 return {
                    "error": "Crew finished, but final output was text, not structured proposal.",
                    "raw_output": result
                 }
            return {
                "error": "Crew execution finished, but the output format is unexpected.",
                "output_type": str(type(result))
            }

    except Exception as e:
        print(f"Error during crew execution: {e}")
        # Log the full traceback for debugging if possible/needed in a real environment
        import traceback
        traceback.print_exc()
        return {
            "error": f"An exception occurred during crew execution: {str(e)}",
            "details": traceback.format_exc()
        }

# Example usage (optional, for testing within this module)
if __name__ == '__main__':
    sample_requirements = """
    We need a web application for a library system.
    Users should be able to browse books, search for books by title or author, and reserve books.
    Librarians should be able to add new books, manage inventory, and track reservations.
    The system should be secure and handle multiple concurrent users.
    We would also like an admin panel for user management.
    """
    print(f"Running test with sample requirements:\n{sample_requirements}\n")
    # Make sure your .env file is set up with OPENAI_API_KEY and OPENAI_MODEL_NAME
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")
    else:
        proposal_result = run_crew(sample_requirements)
        print("\n--- Proposal Result ---")
        import json
        print(json.dumps(proposal_result, indent=2))
