# Hot Tips with Friends

## Overview

An AFL (Australian Football League) tipping application called "Hot Tips with Friends" that allows users to submit and share match predictions securely. The app enables users to select winning teams for AFL fixtures, add margin predictions, and encrypt their tips with a password for secure sharing. Built with Flask and featuring client-side encryption for privacy protection.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **CSS Framework**: Bootstrap 5 with dark theme for responsive UI design
- **Client-side Encryption**: CryptoJS library for AES encryption/decryption in the browser
- **Interactive Elements**: JavaScript for form handling and encryption operations
- **Styling**: Custom CSS with AFL-themed color scheme and enhanced card/button interactions

### Backend Architecture
- **Web Framework**: Flask as the lightweight Python web framework
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension for database operations
- **Model Structure**: Simple Tip model storing encrypted tip data with user identification
- **Routing**: Centralized route definitions with separation from application initialization
- **Session Management**: Flask sessions with configurable secret keys
- **Proxy Support**: ProxyFix middleware for handling proxy headers in deployment environments

### Data Storage Solutions
- **Database**: SQLite for development with PostgreSQL compatibility through SQLAlchemy
- **Schema Design**: Single Tip table with encrypted JSON data storage approach
- **Connection Pooling**: Configured with pool recycling and connection health checks
- **Data Encryption**: Client-side AES encryption before database storage for privacy

### Authentication and Authorization
- **Encryption-based Security**: Password-based encryption instead of traditional user authentication
- **Client-side Processing**: All encryption/decryption happens in the browser for maximum privacy
- **No User Sessions**: Stateless approach where tips are accessed via encrypted strings and passwords

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework
- **SQLAlchemy**: Database ORM and toolkit
- **Werkzeug**: WSGI utilities including ProxyFix middleware

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome**: Icon library for UI elements
- **CryptoJS**: JavaScript cryptography library for AES encryption

### Development Tools
- **Python Logging**: Built-in logging configuration for debugging
- **Environment Variables**: Configuration through environment variables for deployment flexibility

### Web Scraping Integration
- **AFL Fixtures**: Real-time fixture data scraped from austadiums.com using Trafilatura
- **Caching System**: 12-hour cache to minimize excessive requests to external source
- **Fallback System**: Automatic fallback to generated fixture data if scraping fails
- **Data Processing**: Intelligent parsing of team names, venues, dates, and times from scraped content

### Recent Changes (August 2025)
- **Removed Feature Marketing**: Cleaned up home page by removing feature advertisements and "How It Works" sections per user request
- **Implemented Live Data**: Replaced mock AFL fixtures with real Squiggle API integration after web scraping failed
- **API Integration**: Successfully integrated with Squiggle API using proper User-Agent headers
- **Round Selector**: Added comprehensive round dropdown with all 23 regular season rounds plus finals
- **2025 Season Data**: Updated app to use 2025 AFL fixtures as default, discovered Squiggle API has current season data available
- **Multi-Year Support**: Added year selector allowing users to choose between 2024 and 2025 AFL seasons
- **Enhanced Timestamp System**: Implemented UTC timestamp storage with browser timezone display and relative time formatting
- **Improved Data Structure**: Added year information to encrypted tip data for proper fixture matching when viewing tips

### Future Integration Opportunities
- Database migration to PostgreSQL for production
- External authentication providers if needed
- Enhanced scraping with additional AFL data sources