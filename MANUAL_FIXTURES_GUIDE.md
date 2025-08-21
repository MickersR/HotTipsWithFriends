# Manual AFL Fixtures Guide

## How to Update 2025 AFL Fixtures

The app now supports manual fixture data input through the `manual_fixtures_2025.json` file. This allows you to easily add or update AFL fixtures with accurate data.

## File Structure

The `manual_fixtures_2025.json` file contains:

```json
{
  "season": 2025,
  "rounds": [
    {
      "number": 1,
      "name": "Round 1",
      "fixtures": [
        {
          "id": 1,
          "home_team": "Richmond",
          "away_team": "Carlton", 
          "venue": "MCG",
          "date": "2025-03-13",
          "time": "19:30"
        }
      ]
    }
  ]
}
```

## How to Edit

1. **Open the file**: Edit `manual_fixtures_2025.json` directly in Replit
2. **Add rounds**: Copy the round structure and change the number/name
3. **Add fixtures**: Copy the fixture structure within each round
4. **Update details**: Change team names, venues, dates, and times

## Important Notes

- **Team Names**: Use full team names (e.g., "GWS Giants", "Port Adelaide", "West Coast")
- **Dates**: Use YYYY-MM-DD format (e.g., "2025-03-13")
- **Times**: Use 24-hour format (e.g., "19:30" for 7:30 PM)
- **IDs**: Make each fixture ID unique across all rounds

## Example AFL Team Names

Use these exact team names for consistency:
- Adelaide
- Brisbane  
- Carlton
- Collingwood
- Essendon
- Fremantle
- Geelong
- Gold Coast
- GWS Giants
- Hawthorn
- Melbourne
- North Melbourne
- Port Adelaide
- Richmond
- St Kilda
- Sydney
- West Coast
- Western Bulldogs

## Common AFL Venues

- MCG
- Marvel Stadium
- Adelaide Oval
- Gabba
- SCG
- Optus Stadium
- GMHBA Stadium
- TIO Stadium
- Blundstone Arena
- Manuka Oval
- People First Stadium
- Heritage Bank Stadium
- GIANTS Stadium

## After Editing

1. Save the file
2. The app will automatically use your manual data for 2025 season
3. If no manual data exists, it falls back to the API data
4. Test by selecting 2025 season in the app

## Priority System

For 2025 season data:
1. **First**: Manual fixtures from `manual_fixtures_2025.json`
2. **Fallback**: Squiggle API data
3. **Last resort**: Default fixture data

This system ensures you always have working fixtures while allowing you to override with accurate data.