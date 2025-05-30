import os
from flask import Flask, request, jsonify
# from backend.agent import generate_proposal # Old import
from backend.crew_ai_processor import run_crew

# Define the uploads directory path relative to this file.
# It navigates up one level from 'backend' (where app.py is) to the project root,
# then into the 'uploads' directory.
UPLOADS_DIR_PATH = os.path.join(os.path.dirname(__file__), '..', 'uploads')

# Initialize the Flask application.
app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Handles file uploads via POST request to /api/upload.
    Saves the uploaded file to the UPLOADS_DIR_PATH, then calls
    the generate_proposal function from agent.py to process the file
    and returns the generated proposal as JSON.
    """
    # Ensure the uploads directory exists; create it if it doesn't.
    # exist_ok=True means it won't raise an error if the directory already exists.
    os.makedirs(UPLOADS_DIR_PATH, exist_ok=True)

    # Check if the 'requirementsFile' part is in the request.
    # This is the name attribute of the file input in the HTML form.
    if 'requirementsFile' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400 # Bad Request
    
    file = request.files['requirementsFile']
    
    # Check if a file was actually selected by the user.
    # If the user does not select a file, the browser submits an
    # empty file part with an empty filename.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400 # Bad Request
    
    # If a file is present and has a filename.
    if file:
        filename = file.filename
        # Construct the full path to save the file.
        filepath = os.path.join(UPLOADS_DIR_PATH, filename)
        # Save the uploaded file to the specified path.
        file.save(filepath)

        # Read the content of the saved file
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                requirements_content = f.read()
        except Exception as e:
            # Handle file reading error
            return jsonify({"error": f"Failed to read uploaded file: {str(e)}"}), 500
        
        # Call the CrewAI processor function to generate the proposal based on the file content.
        # result = generate_proposal(filepath) # Old call
        result = run_crew(requirements_content)
        # Return the proposal data as a JSON response.
        return jsonify(result)

# Standard Python entry point.
if __name__ == '__main__':
    # Run the Flask development server.
    # debug=True enables auto-reloading on code changes and provides a debugger.
    # port=5000 specifies the port the server will listen on.
    app.run(debug=True, port=5000)
