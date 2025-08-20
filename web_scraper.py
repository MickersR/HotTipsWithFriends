import requests
import re
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

def get_afl_fixtures_api(year: int = 2024, round_num: Optional[int] = None) -> List[Dict]:
    """
    Get AFL fixtures from Squiggle API
    Returns a list of fixture dictionaries
    """
    try:
        # Build API URL
        api_url = f"https://api.squiggle.com.au/?q=games&year={year}"
        if round_num:
            api_url += f"&round={round_num}"
        
        logger.info(f"Fetching AFL fixtures from API: {api_url}")
        
        # Make API request with proper headers
        headers = {
            'User-Agent': 'AFL-Tipping-App/1.0 (Contact: admin@example.com)'
        }
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('games'):
            logger.warning("No games found in API response")
            return get_fallback_fixtures()
        
        # Convert API data to our format
        fixtures = []
        for game in data['games']:
            fixture = {
                'id': game.get('id', len(fixtures) + 1),
                'home_team': game.get('hteam', 'Unknown'),
                'away_team': game.get('ateam', 'Unknown'),
                'venue': game.get('venue', 'TBA'),
                'date': format_game_date(game.get('date')),
                'time': format_game_time(game.get('date')),
                'round': f"Round {game.get('round', 1)}"
            }
            fixtures.append(fixture)
        
        logger.info(f"Successfully fetched {len(fixtures)} AFL fixtures from API")
        return fixtures
        
    except requests.RequestException as e:
        logger.error(f"API request error: {str(e)}")
        return get_fallback_fixtures()
    except Exception as e:
        logger.error(f"Error fetching AFL fixtures from API: {str(e)}")
        return get_fallback_fixtures()

def get_all_rounds_2025() -> List[Dict]:
    """
    Get all rounds for 2024 AFL season (using 2024 data as 2025 isn't available yet)
    Returns a list of round dictionaries with round number and name
    """
    try:
        api_url = "https://api.squiggle.com.au/?q=games&year=2024"
        headers = {
            'User-Agent': 'AFL-Tipping-App/1.0 (Contact: admin@example.com)'
        }
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        rounds = set()
        
        for game in data.get('games', []):
            round_num = game.get('round')
            if round_num:
                rounds.add(round_num)
        
        # Convert to sorted list of dictionaries
        round_list = []
        for round_num in sorted(rounds):
            if round_num <= 23:  # Regular season
                round_list.append({
                    'number': round_num,
                    'name': f'Round {round_num}'
                })
            else:  # Finals
                finals_names = {
                    24: 'Elimination Finals',
                    25: 'Qualifying Finals', 
                    26: 'Semi Finals',
                    27: 'Preliminary Finals',
                    28: 'Grand Final'
                }
                round_list.append({
                    'number': round_num,
                    'name': finals_names.get(round_num, f'Finals Week {round_num - 23}')
                })
        
        logger.info(f"Found {len(round_list)} rounds for 2025 season")
        return round_list
        
    except Exception as e:
        logger.error(f"Error fetching rounds: {str(e)}")
        # Return basic round structure as fallback
        return [{'number': i, 'name': f'Round {i}'} for i in range(1, 24)]

def scrape_afl_fixtures() -> List[Dict]:
    """
    Legacy function name - now uses API instead of scraping
    """
    return get_afl_fixtures_api()

def format_game_date(date_str: Optional[str]) -> str:
    """Format game date from API to YYYY-MM-DD format"""
    if not date_str:
        return get_next_weekend_date()
    
    try:
        # Parse the date (API returns in YYYY-MM-DD HH:MM:SS format)
        date_part = date_str.split()[0] if ' ' in date_str else date_str
        # Validate and return if already in correct format
        datetime.strptime(date_part, '%Y-%m-%d')
        return date_part
    except (ValueError, IndexError):
        return get_next_weekend_date()

def format_game_time(date_str: Optional[str]) -> str:
    """Format game time from API to HH:MM format"""
    if not date_str:
        return '15:00'
    
    try:
        # Parse the time (API returns in YYYY-MM-DD HH:MM:SS format)
        if ' ' in date_str:
            time_part = date_str.split()[1]
            # Return just HH:MM
            return time_part[:5] if ':' in time_part else '15:00'
    except (ValueError, IndexError):
        pass
    
    return '15:00'



def get_next_weekend_date() -> str:
    """Get the next weekend date"""
    today = datetime.now()
    days_until_saturday = (5 - today.weekday()) % 7
    if days_until_saturday == 0:  # If today is Saturday
        days_until_saturday = 7
    next_saturday = today + timedelta(days=days_until_saturday)
    return next_saturday.strftime('%Y-%m-%d')

def get_fallback_fixtures() -> List[Dict]:
    """Return fallback fixture data when scraping fails"""
    logger.info("Using fallback AFL fixtures")
    
    # Get upcoming weekend dates
    base_date = datetime.now()
    days_until_saturday = (5 - base_date.weekday()) % 7
    if days_until_saturday == 0:
        days_until_saturday = 7
    
    saturday = base_date + timedelta(days=days_until_saturday)
    sunday = saturday + timedelta(days=1)
    
    return [
        {
            'id': 1,
            'home_team': 'Richmond',
            'away_team': 'Collingwood',
            'venue': 'MCG',
            'date': saturday.strftime('%Y-%m-%d'),
            'time': '19:50'
        },
        {
            'id': 2,
            'home_team': 'Adelaide',
            'away_team': 'Port Adelaide',
            'venue': 'Adelaide Oval',
            'date': saturday.strftime('%Y-%m-%d'),
            'time': '13:45'
        },
        {
            'id': 3,
            'home_team': 'Brisbane',
            'away_team': 'Gold Coast',
            'venue': 'Gabba',
            'date': saturday.strftime('%Y-%m-%d'),
            'time': '16:35'
        },
        {
            'id': 4,
            'home_team': 'Geelong',
            'away_team': 'Carlton',
            'venue': 'GMHBA Stadium',
            'date': saturday.strftime('%Y-%m-%d'),
            'time': '19:25'
        },
        {
            'id': 5,
            'home_team': 'Western Bulldogs',
            'away_team': 'Melbourne',
            'venue': 'Marvel Stadium',
            'date': sunday.strftime('%Y-%m-%d'),
            'time': '13:20'
        },
        {
            'id': 6,
            'home_team': 'Sydney',
            'away_team': 'GWS Giants',
            'venue': 'SCG',
            'date': sunday.strftime('%Y-%m-%d'),
            'time': '15:20'
        },
        {
            'id': 7,
            'home_team': 'West Coast',
            'away_team': 'Fremantle',
            'venue': 'Optus Stadium',
            'date': sunday.strftime('%Y-%m-%d'),
            'time': '18:10'
        },
        {
            'id': 8,
            'home_team': 'St Kilda',
            'away_team': 'Essendon',
            'venue': 'Marvel Stadium',
            'date': sunday.strftime('%Y-%m-%d'),
            'time': '20:10'
        }
    ]