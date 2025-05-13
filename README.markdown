# HSN Code Validation API

## Overview
This is a Flask-based application for validating Harmonized System Nomenclature (HSN) codes against a master dataset stored in an Excel file (`HSN_Master_Data.xlsx`). The application provides both a RESTful API and a terminal-based interface for validating HSN codes. It checks for:
- Numeric format (2 to 8 digits)
- Existence in the master dataset
- Returns associated descriptions for valid codes

## Features
- **Single HSN Code Validation**: Validate one code via a GET request.
- **Bulk HSN Code Validation**: Validate multiple codes via a POST request.
- **Terminal Interface**: Interactive CLI for manual validation.
- **Fast Lookup**: Uses a dictionary for efficient validation.
- **Environment Configuration**: Supports environment variables for flexibility.

## Prerequisites
- Python 3.8+
- Required Python packages:
  - `flask`
  - `pandas`
  - `openpyxl` (for Excel file handling)
- An Excel file (`HSN_Master_Data.xlsx`) with columns `HSNCode` and `Description`.

## Installation
1. **Clone the Repository** (or download the source code):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install flask pandas openpyxl
   ```

4. **Prepare the Master Data**:
   - Place the `HSN_Master_Data.xlsx` file in the project root directory or specify its path via the `HSN_MASTER_PATH` environment variable.
   - Ensure the Excel file has at least two columns: `HSNCode` and `Description`.

5. **Set Environment Variables** (optional):
   - `HSN_MASTER_PATH`: Path to the Excel file (default: `HSN_Master_Data.xlsx`).
   - `PORT`: Port for the Flask server (default: `5000`).
   - `TERMINAL_MODE`: Set to any value to run in terminal mode instead of the web server.

   Example (Linux/Mac):
   ```bash
   export HSN_MASTER_PATH="/path/to/HSN_Master_Data.xlsx"
   export PORT=8080
   ```

   Example (Windows):
   ```cmd
   set HSN_MASTER_PATH=C:\path\to\HSN_Master_Data.xlsx
   set PORT=8080
   ```

## Running the Application
### Web Server Mode
Run the Flask application to start the API server:
```bash
python app.py
```
The server will be available at `http://localhost:5000` (or the specified `PORT`).

### Terminal Mode
Run the terminal interface for interactive validation:
```bash
export TERMINAL_MODE=1  # On Windows: set TERMINAL_MODE=1
python app.py
```
Follow the prompts to enter HSN codes and view validation results.

## API Endpoints
### 1. Validate Single HSN Code
- **Endpoint**: `GET /validate/<hsn_code>`
- **Description**: Validates a single HSN code.
- **Response**:
  - `code`: The input HSN code.
  - `valid`: Boolean indicating if the code is valid.
  - `description`: Description from master data (if valid).
  - `reason`: Reason for failure (if invalid).

- **Example**:
  ```bash
  curl http://localhost:5000/validate/123456
  ```
  **Sample Response** (valid):
  ```json
  {
    "code": "123456",
    "valid": true,
    "description": "Some product description"
  }
  ```
  **Sample Response** (invalid):
  ```json
  {
    "code": "123",
    "valid": false,
    "reason": "HSN code not found in master data"
  }
  ```

### 2. Validate Multiple HSN Codes
- **Endpoint**: `POST /validate`
- **Description**: Validates a list of HSN codes provided in a JSON payload.
- **Request Body**:
  ```json
  {
    "codes": ["123456", "789012", "invalid"]
  }
  ```
- **Response**:
  - `results`: Array of validation results (same structure as single validation).

- **Example**:
  ```bash
  curl -X POST http://localhost:5000/validate -H "Content-Type: application/json" -d '{"codes": ["123456", "789012"]}'
  ```
  **Sample Response**:
  ```json
  {
    "results": [
      {
        "code": "123456",
        "valid": true,
        "description": "Some product description"
      },
      {
        "code": "789012",
        "valid": false,
        "reason": "HSN code not found in master data"
      }
    ]
  }
  ```

## Terminal Interface Usage
1. Start the terminal mode (see "Running the Application").
2. Enter an HSN code when prompted.
3. View the result (valid with description or invalid with reason).
4. Type `exit` or `quit` to stop.

**Example**:
```
HSN Code Validator (Type 'exit' to quit)

Enter HSN Code: 123456
✅ Valid: Some product description

Enter HSN Code: abc
❌ Invalid: HSN code must be numeric

Enter HSN Code: exit
```

## Error Handling
- **Excel File Errors**: If the `HSN_Master_Data.xlsx` file is missing or malformed, the application will raise a `RuntimeError` on startup.
- **Invalid JSON Payload**: The `/validate` POST endpoint returns a `400` status code with an error message if the payload is missing or lacks the `codes` key.
- **Invalid HSN Codes**: Validation errors are returned with descriptive reasons (e.g., non-numeric, wrong length, not in master data).

## Notes
- The application assumes the Excel file has clean data (no extra spaces in `HSNCode` or `Description` columns). The code strips spaces during loading and validation.
- The lookup dictionary (`hsn_lookup`) is created on startup for performance, so ensure the Excel file is not excessively large to avoid memory issues.
- Debug mode is enabled by default (`debug=True`) for development. Disable it in production for security.

## Contributing
Feel free to submit issues or pull requests for bug fixes, performance improvements, or new features. Ensure any changes are tested and maintain compatibility with the existing functionality.

## License
This project is licensed under the MIT License.