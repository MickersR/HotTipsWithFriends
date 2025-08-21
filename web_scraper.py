import requests
import re
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional
import trafilatura

logger = logging.getLogger(__name__)

def scrape_afl_2025_fixtures() -> List[Dict]:
    """
    Scrape AFL 2025 fixtures from AFL.com.au using trafilatura
    """
    try:
        url = "https://www.afl.com.au/fixture?Competition=1&Season=73&Round=1170"
        logger.info(f"Scraping 2025 AFL fixtures from: {url}")
        
        # Download the page content
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            logger.error("Failed to download AFL fixture page")
            return get_fallback_2025_fixtures()
        
        # Extract text content
        text_content = trafilatura.extract(downloaded)
        if not text_content:
            logger.error("Failed to extract content from AFL fixture page")
            return get_fallback_2025_fixtures()
        
        logger.info("Successfully scraped AFL fixture page content")
        
        # Parse the content to extract fixture information
        fixtures = parse_afl_fixture_text(text_content)
        
        if fixtures:
            logger.info(f"Successfully parsed {len(fixtures)} fixtures from 2025 AFL data")
            return fixtures
        else:
            logger.warning("No fixtures found in scraped content, using fallback")
            return get_fallback_2025_fixtures()
            
    except Exception as e:
        logger.error(f"Error scraping 2025 AFL fixtures: {str(e)}")
        return get_fallback_2025_fixtures()

def parse_afl_fixture_text(content: str) -> List[Dict]:
    """
    Parse AFL fixture information from scraped text content
    """
    fixtures = []
    
    # Common AFL team names and their variations
    team_patterns = {
        'Adelaide': ['Adelaide', 'Crows', 'Adelaide Crows'],
        'Brisbane': ['Brisbane', 'Lions', 'Brisbane Lions'],
        'Carlton': ['Carlton', 'Blues'],
        'Collingwood': ['Collingwood', 'Magpies', 'Pies'],
        'Essendon': ['Essendon', 'Bombers'],
        'Fremantle': ['Fremantle', 'Dockers', 'Freo'],
        'Geelong': ['Geelong', 'Cats'],
        'Gold Coast': ['Gold Coast', 'Suns', 'Gold Coast Suns'],
        'GWS Giants': ['GWS', 'Giants', 'GWS Giants'],
        'Hawthorn': ['Hawthorn', 'Hawks'],
        'Melbourne': ['Melbourne', 'Demons'],
        'North Melbourne': ['North Melbourne', 'Kangaroos', 'North'],
        'Port Adelaide': ['Port Adelaide', 'Power', 'Port'],
        'Richmond': ['Richmond', 'Tigers'],
        'St Kilda': ['St Kilda', 'Saints'],
        'Sydney': ['Sydney', 'Swans', 'Sydney Swans'],
        'West Coast': ['West Coast', 'Eagles', 'West Coast Eagles'],
        'Western Bulldogs': ['Western Bulldogs', 'Bulldogs', 'Dogs']
    }
    
    # Try to extract team matchups from the content
    lines = content.split('\n')
    
    fixture_id = 1
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Look for patterns that might indicate a match
        # Example patterns: "Team1 v Team2", "Team1 vs Team2"
        vs_match = re.search(r'([A-Za-z\s]+?)\s+(?:v|vs|V|VS)\s+([A-Za-z\s]+)', line)
        
        if vs_match:
            team1 = vs_match.group(1).strip()
            team2 = vs_match.group(2).strip()
            
            # Validate that these look like AFL team names
            if is_valid_team_name(team1, team_patterns) and is_valid_team_name(team2, team_patterns):
                # Normalize team names
                home_team = normalize_team_name(team1, team_patterns)
                away_team = normalize_team_name(team2, team_patterns)
                
                if home_team and away_team and home_team != away_team:
                    fixture = {
                        'id': fixture_id,
                        'home_team': home_team,
                        'away_team': away_team,
                        'venue': extract_venue_from_context(lines, i),
                        'date': get_next_weekend_date(),  # Default to next weekend
                        'time': '15:00',  # Default time
                        'round': 'Round 1'  # Default round
                    }
                    fixtures.append(fixture)
                    fixture_id += 1
    
    return fixtures

def is_valid_team_name(name: str, team_patterns: Dict) -> bool:
    """Check if a name looks like an AFL team name"""
    name = name.strip()
    if len(name) < 3 or len(name) > 20:
        return False
    
    # Check against known team patterns
    for team, variations in team_patterns.items():
        for variation in variations:
            if variation.lower() in name.lower():
                return True
    return False

def normalize_team_name(name: str, team_patterns: Dict) -> Optional[str]:
    """Normalize team name to standard format"""
    name = name.strip()
    
    for team, variations in team_patterns.items():
        for variation in variations:
            if variation.lower() in name.lower():
                return team
    return None

def extract_venue_from_context(lines: List[str], current_index: int) -> str:
    """Try to extract venue information from surrounding lines"""
    venues = [
        'MCG', 'Marvel Stadium', 'Adelaide Oval', 'Gabba', 'SCG', 
        'Optus Stadium', 'GMHBA Stadium', 'TIO Stadium', 'Blundstone Arena',
        'Manuka Oval', 'Stadium Australia', 'People First Stadium',
        'Heritage Bank Stadium', 'GIANTS Stadium'
    ]
    
    # Check a few lines around the current match
    for i in range(max(0, current_index - 2), min(len(lines), current_index + 3)):
        line = lines[i].strip()
        for venue in venues:
            if venue.lower() in line.lower():
                return venue
    
    return 'TBA'

