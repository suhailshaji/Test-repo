# AI Software Proposal Generator

This project is an AI-powered system designed to take software requirements as input and generate a detailed software proposal using a crew of specialized AI agents powered by CrewAI and OpenAI. The proposal includes development plans, technical specifications, and an overall summary.

## Project Structure

- `frontend/`: Contains the HTML, CSS, and JavaScript for the user interface.
- `backend/`: Contains the Python Flask server and the CrewAI agent processing logic.
    - `app.py`: The Flask web server.
    - `crew_ai_processor.py`: Defines and runs the CrewAI agents and tasks.
    - `agent_legacy.py`: The previous placeholder logic for proposal generation (now unused by default).
- `uploads/`: Directory where uploaded requirement files are temporarily stored (ensure this is in `.gitignore` if it contains sensitive test data, see `gitignore_instructions.txt`).
- `docs/`: Contains documentation, including:
    - `proposal_template.md`: The base template for the generated proposals.
    - `TESTING_AND_REFINEMENT_GUIDE.md`: Detailed guide for testing and improving AI outputs.
- `requirements.txt`: Python dependencies for the project.
- `.env.example`: Example file for environment variable configuration.
- `gitignore_instructions.txt`: Instructions for what to include in your `.gitignore` file.

## Setup

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Configure Environment Variables**

    This project uses OpenAI models via CrewAI. You need to configure your OpenAI API key.

    -   Copy the example environment file `.env.example` to a new file named `.env`:
        ```bash
        cp .env.example .env
        ```
    -   Edit the `.env` file and add your actual `OPENAI_API_KEY` and desired `OPENAI_MODEL_NAME`:
        ```env
        OPENAI_API_KEY="your_openai_api_key_here"
        OPENAI_MODEL_NAME="gpt-4-turbo" # Or your preferred model
        ```
    **Important:** The `.env` file contains sensitive keys and should NOT be committed to version control. Ensure `.env` is listed in your `.gitignore` file. (Instructions are in `gitignore_instructions.txt`).

4.  **Install Python dependencies:**
    All required Python packages, including Flask, CrewAI, CrewAI Tools, OpenAI, Python-Dotenv, and Langchain-OpenAI, are listed in `requirements.txt`. Install them using:
    ```bash
    pip install -r requirements.txt
    ```

## How it Works

The application uses a Flask backend to serve a simple frontend. When a user uploads a software requirements document:
1.  The file is saved to the `uploads/` directory.
2.  The content of the file is passed to the CrewAI processing system (`backend/crew_ai_processor.py`).
3.  A "crew" of specialized AI agents is assembled:
    *   **Requirements Clarifier Agent:** Analyzes the input document for clarity, key functionalities, and ambiguities.
    *   **Development Proposal Agent:** Drafts the development plan, scope, timeline, and deliverables based on the clarified requirements.
    *   **Technical Proposal Agent:** Creates the technical specifications, including system architecture and technology stack.
    *   **Proposal Compilation Agent:** Synthesizes all inputs into a final, structured proposal document.
4.  These agents work sequentially, each performing its task and passing its output to the next, to generate a comprehensive software proposal.
5.  The final proposal (a structured JSON object) is sent back to the frontend and displayed to the user.

## Running the Application

1.  **Start the Flask backend server:**
    Ensure your environment variables are set up (see Step 3 in Setup). Navigate to the `backend` directory and run the Flask application:
    ```bash
    cd backend
    python app.py
    ```
    The server will typically start on `http://127.0.0.1:5000`. You will see logs from Flask and CrewAI in the terminal.

2.  **Open the frontend:**
    Open the `frontend/index.html` file in your web browser.

3.  **Usage:**
    - Click "Choose File" to select your requirements document (e.g., a .txt or .md file).
    - Click "Generate Proposal".
    - The AI-generated proposal will appear below the form. This may take some time depending on the complexity of the requirements and the LLM's response speed.

## Testing and Refinement

The quality of the AI-generated proposals can be significantly improved through iterative testing and refinement of the agent prompts and task definitions.

For detailed instructions on how to test the AI proposal generation and refine its performance, please see the [Testing and Refinement Guide](docs/TESTING_AND_REFINEMENT_GUIDE.md).

## Future Development Ideas

- **Enhanced AI Capabilities:**
    - Integrate more sophisticated tools for agents (e.g., web search for current technology trends, code execution for validating snippets).
    - Allow for more complex requirement document formats (PDF, DOCX) by adding pre-processing tools.
    - Experiment with different LLMs or fine-tuning models for specific proposal sections.
- **Application Features:**
    - Add user authentication and project management features to save and manage proposals.
    - Implement a more interactive frontend (e.g., allowing users to edit sections of the AI-generated proposal).
    - Provide options to customize the proposal template through the UI.
- **UI/UX:**
    - Improve the visual design and user experience of the frontend.
    - Add progress indicators for the AI generation process.
