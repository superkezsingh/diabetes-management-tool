import os
from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Route to serve the index.html page
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle the management plan request
@app.route("/get-management-plan", methods=["POST"])
def get_management_plan():
    data = request.json
    hba1c = data.get("hba1c")
    medications = data.get("medications")

    # Enhanced prompt for detailed, guideline-specific responses
    prompt = f"""
    You are a specialist diabetes nurse following the 'Algorithm for the Treatment of Type 2 Diabetes' as the only reference. 
    The patient's HbA1c level is {hba1c} mmol/mol, and their current medications are: {medications}.
    
    Based solely on this guideline, provide a comprehensive management plan with detailed, actionable steps. Include:

    1. **Medication Choice with Specific Dosages**: Recommend precise medications and starting dosages based on the patient's HbA1c level and BMI. 
       For example:
       - For HbA1c of 48 mmol/mol or above, consider starting Metformin as monotherapy, and provide the exact starting dosage and adjustment schedule.
       - For HbA1c thresholds of 53 mmol/mol or 58 mmol/mol, outline dual or triple therapy options with exact drug names and dosage guidance.
       - Detail when to escalate to injectable therapies if HbA1c remains above 58 mmol/mol after dual or triple therapy.
       
    2. **Lifestyle Recommendations**: Include recommended lifestyle changes, such as dietary advice, exercise, or weight management, to support glycemic control. Be specific about the type of exercise and dietary approach recommended in the guideline.

    3. **Monitoring and Follow-Up Instructions**: Specify follow-up intervals for HbA1c (e.g., 3-6 months) and additional monitoring requirements, such as blood glucose checks if a patient is started on a sulfonylurea with hypoglycemia risk.

    Only use the details from the guideline, and presume the user does not have access to the document.
    """

    try:
        # Use the ChatCompletion API with gpt-3.5-turbo for highly detailed responses
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a diabetes nurse assistant who strictly follows a detailed guideline-based approach."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.5
        )

        # Extract and return the response
        management_plan = response.choices[0].message['content'].strip()
        return jsonify({"management_plan": management_plan})
    except Exception as e:
        # Print the error to the console and send an error response
        print("Error with OpenAI API call:", e)
        return jsonify({"error": "There was an error processing your request."}), 500

if __name__ == "__main__":
    app.run(debug=True)