def get_fallback_2025_fixtures() -> List[Dict]:
    """Return fallback fixture data for 2025 when scraping fails"""
    logger.info("Using fallback 2025 AFL fixtures")
    
    # Get upcoming weekend dates for 2025
    base_date = datetime(2025, 3, 15)  # Approximate AFL season start
    saturday = base_date
    sunday = base_date + timedelta(days=1)
    
    return [
        {
            'id': 1,
            'home_team': 'Richmond',
            'away_team': 'Carlton',
            'venue': 'MCG',
            'date': saturday.strftime('%Y-%m-%d'),
            'time': '19:50',
            'round': 'Round 1'
        },
        {
            'id': 2,
            'home_team': 'Adelaide',
            'away_team': 'Port Adelaide',
            'venue': 'Adelaide Oval',
            'date': saturday.strftime('%Y-%m-%d'),
            'time': '16:40',
            'round': 'Round 1'
        },
        {
            'id': 3,
            'home_team': 'Brisbane',
            'away_team': 'Sydney',
            'venue': 'Gabba',
            'date': saturday.strftime('%Y-%m-%d'),
            'time': '14:20',
            'round': 'Round 1'
        },
        {
            'id': 4,
            'home_team': 'Collingwood',
            'away_team': 'Melbourne',
            'venue': 'MCG',
            'date': sunday.strftime('%Y-%m-%d'),
            'time': '13:20',
            'round': 'Round 1'
        },
        {
            'id': 5,
            'home_team': 'Geelong',
            'away_team': 'St Kilda',
            'venue': 'GMHBA Stadium',
            'date': sunday.strftime('%Y-%m-%d'),
            'time': '15:40',
            'round': 'Round 1'
        },
        {
            'id': 6,
            'home_team': 'Western Bulldogs',
            'away_team': 'Hawthorn',
            'venue': 'Marvel Stadium',
            'date': sunday.strftime('%Y-%m-%d'),
            'time': '18:10',
            'round': 'Round 1'
        },
        {
            'id': 7,
            'home_team': 'West Coast',
            'away_team': 'Fremantle',
            'venue': 'Optus Stadium',
            'date': sunday.strftime('%Y-%m-%d'),
            'time': '20:40',
            'round': 'Round 1'
        },
        {
            'id': 8,
            'home_team': 'GWS Giants',
            'away_team': 'Essendon',
            'venue': 'GIANTS Stadium',
            'date': base_date.strftime('%Y-%m-%d'),
            'time': '17:20',
            'round': 'Round 1'
        }
    ]

def get_all_rounds_2025() -> List[Dict]:
    """
    Get all rounds for 2025 AFL season
    Returns a list of round dictionaries with round number and name
    """
    try:
        api_url = "https://api.squiggle.com.au/?q=games&year=2025"
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
        logger.error(f"Error fetching 2025 rounds: {str(e)}")
        # Return basic round structure as fallback
        return [{'number': i, 'name': f'Round {i}'} for i in range(1, 24)]

def load_manual_fixtures() -> List[Dict]:
    """
    Load AFL fixtures from manual JSON file
    """
    try:
        import json
        import os
        
        json_file = 'manual_fixtures_2025.json'
        
        if not os.path.exists(json_file):
            logger.warning("Manual fixtures file not found, using API fallback")
            return []
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        fixtures = []
        fixture_id = 1
        
        for round_data in data.get('rounds', []):
            round_number = round_data.get('number', 1)
            round_name = round_data.get('name', f'Round {round_number}')
            
            for fixture in round_data.get('fixtures', []):
                fixture_data = {
                    'id': fixture.get('id', fixture_id),
                    'home_team': fixture.get('home_team', 'TBA'),
                    'away_team': fixture.get('away_team', 'TBA'),
                    'venue': fixture.get('venue', 'TBA'),
                    'date': fixture.get('date', '2025-03-15'),
                    'time': fixture.get('time', '15:00'),
                    'round': round_name
                }
                fixtures.append(fixture_data)
                fixture_id += 1
        
        logger.info(f"Loaded {len(fixtures)} fixtures from manual file")
        return fixtures
        
    except Exception as e:
        logger.error(f"Error loading manual fixtures: {str(e)}")
        return []

def get_manual_rounds() -> List[Dict]:
    """
    Get rounds from manual JSON file
    """
    try:
        import json
        import os
        
        json_file = 'manual_fixtures_2025.json'
        
        if not os.path.exists(json_file):
            return []
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        rounds = []
        for round_data in data.get('rounds', []):
            rounds.append({
                'number': round_data.get('number', 1),
                'name': round_data.get('name', f'Round {round_data.get("number", 1)}')
            })
        
        logger.info(f"Loaded {len(rounds)} rounds from manual file")
        return rounds
        
    except Exception as e:
        logger.error(f"Error loading manual rounds: {str(e)}")
        return []

def get_afl_fixtures_api(year: int = 2025, round_num: Optional[int] = None) -> List[Dict]:
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

def get_all_rounds_2024() -> List[Dict]:
    """
    Get all rounds for 2024 AFL season
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
        
        logger.info(f"Found {len(round_list)} rounds for 2024 season")
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