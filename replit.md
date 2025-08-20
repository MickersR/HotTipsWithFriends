# AFL Tipping App

## Overview

An AFL (Australian Football League) tipping application that allows users to submit and share match predictions securely. The app enables users to select winning teams for AFL fixtures, add margin predictions, and encrypt their tips with a password for secure sharing. Built with Flask and featuring client-side encryption for privacy protection.

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

### Mock Data
- **AFL Fixtures**: Hardcoded fixture data for current implementation (designed to be replaced with external AFL API)

### Future Integration Opportunities
- AFL official API for live fixture data
- Database migration to PostgreSQL for production
- External authentication providers if needed