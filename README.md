# AI Software Proposal Generator

This project is an AI-powered agent designed to take software requirements as input and generate a detailed software proposal. The proposal includes development plans, technical specifications, and an overall summary.

## Project Structure

- `frontend/`: Contains the HTML, CSS, and JavaScript for the user interface.
- `backend/`: Contains the Python Flask server and AI agent logic.
- `uploads/`: Directory where uploaded requirement files are temporarily stored.
- `docs/`: Contains documentation, including the proposal template.
- `requirements.txt`: Python dependencies.

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

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Start the Flask backend server:**
    Navigate to the `backend` directory and run the Flask application:
    ```bash
    cd backend
    python app.py
    ```
    The server will typically start on `http://127.0.0.1:5000`.

2.  **Open the frontend:**
    Open the `frontend/index.html` file in your web browser.

3.  **Usage:**
    - Click "Choose File" to select your requirements document (e.g., a .txt or .md file).
    - Click "Generate Proposal".
    - The generated proposal (currently a placeholder) will appear below the form.

## Future Development

- Integrate a sophisticated AI/LLM to parse requirements and generate meaningful proposal content.
- Allow various input formats (e.g., PDF, DOCX).
- Add user authentication and project management features.
- Enhance the UI/UX.
