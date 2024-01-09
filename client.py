"""This module contains functions for email and domain verification."""
from typing import Dict, Any

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

API_KEY: str = 'your API key here'
BASE_URL: str = 'https://api.hunter.io/v2/'

# local var for results
email_results: Dict[str, Dict[str, Any]] = {}
domain_results: Dict[str, Dict[str, Any]] = {}


# Hunter.io request funcs
def verify_email(email: str) -> Dict[str, Any]:
    """Verify the provided email address."""
    url = f'{BASE_URL}email-verifier?email={email}&api_key={API_KEY}'
    try:
        return requests.get(url, timeout=3).json()
    except requests.RequestException as error_msg:
        return {'error': f'Request failed: {str(error_msg)}'}


def domain_count(domain: str) -> Dict[str, Any]:
    """Count domain instances."""
    url = f'{BASE_URL}email-count?domain={domain}'
    try:
        return requests.get(url, timeout=3).json()
    except requests.RequestException as error_msg:
        return {'error': f'Request failed: {str(error_msg)}'}


# CRUD
@app.route('/verify-email', methods=['POST'])
def check_email() -> str:
    """Verify the provided email address."""
    email: str = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    verification_result: Dict[str, Any] = verify_email(email)
    email_results[email] = verification_result

    return jsonify(verification_result)


@app.route('/email-results', methods=['GET'])
def get_email_results() -> str:
    """Get Email results ALL."""
    return jsonify(email_results)


@app.route('/email-results/<string:email>', methods=['GET'])
def get_email_result(email) -> str:
    """Get one Email results."""
    if email in email_results:
        return jsonify({email: email_results.get(email)})
    return jsonify({'error': 'Email not found'}), 404


@app.route('/email-results/<string:email>', methods=['PUT'])
def update_email_result(email) -> str:
    """Update one Email results."""
    if email in email_results:
        email_results[email] = request.json
        return jsonify({'message': f'Email {email} result updated successfully'})

    return jsonify({'error': 'Email not found'}), 404


@app.route('/email-results/<string:email>', methods=['DELETE'])
def delete_email_result(email) -> str:
    """Remove  Email results."""
    if email in email_results:
        email_results.pop(email)
        return jsonify({'message': f'Email {email} result deleted successfully'})
    return jsonify({'error': 'Email not found'}), 404


@app.route('/domain-results', methods=['GET'])
def get_domain_results() -> str:
    """Domain results ALL."""
    return jsonify(domain_results)


@app.route('/domain-count-result', methods=['GET'])
def count_results() -> str:
    """Count domain instances."""
    domain: str = request.json.get('domain')

    if not domain:
        return jsonify({'error': 'Domain is required'}), 400

    verification_result: Dict[str, Any] = domain_count(domain)
    domain_results[domain] = verification_result['data']['total']

    return jsonify(verification_result)


if __name__ == '__main__':
    app.run(debug=False)
