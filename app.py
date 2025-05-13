from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Configuration: path to the master Excel file
HSN_MASTER_PATH = os.environ.get("HSN_MASTER_PATH", "HSN_Master_Data.xlsx")

# Load HSN master data once on startup
try:
    hsn_df = pd.read_excel(HSN_MASTER_PATH, dtype=str)
    hsn_df.columns = hsn_df.columns.str.strip().str.replace(" ", "")
except Exception as e:
    raise RuntimeError(f"Failed to load HSN master data: {e}")

# Create a lookup dictionary for fast validation
hsn_lookup = dict(zip(hsn_df["HSNCode"].str.strip(), hsn_df["Description"].str.strip()))

def validate_hsn_code(code: str) -> dict:
    """ Validate a single HSN code:
    - Format: numeric, length 2 to 8
    - Existence in master data
    Returns a dict with keys: code, valid, description (if valid), reason (if invalid)
    """
    code = code.strip()

    # Format validation
    if not code.isdigit():
        return {"code": code, "valid": False, "reason": "HSN code must be numeric"}
    if len(code) < 2 or len(code) > 8:
        return {"code": code, "valid": False, "reason": "HSN code length must be between 2 and 8 digits"}

    # Existence validation
    if code in hsn_lookup:
        return {"code": code, "valid": True, "description": hsn_lookup[code]}
    else:
        return {"code": code, "valid": False, "reason": "HSN code not found in master data"}

def terminal_interface():
    """Run this for terminal-based interaction"""
    print("\nHSN Code Validator (Type 'exit' to quit)")
    while True:
        code = input("\nEnter HSN Code: ").strip()
        if code.lower() in ('exit', 'quit'): break
        
        result = validate_hsn_code(code)
        if result['valid']:
            print(f"✅ Valid: {result['description']}")
        else:
            print(f"❌ Invalid: {result['reason']}")

@app.route('/')
def home():
    return """
    <h1>HSN Code Validation API</h1>
    <p>Endpoints:</p>
    <ul>
        <li>GET /validate/&lt;hsn_code&gt; - Validate single code</li>
        <li>POST /validate - Validate multiple codes (JSON payload)</li>
    </ul>
    """

@app.route('/validate/<hsn_code>', methods=['GET'])
def validate_single(hsn_code):
    """Endpoint for validating a single HSN code via URL"""
    result = validate_hsn_code(hsn_code)
    return jsonify(result)

@app.route('/validate', methods=['POST'])
def validate_multiple():
    """Endpoint for validating multiple HSN codes via JSON"""
    data = request.get_json()
    
    if not data or 'codes' not in data:
        return jsonify({"error": "Please provide 'codes' array in JSON payload"}), 400
    
    codes = data['codes']
    if isinstance(codes, str):
        codes = [codes]
    
    results = [validate_hsn_code(code) for code in codes]
    return jsonify({"results": results})

if __name__ == '__main__':
    # Start either web server or terminal interface
    if os.environ.get('TERMINAL_MODE'):
        terminal_interface()
    else:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)