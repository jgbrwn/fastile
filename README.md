# FASTile - A Wordle Clone

FASTile is a Wordle clone built using the FastHTML framework. It's a server-rendered hypermedia application that requires minimal JavaScript.

## Features

- Play Wordle with 5, 6, or 7 letter words
- Real dictionary word validation
- Visual keyboard that shows letter statuses
- Responsive design
- No JavaScript required (except for keyboard input handling)

## How to Play

1. The goal is to guess the hidden word in six tries.
2. Each guess must be a valid word from the dictionary.
3. After each guess, the color of the tiles will change to show how close your guess was to the word:
   - Green: The letter is in the correct spot
   - Yellow: The letter is in the word but in the wrong spot
   - Gray: The letter is not in the word

## Requirements

- Python 3.7+
- FastHTML (`pip install python-fasthtml`)

## Running the Application

1. Install the required dependencies:
   ```
   pip install python-fasthtml
   ```

2. Run the application:
   ```
   python main.py
   ```

3. Open your browser and navigate to http://localhost:5001

## Implementation Details

This application is built using FastHTML, which combines:
- Starlette for the web framework
- Uvicorn for the ASGI server
- HTMX for interactive UI without JavaScript
- FastTags for HTML generation in Python

The game logic is entirely server-side, with HTMX handling the interactive elements.
