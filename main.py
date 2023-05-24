from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from emailService import send_email

app = Flask(__name__)
CORS(app)

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()  # Get the JSON data from the request
    name = data.get('name')  # Access the 'name' field from the data
    email = data.get('email')  # Access the 'email' field from the data
    review = data.get('review')  # Access the 'review' field from the data

    # Perform any necessary operations with the data
    # ...

    # return 'Feedback submitted successfully!'
    send_email(email, name, review)

    # Perform any necessary processing or validation on the form data
    # ...
    
    # Return a response indicating successful submission
    response = {'message': 'Feedback submitted successfully'}
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=7000)

