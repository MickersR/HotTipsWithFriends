from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import Tip
from web_scraper import scrape_afl_fixtures, get_afl_fixtures_api, get_all_rounds_2024
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Cache for AFL fixtures to avoid excessive scraping
_afl_fixtures_cache = None
_cache_timestamp = None

def get_afl_fixtures(round_num=None):
    """Get AFL fixtures with caching"""
    global _afl_fixtures_cache, _cache_timestamp
    
    from datetime import datetime, timedelta
    
    # If requesting specific round, always fetch fresh
    if round_num:
        return get_afl_fixtures_api(2024, round_num)
    
    # Check if cache is valid (refresh every 12 hours)
    now = datetime.now()
    if _cache_timestamp and _afl_fixtures_cache:
        if now - _cache_timestamp < timedelta(hours=12):
            return _afl_fixtures_cache
    
    # Fetch fresh data from API
    logger.info("Fetching fresh AFL fixtures from API")
    fixtures = get_afl_fixtures_api()
    
    if fixtures:
        _afl_fixtures_cache = fixtures
        _cache_timestamp = now
        logger.info(f"Cached {len(fixtures)} AFL fixtures")
    
    return fixtures or []

@app.route('/')
def index():
    """Home page with navigation options"""
    return render_template('index.html')

@app.route('/submit-tips')
def submit_tips():
    """Display the tip submission form"""
    round_num = request.args.get('round', type=int)
    fixtures = get_afl_fixtures(round_num)
    rounds = get_all_rounds_2024()
    
    return render_template('submit_tips.html', 
                         fixtures=fixtures, 
                         rounds=rounds, 
                         selected_round=round_num)

@app.route('/view-tips')
def view_tips():
    """Display the tip viewing form"""
    return render_template('view_tips.html')

@app.route('/api/fixtures')
def get_fixtures():
    """API endpoint to get current AFL fixtures"""
    round_num = request.args.get('round', type=int)
    fixtures = get_afl_fixtures(round_num)
    return jsonify(fixtures)

@app.route('/api/rounds')
def get_rounds():
    """API endpoint to get all available rounds"""
    rounds = get_all_rounds_2024()
    return jsonify(rounds)

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
        
        # Get current timestamp
        current_time = datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Prepare tip data for encryption
        tip_data = {
            'user_name': user_name,
            'tips': tips,
            'margin': margin,
            'round': data.get('round', 'Current Round'),
            'created_at': timestamp
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
