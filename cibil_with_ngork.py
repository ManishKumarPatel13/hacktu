# 2sbhncQR7LWduaezXUgkQWUB9Kl_5P1XJFLJGinFKRsfaJefW
from flask import Flask, request, jsonify
import numpy as np
from pyngrok import ngrok
import os

app = Flask(__name__)

@app.route('/calculate_cibil', methods=['POST'])
def calculate_cibil():
    try:
        data = request.json
        
        # Convert inputs to numpy arrays
        payment_history = np.array(data['payment_history'], dtype=int)
        credit_utilization = np.array(data['credit_utilization'], dtype=float)
        credit_age = np.array(data['credit_age'], dtype=int)
        credit_mix = np.array(data['credit_mix'], dtype=str)
        new_inquiries = np.array(data['new_inquiries'], dtype=int)

        # Calculate scores
        scores = calculate_cibil_score_vectorized(
            payment_history,
            credit_utilization,
            credit_age,
            credit_mix,
            new_inquiries
        )

        return jsonify({
            'cibil_scores': scores.tolist(),
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

if __name__ == '__main__':
    # Set up ngrok
    ngrok.set_auth_token(os.getenv('cr_2sbgjeZkqt4CpgfjSI5ntDnIlBV'))
    public_url = ngrok.connect(5000, bind_tls=True).public_url
    print(f'API Endpoint: {public_url}/calculate_cibil')
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000)

