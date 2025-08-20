from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import Tip
from web_scraper import scrape_afl_fixtures
import json
import logging

logger = logging.getLogger(__name__)

# Cache for AFL fixtures to avoid excessive scraping
_afl_fixtures_cache = None
_cache_timestamp = None

def get_afl_fixtures():
    """Get AFL fixtures with caching"""
    global _afl_fixtures_cache, _cache_timestamp
    
    from datetime import datetime, timedelta
    
    # Check if cache is valid (refresh daily)
    now = datetime.now()
    if _cache_timestamp and _afl_fixtures_cache:
        if now - _cache_timestamp < timedelta(hours=12):  # Cache for 12 hours
            return _afl_fixtures_cache
    
    # Scrape fresh data
    logger.info("Fetching fresh AFL fixtures from austadiums.com")
    fixtures = scrape_afl_fixtures()
    
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
    fixtures = get_afl_fixtures()
    return render_template('submit_tips.html', fixtures=fixtures)

@app.route('/view-tips')
def view_tips():
    """Display the tip viewing form"""
    return render_template('view_tips.html')

@app.route('/api/fixtures')
def get_fixtures():
    """API endpoint to get current AFL fixtures"""
    fixtures = get_afl_fixtures()
    return jsonify(fixtures)

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
