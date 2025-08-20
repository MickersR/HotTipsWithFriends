import trafilatura
import re
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            logger.error(f"Failed to download content from {url}")
            return ""
        
        text = trafilatura.extract(downloaded)
        return text or ""
    except Exception as e:
        logger.error(f"Error extracting content from {url}: {str(e)}")
        return ""

def scrape_afl_fixtures() -> List[Dict]:
    """
    Scrape AFL fixtures from austadiums.com
    Returns a list of fixture dictionaries
    """
    url = "https://www.austadiums.com/sport/comp/afl/fixture"
    
    try:
        # Get the webpage content
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            logger.error("Failed to download AFL fixtures page")
            return get_fallback_fixtures()
        
        # Extract text content
        text_content = trafilatura.extract(downloaded)
        if not text_content:
            logger.error("Failed to extract text from AFL fixtures page")
            return get_fallback_fixtures()
        
        # Parse fixtures from the text content
        fixtures = parse_fixtures_from_text(text_content)
        
        if not fixtures:
            logger.warning("No fixtures found, using fallback data")
            return get_fallback_fixtures()
        
        logger.info(f"Successfully scraped {len(fixtures)} AFL fixtures")
        return fixtures
        
    except Exception as e:
        logger.error(f"Error scraping AFL fixtures: {str(e)}")
        return get_fallback_fixtures()

def parse_fixtures_from_text(text_content: str) -> List[Dict]:
    """
    Parse AFL fixtures from the extracted text content
    """
    fixtures = []
    fixture_id = 1
    
    try:
        # Split content into lines and look for fixture patterns
        lines = text_content.split('\n')
        
        # Look for patterns that indicate AFL matches
        # Common patterns: "Team1 vs Team2", "Team1 v Team2", dates, times, venues
        team_names = [
            'Adelaide', 'Brisbane', 'Carlton', 'Collingwood', 'Essendon', 'Fremantle',
            'Geelong', 'Gold Coast', 'GWS Giants', 'Hawthorn', 'Melbourne', 'North Melbourne',
            'Port Adelaide', 'Richmond', 'St Kilda', 'Sydney', 'West Coast', 'Western Bulldogs'
        ]
        
        current_date = None
        current_round = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Look for round information
            if re.search(r'round\s+\d+', line, re.IGNORECASE):
                current_round = line
                continue
            
            # Look for date patterns
            date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}-\d{2}-\d{2})', line)
            if date_match:
                try:
                    date_str = date_match.group(1)
                    # Convert to standard format
                    if '/' in date_str or '-' in date_str:
                        current_date = parse_date_string(date_str)
                except:
                    pass
                continue
            
            # Look for team vs team patterns
            vs_patterns = [r'\s+vs?\s+', r'\s+v\s+', r'\s+@\s+']
            
            for pattern in vs_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Split on the vs pattern
                    teams = re.split(pattern, line, flags=re.IGNORECASE)
                    if len(teams) == 2:
                        team1 = teams[0].strip()
                        team2_and_more = teams[1].strip()
                        
                        # Extract just the team name from team2 (might have venue/time after)
                        team2_parts = team2_and_more.split()
                        team2 = team2_parts[0] if team2_parts else team2_and_more
                        
                        # Check if these look like AFL team names
                        if is_afl_team(team1, team_names) and is_afl_team(team2, team_names):
                            # Look for venue and time in surrounding lines
                            venue = extract_venue(lines, i)
                            time_str = extract_time(lines, i)
                            
                            fixture = {
                                'id': fixture_id,
                                'home_team': clean_team_name(team1, team_names),
                                'away_team': clean_team_name(team2, team_names),
                                'venue': venue or 'TBA',
                                'date': current_date or get_next_weekend_date(),
                                'time': time_str or '15:00',
                                'round': current_round or 'Current Round'
                            }
                            fixtures.append(fixture)
                            fixture_id += 1
                    break
        
        # If we found some fixtures, return them
        if fixtures:
            return fixtures[:8]  # Limit to 8 games per round
        
    except Exception as e:
        logger.error(f"Error parsing fixtures: {str(e)}")
    
    return []

