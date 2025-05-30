# Testing and Refinement Guide for AI Proposal Generator

This guide outlines the steps to test the CrewAI-powered proposal generator and suggestions for refining its output. The quality of the generated proposals heavily depends on the LLM used, the clarity of requirements, and the prompts given to the AI agents. Expect to iterate on the agent/task definitions for optimal results.

## 1. Prerequisites

*   **Environment Variables:** Ensure you have a `.env` file in the root directory (you can copy `.env.example` to `.env`). This file *must* contain:
    *   `OPENAI_API_KEY`: Your valid OpenAI API key.
    *   `OPENAI_MODEL_NAME`: The OpenAI model you wish to use (e.g., `gpt-4-turbo`, `gpt-3.5-turbo`). Using a more capable model like GPT-4 series is highly recommended for better results.
*   **Dependencies:** All Python dependencies from `requirements.txt` must be installed in your environment (`pip install -r requirements.txt`).

## 2. Running the Application

1.  **Start the Flask Backend Server:**
    Open your terminal, navigate to the `backend` directory, and run:
    ```bash
    python app.py
    ```
    The server should start on `http://127.0.0.1:5000`. You will see output from Flask and potentially CrewAI in this terminal.

2.  **Open the Frontend:**
    Open the `frontend/index.html` file in your web browser.

## 3. Performing Tests

1.  **Prepare Test Requirement Documents:**
    Create a few sample requirement documents as plain text files (`.txt`). Consider:
    *   **Simple Case:** A straightforward project with 2-3 clear features (e.g., the library system example).
        ```txt
        Project: Simple Library Management System

        Core Requirements:
        - Users should be able to browse available books.
        - Users should be able to search for books by title or author.
        - Users should be able to reserve a book if it's available.
        - Librarians should be able to add new books to the system.
        - Librarians should be able to manage book inventory (update details, mark as unavailable).
        - Librarians should be able to view and manage reservations.
        - The system must be accessible via a web browser.
        - Basic security measures to protect user data are required.
        ```
    *   **More Complex Case:** A project with more features, interdependencies, or specific non-functional requirements.
    *   **Ambiguous Case (Optional):** A document with vague or conflicting requirements to test the `RequirementsClarifierAgent`.

2.  **Upload and Generate:**
    *   Use the "Choose File" button on the webpage to select one of your test requirement documents.
    *   Click "Generate Proposal."
    *   Observe the backend terminal for `verbose` output from CrewAI. This will show which agent is running and what task it's performing. This is very useful for debugging.
    *   Examine the proposal displayed on the webpage.

## 4. Analyzing the Output

For each generated proposal, consider the following:

*   **Overall Structure:** Does the output match the structure defined in `docs/proposal_template.md`? Are all sections present?
*   **Clarity of Requirements (Output from `RequirementsClarifierAgent`):**
    *   Did the agent correctly identify functional and non-functional requirements?
    *   Were ambiguities (if any) flagged?
    *   Is the summary clear and actionable?
*   **Development Proposal (Output from `DevelopmentProposalAgent`):**
    *   Is the proposed solution overview reasonable?
    *   Is the scope of work well-defined and based on the requirements?
    *   Is the timeline suggestion (even if high-level) logical?
    *   Are deliverables appropriate?
*   **Technical Proposal (Output from `TechnicalProposalAgent`):**
    *   Is the system architecture suggestion suitable?
    *   Is the technology stack appropriate for the project type?
    *   Are deployment considerations sensible?
*   **Final Compiled Proposal (Output from `ProposalCompilationAgent`):**
    *   Is the introduction engaging?
    *   Is the overall summary accurate?
    *   Is the language professional and consistent?
    *   Is the content well-organized and easy to read?
*   **Error Handling:** If you provide malformed input or if an API error occurs (e.g., invalid API key), does the system handle it gracefully and show an error message on the frontend?

## 5. Refining the Crew (Iterative Process)

If the results are not satisfactory, you'll need to refine the CrewAI setup. This typically involves editing `backend/crew_ai_processor.py`:

*   **Agent Prompts (Role, Goal, Backstory):**
    *   These are critical. Make them more specific or add more context if an agent is not performing as expected. For example, if the `TechnicalProposalAgent` suggests an outdated technology, you might add to its backstory or goal that it should "focus on modern, scalable, and cost-effective cloud-native solutions."
*   **Task Descriptions & Expected Outputs:**
    *   These are the instructions for the LLM. Ensure they are very clear, unambiguous, and detailed about what you expect.
    *   If a task's output is consistently missing something, add it explicitly to its `expected_output` description.
    *   You can guide the format more strictly within the `expected_output` (e.g., "Provide the scope of work as a bulleted list.").
*   **LLM Choice:**
    *   The `OPENAI_MODEL_NAME` in your `.env` file matters a lot. `gpt-3.5-turbo` is faster and cheaper but less capable than `gpt-4-turbo` or newer GPT-4 models. For high-quality, nuanced proposal generation, a GPT-4 class model is highly recommended.
*   **Tools (Advanced):**
    *   If agents need to perform actions beyond text processing (e.g., read specific file types they don't natively handle, search the web for current information, perform calculations), you might need to add custom CrewAI tools. Refer to the CrewAI documentation for creating and assigning tools.
*   **Sequential vs. Hierarchical Process:**
    *   Our current setup uses a `Process.sequential`. For very complex proposals, you might explore hierarchical processes where a manager agent delegates to sub-crews.
*   **Memory:**
    *   For longer conversations or more context retention between tasks than what's automatically passed, you might enable memory for the crew: `memory=True` in the `Crew` definition.

**Debugging Tips:**

*   **Verbose Output:** The `verbose=2` setting in the `Crew` definition is your best friend. Examine the detailed logs in the backend terminal to understand what each agent is doing, what prompts are being sent to the LLM, and what raw outputs are being received.
*   **Test Agents/Tasks Individually:** You can temporarily modify `crew_ai_processor.py` to run only a specific agent or task to isolate issues.
*   **LangSmith (Optional):** If you set up LangSmith (as per `.env.example`), it provides excellent tracing and debugging capabilities for LangChain/CrewAI applications.

By iteratively testing and refining, you can significantly improve the quality of the AI-generated software proposals.
