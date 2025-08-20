from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import Tip
import json

# Mock AFL fixture data for current round
AFL_FIXTURES = [
    {
        'id': 1,
        'home_team': 'Richmond',
        'away_team': 'Collingwood',
        'venue': 'MCG',
        'date': '2025-08-23',
        'time': '19:50'
    },
    {
        'id': 2,
        'home_team': 'Adelaide',
        'away_team': 'Port Adelaide',
        'venue': 'Adelaide Oval',
        'date': '2025-08-24',
        'time': '13:45'
    },
    {
        'id': 3,
        'home_team': 'Brisbane',
        'away_team': 'Gold Coast',
        'venue': 'Gabba',
        'date': '2025-08-24',
        'time': '16:35'
    },
    {
        'id': 4,
        'home_team': 'Geelong',
        'away_team': 'Carlton',
        'venue': 'GMHBA Stadium',
        'date': '2025-08-24',
        'time': '19:25'
    },
    {
        'id': 5,
        'home_team': 'Western Bulldogs',
        'away_team': 'Melbourne',
        'venue': 'Marvel Stadium',
        'date': '2025-08-25',
        'time': '13:20'
    },
    {
        'id': 6,
        'home_team': 'Sydney',
        'away_team': 'GWS Giants',
        'venue': 'SCG',
        'date': '2025-08-25',
        'time': '15:20'
    },
    {
        'id': 7,
        'home_team': 'West Coast',
        'away_team': 'Fremantle',
        'venue': 'Optus Stadium',
        'date': '2025-08-25',
        'time': '18:10'
    },
    {
        'id': 8,
        'home_team': 'St Kilda',
        'away_team': 'Essendon',
        'venue': 'Marvel Stadium',
        'date': '2025-08-25',
        'time': '20:10'
    }
]

@app.route('/')
def index():
    """Home page with navigation options"""
    return render_template('index.html')

@app.route('/submit-tips')
def submit_tips():
    """Display the tip submission form"""
    return render_template('submit_tips.html', fixtures=AFL_FIXTURES)

@app.route('/view-tips')
def view_tips():
    """Display the tip viewing form"""
    return render_template('view_tips.html')

@app.route('/api/fixtures')
def get_fixtures():
    """API endpoint to get current AFL fixtures"""
    return jsonify(AFL_FIXTURES)

@app.route('/process-tips', methods=['POST'])
def process_tips():
    """Process submitted tips and return encrypted string"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        user_name = data.get('user_name', '').strip()
        password = data.get('password', '').strip()
        tips = data.get('tips', {})
        margin = data.get('margin', '')
        
        if not user_name or not password:
            return jsonify({'error': 'Name and password are required'}), 400
            
        if not tips:
            return jsonify({'error': 'At least one tip must be selected'}), 400
        
        # Prepare tip data for encryption
        tip_data = {
            'user_name': user_name,
            'tips': tips,
            'margin': margin,
            'round': 'Round 24',  # Current round
            'created_at': '2025-08-20'
        }
        
        return jsonify({
            'success': True,
            'tip_data': tip_data,
            'message': 'Tips processed successfully!'
        })
        
    except Exception as e:
        app.logger.error(f"Error processing tips: {str(e)}")
        return jsonify({'error': 'An error occurred processing your tips'}), 500

@app.route('/decrypt-tips', methods=['POST'])
def decrypt_tips():
    """Decrypt and return tip data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        encrypted_string = data.get('encrypted_string', '').strip()
        password = data.get('password', '').strip()
        
        if not encrypted_string or not password:
            return jsonify({'error': 'Both encrypted string and password are required'}), 400
        
        return jsonify({
            'success': True,
            'encrypted_string': encrypted_string,
            'password': password
        })
        
    except Exception as e:
        app.logger.error(f"Error decrypting tips: {str(e)}")
        return jsonify({'error': 'Failed to decrypt tips. Please check your password and encrypted string.'}), 500