def is_afl_team(team_name: str, team_names: List[str]) -> bool:
    """Check if a string looks like an AFL team name"""
    team_name = team_name.strip()
    
    # Direct match
    if team_name in team_names:
        return True
    
    # Partial match
    for official_name in team_names:
        if team_name.lower() in official_name.lower() or official_name.lower() in team_name.lower():
            return True
    
    # Check for common abbreviations
    abbreviations = {
        'crows': 'Adelaide',
        'lions': 'Brisbane', 
        'blues': 'Carlton',
        'pies': 'Collingwood',
        'bombers': 'Essendon',
        'dockers': 'Fremantle',
        'cats': 'Geelong',
        'suns': 'Gold Coast',
        'giants': 'GWS Giants',
        'hawks': 'Hawthorn',
        'demons': 'Melbourne',
        'roos': 'North Melbourne',
        'power': 'Port Adelaide',
        'tigers': 'Richmond',
        'saints': 'St Kilda',
        'swans': 'Sydney',
        'eagles': 'West Coast',
        'bulldogs': 'Western Bulldogs'
    }
    
    return team_name.lower() in abbreviations

def clean_team_name(team_name: str, team_names: List[str]) -> str:
    """Clean and standardize team name"""
    team_name = team_name.strip()
    
    # Direct match
    if team_name in team_names:
        return team_name
    
    # Find best match
    for official_name in team_names:
        if team_name.lower() in official_name.lower() or official_name.lower() in team_name.lower():
            return official_name
    
    # Check abbreviations
    abbreviations = {
        'crows': 'Adelaide',
        'lions': 'Brisbane', 
        'blues': 'Carlton',
        'pies': 'Collingwood',
        'bombers': 'Essendon',
        'dockers': 'Fremantle',
        'cats': 'Geelong',
        'suns': 'Gold Coast',
        'giants': 'GWS Giants',
        'hawks': 'Hawthorn',
        'demons': 'Melbourne',
        'roos': 'North Melbourne',
        'power': 'Port Adelaide',
        'tigers': 'Richmond',
        'saints': 'St Kilda',
        'swans': 'Sydney',
        'eagles': 'West Coast',
        'bulldogs': 'Western Bulldogs'
    }
    
    return abbreviations.get(team_name.lower(), team_name)

def extract_venue(lines: List[str], current_index: int) -> Optional[str]:
    """Extract venue from surrounding lines"""
    venues = [
        'MCG', 'Marvel Stadium', 'Adelaide Oval', 'Gabba', 'Optus Stadium',
        'SCG', 'ANZ Stadium', 'GMHBA Stadium', 'Metricon Stadium', 'York Park',
        'Docklands', 'Etihad Stadium', 'Telstra Dome', 'Stadium Australia'
    ]
    
    # Check current line and surrounding lines
    for i in range(max(0, current_index - 2), min(len(lines), current_index + 3)):
        line = lines[i].strip()
        for venue in venues:
            if venue.lower() in line.lower():
                return venue
    
    return None

def extract_time(lines: List[str], current_index: int) -> Optional[str]:
    """Extract time from surrounding lines"""
    time_pattern = r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)?'
    
    # Check current line and surrounding lines
    for i in range(max(0, current_index - 2), min(len(lines), current_index + 3)):
        line = lines[i].strip()
        time_match = re.search(time_pattern, line)
        if time_match:
            hour = int(time_match.group(1))
            minute = time_match.group(2)
            period = time_match.group(3)
            
            # Convert to 24-hour format
            if period and period.upper() == 'PM' and hour != 12:
                hour += 12
            elif period and period.upper() == 'AM' and hour == 12:
                hour = 0
            
            return f"{hour:02d}:{minute}"
    
    return None

def parse_date_string(date_str: str) -> str:
    """Parse various date formats and return YYYY-MM-DD"""
    try:
        # Try different date formats
        formats = ['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d', '%d-%m-%Y']
        
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        return get_next_weekend_date()
    except:
        return get_next_weekend_date()

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