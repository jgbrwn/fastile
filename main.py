from fasthtml.common import *
import random
import string
from dataclasses import dataclass, asdict
import json
from typing import List, Optional
import os

# Initialize FastHTML app with debug mode to see errors
app, rt = fast_app(
    title="FASTile - Wordle Clone",
    debug=True  # Enable debug mode to see errors
)

# Load dictionary words
def load_dictionary():
    print(f"Current working directory: {os.getcwd()}")
    dictionary_path = "dictionary.txt"
    print(f"Checking if dictionary file exists at: {os.path.abspath(dictionary_path)}")
    print(f"Dictionary file exists: {os.path.exists(dictionary_path)}")
    
    try:
        with open(dictionary_path, "r") as f:
            words = [word.strip().lower() for word in f if word.strip()]
            print(f"Loaded {len(words)} words from dictionary")
            if len(words) < 100:
                print(f"Warning: Dictionary has very few words ({len(words)}). First 10 words: {words[:10]}")
                print("Creating a more comprehensive dictionary...")
                create_basic_dictionary()
                with open(dictionary_path, "r") as f:
                    words = [word.strip().lower() for word in f if word.strip()]
                    print(f"Now loaded {len(words)} words from dictionary")
            return words
    except FileNotFoundError:
        # If dictionary file not found, create a basic one
        # In a real app, we'd use a more complete dictionary
        print("Dictionary file not found, creating a basic one...")
        create_basic_dictionary()
        with open(dictionary_path, "r") as f:
            words = [word.strip().lower() for word in f if word.strip()]
            print(f"Created dictionary with {len(words)} words")
            return words

def create_basic_dictionary():
    # Create a basic dictionary with common words
    # This is just a fallback if no dictionary file exists
    import urllib.request
    try:
        print("Attempting to download dictionary from GitHub...")
        url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
        with urllib.request.urlopen(url) as response:
            words = response.read().decode('utf-8').splitlines()
            # Filter words by length and only keep alphabetic words
            filtered_words = [word.lower() for word in words 
                             if word.isalpha() and 5 <= len(word) <= 7]
            
            print(f"Downloaded {len(filtered_words)} words")
            with open("dictionary.txt", "w") as f:
                f.write("\n".join(filtered_words))
    except Exception as e:
        print(f"Download failed: {e}")
        # If download fails, create a minimal dictionary
        basic_words = [
            "apple", "beach", "chair", "dance", "earth", "flame", "grape", "house",
            "igloo", "juice", "knife", "lemon", "music", "night", "ocean", "piano",
            "queen", "river", "sugar", "table", "uncle", "voice", "water", "youth",
            "zebra", "abroad", "bright", "castle", "dragon", "escape", "forest",
            "garden", "heaven", "island", "jungle", "kitchen", "legend", "market",
            "nature", "orange", "planet", "quartz", "rabbit", "summer", "travel",
            "unique", "violet", "window", "xylophone", "yellow", "zephyr", "amazing",
            "balloon", "captain", "diamond", "elegant", "fantasy", "glitter", "harmony",
            "there", "where", "which", "about", "would", "these", "other", "words",
            "could", "write", "first", "water", "after", "right", "think", "three",
            "years", "place", "sound", "great", "again", "still", "every", "small",
            "found", "those", "never", "under", "might", "while", "house", "world",
            "below", "asked", "going", "large", "until", "along", "shall", "being",
            "often", "earth", "began", "since", "study", "night", "light", "above",
            "paper", "parts", "young", "story", "point", "times", "heard", "whole",
            "white", "given", "means", "music", "miles", "thing", "today", "later",
            "using", "money", "lines", "order", "group", "among", "learn", "known",
            "space", "table", "early", "trees", "short", "hands", "state", "black",
            "shown", "stood", "front", "voice", "kinds", "makes", "comes", "close",
            "power", "lived", "vowel", "taken", "built", "heart", "ready", "quite",
            "class", "bring", "round", "horse", "shows", "piece", "green", "stand",
            "birds", "start", "river", "tried", "least", "field", "whose", "girls",
            "leave", "added", "color", "third", "hours", "moved", "plant", "doing",
            "names", "forms", "heavy", "ideas", "cried", "check", "floor", "begin",
            "woman", "alone", "plane", "spell", "watch", "carry", "wrote", "clear",
            "named", "books", "child", "glass", "human", "takes", "party", "build",
            "seems", "blood", "sides", "seven", "mouth", "solve", "north", "value",
            "death", "maybe", "happy", "tells", "gives", "looks", "shape", "lives",
            "steps", "areas", "sense", "speak", "force", "ocean", "speed", "women",
            "metal", "south", "grass", "scale", "cells", "lower", "sleep", "wrong",
            "pages", "ships", "needs", "rocks", "eight", "major", "level", "total",
            "ahead", "reach", "stars", "store", "sight", "terms", "catch", "works",
            "board", "cover", "songs", "equal", "stone", "waves", "guess", "dance",
            "spoke", "break", "cause", "radio", "weeks", "lands", "basic", "liked",
            "trade", "fresh", "final", "fight", "meant", "drive", "spent", "local",
            "waxes", "knows", "train", "bread", "homes", "teeth", "coast", "thick",
            "brown", "clean", "quiet", "sugar", "facts", "steel", "forth", "rules",
            "notes", "units", "peace", "month", "verbs", "seeds", "helps", "sharp",
            "visit", "woods", "chief", "walls", "cross", "wings", "grown", "cases",
            "foods", "crops", "fruit", "stick", "wants", "stage", "sheep", "nouns",
            "plain", "drink", "bones", "apart", "turns", "moves", "touch", "angle",
            "based", "range", "marks", "tired", "older", "farms", "spend", "shoes",
            "goods", "chair", "twice", "cents", "empty", "alike", "style", "broke",
            "pairs", "count", "enjoy", "score", "shore", "roots", "paint", "heads",
            "shook", "serve", "angry", "crowd", "wheel", "quick", "dress", "share",
            "alive", "noise", "solid", "cloth", "signs", "hills", "types", "drawn",
            "worth", "truck", "piano", "upper", "loved", "usual", "faces", "drove",
            "cabin", "boats", "towns", "proud", "court", "model", "prime", "fifty",
            "plans", "yards", "prove", "tools", "price", "sheet", "smell", "boxes",
            "raise", "match", "truth", "roads", "threw", "enemy", "lunch", "chart",
            "scene", "graph", "doubt", "guide", "winds", "block", "grain", "smoke",
            "mixed", "games", "wagon", "sweet", "topic", "extra", "plate", "title",
            "knife", "fence", "falls", "cloud", "wheat", "plays", "enter", "broad",
            "steam", "atoms", "press", "lying", "basis", "clock", "taste", "grows",
            "thank", "storm", "agree", "brain", "track", "smile", "funny", "beach",
            "stock", "hurry", "saved", "sorry", "giant", "trail", "offer", "ought",
            "rough", "daily", "avoid", "keeps", "throw", "allow", "cream", "laugh",
            "edges", "teach", "frame", "bells", "dream", "magic", "occur", "ended",
            "chord", "false", "skill", "holes", "dozen", "brave", "apple", "climb",
            "outer", "pitch", "ruler", "holds", "fixed", "costs", "calls", "blank",
            "staff", "labor", "eaten", "youth", "tones", "honor", "globe", "gases",
            "doors", "poles", "loose", "apply", "tears", "exact", "brush", "chest",
            "layer", "whale", "minor", "faith", "tests", "judge", "items", "worry",
            "waste", "hoped", "strip", "begun", "aside", "lakes", "bound", "depth",
            "candy", "event", "worse", "aware", "shell", "rooms", "ranch", "image",
            "snake", "aloud", "dried", "likes", "motor", "pound", "knees", "refer",
            "fully", "chain", "shirt", "flour", "drops", "spite", "orbit", "banks",
            "shoot", "curve", "tribe", "tight", "blind", "slept", "shade", "claim",
            "flies", "theme", "queen", "fifth", "union", "hence", "straw", "entry",
            "issue", "birth", "feels", "anger", "brief", "rhyme", "glory", "guard",
            "flows", "flesh", "owned", "trick", "yours", "sizes", "noted", "width",
            "burst", "route", "lungs", "uncle", "bears", "royal", "kings", "forty",
            "trial", "cards", "brass", "opera", "chose", "owner", "vapor", "beats",
            "mouse", "tough", "wires", "meter", "tower", "finds", "inner", "stuck",
            "arrow", "poems", "label", "swing", "solar", "truly", "tense", "beans",
            "split", "rises", "weigh", "hotel", "stems", "pride", "swung", "grade",
            "digit", "badly", "boots", "pilot", "sales", "swept", "lucky", "prize",
            "stove", "tubes", "acres", "wound", "steep", "slide", "trunk", "error",
            "porch", "slave", "exist", "faced", "mines", "marry", "juice", "raced",
            "waved", "goose", "trust", "fewer", "favor", "mills", "views", "joint",
            "eager", "spots", "blend", "rings", "adult", "index", "nails", "horns",
            "balls", "flame", "rates", "drill", "trace", "skins", "waxed", "seats",
            "stuff", "ratio", "minds", "dirty", "silly", "coins", "hello", "trips",
            "leads", "rifle", "hopes", "bases", "shine", "bench", "moral", "fires",
            "meals", "shake", "shops", "cycle", "movie", "slope", "canoe", "teams",
            "folks", "fired", "bands", "thumb", "shout", "canal", "habit", "reply",
            "ruled", "fever", "crust", "shelf", "walks", "midst", "crack", "print",
            "tales", "coach", "stiff", "flood", "verse", "awake", "rocky", "share",
            "crept", "sweat", "paths", "least", "grain", "brush", "jelly", "ought"
        ]
        with open("dictionary.txt", "w") as f:
            f.write("\n".join(basic_words))

# Game state
@dataclass
class GameState:
    target_word: str
    guesses: List[str] = None
    current_guess: str = ""
    message: str = ""
    message_type: str = ""
    game_over: bool = False
    won: bool = False
    word_length: int = 5
    
    def __post_init__(self):
        if self.guesses is None:
            self.guesses = []
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

# Dictionary of words
all_words = load_dictionary()

# Session management
def get_game_state(session):
    if 'game' not in session:
        session['game'] = create_new_game(5).to_dict()  # Store as dict
    return GameState.from_dict(session['game'])  # Convert back to GameState

def reset_game_state(session, word_length=5):
    """Reset the game state completely"""
    session['game'] = create_new_game(word_length).to_dict()
    return GameState.from_dict(session['game'])

def create_new_game(word_length):
    # Filter words by length
    words_of_length = [word for word in all_words if len(word) == word_length]
    if not words_of_length:
        # Fallback if no words of this length
        words_of_length = [word for word in all_words if len(word) == 5]
        word_length = 5
    
    target_word = random.choice(words_of_length)
    return GameState(target_word=target_word, word_length=word_length)

# Helper functions
def evaluate_guess(guess, target):
    """Evaluate a guess against the target word"""
    print(f"Evaluating guess '{guess}' against target '{target}'")
    
    result = []
    # Convert both to lowercase for comparison
    guess = guess.lower()
    target = target.lower()
    target_chars = list(target)
    
    # First pass: mark correct positions
    for i, char in enumerate(guess):
        if i < len(target) and char == target[i]:
            result.append("correct")
            target_chars[i] = None  # Mark as used
        else:
            result.append(None)  # Placeholder
    
    # Second pass: mark present but incorrect positions
    for i, char in enumerate(guess):
        if result[i] is None:  # Not already marked as correct
            if char in target_chars:
                result[i] = "present"
                target_chars[target_chars.index(char)] = None  # Mark as used
            else:
                result[i] = "absent"
    
    print(f"Evaluation result: {result}")
    return result

# Routes
@rt("/")
def get(sess):
    """Main game route"""
    # Always reset game state on page load
    game_state = reset_game_state(sess, 5)
    sess['game'] = game_state.to_dict()
    
    # Add CSS
    css = Style("""
        :root {
            --correct-color: #6aaa64;
            --present-color: #c9b458;
            --absent-color: #787c7e;
            --key-bg: #d3d6da;
            --key-text: #1a1a1b;
        }
        
        body {
            font-family: 'Clear Sans', 'Helvetica Neue', Arial, sans-serif;
            max-width: 500px;
            margin: 0 auto;
            text-align: center;
        }
        
        header {
            border-bottom: 1px solid #d3d6da;
            margin-bottom: 1rem;
            padding: 0.5rem;
        }
        
        h1 {
            font-weight: 700;
            font-size: 2rem;
            margin: 0;
            letter-spacing: 0.2rem;
        }
        
        .game-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .board {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.25rem;
            margin: 0 auto;
            max-width: 100%;
            padding: 1rem;
        }
        
        .row {
            display: grid;
            grid-gap: 5px;
            width: 100%;
        }
        
        .tile {
            display: inline-flex;
            justify-content: center;
            align-items: center;
            width: 3.5rem;
            height: 3.5rem;
            border: 2px solid #d3d6da;
            font-size: 2rem;
            font-weight: bold;
            vertical-align: middle;
            text-transform: uppercase;
            user-select: none;
        }
        .tile.evaluated {
            transition: background-color 0.5s ease, color 0.5s ease;
            animation: flip 0.5s ease forwards;
        }
        .tile.correct {
            background-color: #6aaa64;
            color: white;
        }
        .tile.present {
            background-color: #c9b458;
            color: white;
        }
        .tile.absent {
            background-color: #787c7e;
            color: white;
        }
        
        @keyframes flip {
            0% { transform: rotateX(0); }
            50% { transform: rotateX(90deg); }
            100% { transform: rotateX(0); }
        }
        
        .keyboard {
            margin: 1rem 0;
            user-select: none;
            width: 100%;
            max-width: 500px;
        }
        
        .keyboard-row {
            display: flex;
            justify-content: center;
            width: 100%;
            margin: 0 auto 8px;
            touch-action: manipulation;
        }
        
        .key {
            font-family: inherit;
            font-weight: bold;
            border: 0;
            padding: 0;
            margin: 0 6px 0 0;
            height: 3.5rem;
            border-radius: 4px;
            cursor: pointer;
            user-select: none;
            background-color: var(--key-bg);
            color: var(--key-text);
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            text-transform: uppercase;
            -webkit-tap-highlight-color: rgba(0,0,0,0.3);
        }
        
        .key:last-of-type {
            margin: 0;
        }
        
        .key.wide {
            flex: 1.5;
        }
        
        .key.correct {
            background-color: var(--correct-color);
            color: white;
        }
        
        .key.present {
            background-color: var(--present-color);
            color: white;
        }
        
        .key.absent {
            background-color: var(--absent-color);
            color: white;
        }
        
        .message {
            margin: 1rem 0;
            font-weight: bold;
        }
        
        .message.error {
            color: #d93025;
        }
        
        .message.success {
            color: var(--correct-color);
        }
        
        .word-length-selector {
            margin: 1rem 0;
        }
        
        .word-length-selector button {
            margin: 0 0.5rem;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            font-weight: bold;
            border-radius: 4px;
            cursor: pointer;
            background-color: var(--key-bg);
            color: var(--key-text);
            border: none;
        }
        
        .word-length-selector button.selected {
            background-color: var(--key-text);
            color: white;
        }
    """)
    
    # Return the complete page
    return Titled(
        "FASTile - Wordle Clone",
        css,
        NotStr(render_game_container(game_state)),
        Script("""
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                document.querySelector('button[hx-post="/guess"]').click();
            } else if (event.key === 'Backspace') {
                document.querySelector('button[hx-post="/backspace"]').click();
            } else if (/^[a-z]$/.test(event.key)) {
                const keyButton = document.querySelector(`button[hx-post="/key/${event.key}"]`);
                if (keyButton) keyButton.click();
            }
        });
        """)
    )

@rt("/key/{key}")
def post(key: str, sess):
    """Handle key press"""
    game_state = get_game_state(sess)
    
    # Ignore if game is over
    if game_state.game_over:
        sess['game'] = game_state.to_dict()
        return NotStr(render_game_container(game_state))
    
    # Add the key to the current guess if it's not full
    if len(game_state.current_guess) < game_state.word_length:
        game_state.current_guess += key
        game_state.message = ""
    
    # Save game state back to session
    sess['game'] = game_state.to_dict()
    
    return NotStr(render_game_container(game_state))

@rt("/backspace")
def post(sess):
    """Handle backspace"""
    game_state = get_game_state(sess)
    
    # Ignore if game is over
    if game_state.game_over:
        sess['game'] = game_state.to_dict()
        return NotStr(render_game_container(game_state))
    
    # Remove last character if there is one
    if len(game_state.current_guess) > 0:
        game_state.current_guess = game_state.current_guess[:-1]
        game_state.message = ""
    
    # Save game state back to session
    sess['game'] = game_state.to_dict()
    
    return NotStr(render_game_container(game_state))

@rt("/guess")
def post(sess):
    """Handle guess submission"""
    game_state = get_game_state(sess)
    
    # Check if the game is already over
    if game_state.game_over:
        game_state.message = "Game is already over. Start a new game."
        game_state.message_type = "error"
        sess['game'] = game_state.to_dict()
        return NotStr(render_game_container(game_state))
    
    # Check if the guess is complete
    if len(game_state.current_guess) != game_state.word_length:
        game_state.message = f"Your guess must be {game_state.word_length} letters."
        game_state.message_type = "error"
        sess['game'] = game_state.to_dict()
        return NotStr(render_game_container(game_state))
    
    # Check if the guess is a valid word
    valid_words = [word for word in all_words if len(word) == game_state.word_length]
    if game_state.current_guess.lower() not in valid_words:
        game_state.message = "Not in word list."
        game_state.message_type = "error"
        sess['game'] = game_state.to_dict()
        return NotStr(render_game_container(game_state))
    
    # Add the guess to the list of guesses
    game_state.guesses.append(game_state.current_guess)
    
    # Check if the guess is correct
    if game_state.current_guess.lower() == game_state.target_word.lower():
        game_state.game_over = True
        game_state.won = True
        game_state.message = "You won!"
        game_state.message_type = "success"
    # Check if the player has used all 6 guesses
    elif len(game_state.guesses) >= 6:
        game_state.game_over = True
        game_state.message = f"Game over. The word was {game_state.target_word.upper()}."
        game_state.message_type = "error"
    
    # Reset the current guess
    game_state.current_guess = ""
    
    # Save the updated game state
    sess['game'] = game_state.to_dict()
    
    # Return the updated game container
    return NotStr(render_game_container(game_state))

@rt("/new-game/{word_length}")
def post(word_length: int, sess):
    """Start a new game with the specified word length"""
    # Validate word length
    if word_length not in [5, 6, 7]:
        word_length = 5
    
    # Reset game state with correct word length
    game_state = reset_game_state(sess, word_length)
    game_state.word_length = word_length
    sess['game'] = game_state.to_dict()
    
    # Return just the game container
    return NotStr(render_game_container(game_state))

def render_game_container(game_state):
    # Create a simple board
    board_rows = []
    for i in range(6):  # 6 rows for 6 guesses
        row_tiles = []
        for j in range(game_state.word_length):
            # Check if this position has a letter from a previous guess
            if i < len(game_state.guesses):
                guess = game_state.guesses[i]
                if j < len(guess):
                    # Get the evaluation for this letter
                    evaluation = evaluate_guess(guess, game_state.target_word)
                    tile_class = f"tile {evaluation[j]}"
                    # Only add evaluated class to the current guess row
                    if i == len(game_state.guesses) - 1:
                        tile_class += " evaluated"
                    row_tiles.append(f'<div class="{tile_class}">{guess[j].upper()}</div>')
                else:
                    row_tiles.append('<div class="tile"></div>')
            # Check if this position has a letter from the current guess
            elif i == len(game_state.guesses) and j < len(game_state.current_guess):
                row_tiles.append(f'<div class="tile filled">{game_state.current_guess[j].upper()}</div>')
            else:
                row_tiles.append('<div class="tile"></div>')
        
        row_style = f'grid-template-columns: repeat({game_state.word_length}, 1fr); width: 100%;'
        board_rows.append(f'<div class="row" style="{row_style}">{"".join(row_tiles)}</div>')
    
    board = f'<div class="board" id="game-board">{"".join(board_rows)}</div>'
    
    # Create the keyboard
    keyboard_rows = [
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]
    
    keyboard_elements = []
    
    # Get keyboard states based on guesses
    key_states = {}
    for guess in game_state.guesses:
        evaluation = evaluate_guess(guess, game_state.target_word)
        for i, char in enumerate(guess):
            # Only update if the current state is better
            current_state = key_states.get(char, "")
            if evaluation[i] == "correct":
                key_states[char] = "correct"
            elif evaluation[i] == "present" and current_state != "correct":
                key_states[char] = "present"
            elif evaluation[i] == "absent" and not current_state:
                key_states[char] = "absent"
    
    for i, row in enumerate(keyboard_rows):
        row_keys = []
        
        # Add Enter key to the start of the last row
        if i == 2:
            enter_class = "key wide"
            row_keys.append(f'<button class="{enter_class}" hx-post="/guess" hx-trigger="click" hx-target="#game-container">Enter</button>')
        
        # Add letter keys
        for char in row:
            key_class = f"key {key_states.get(char, '')}"
            row_keys.append(
                f'<button class="{key_class}" hx-post="/key/{char}" hx-trigger="click" hx-target="#game-container">{char}</button>'
            )
        
        # Add Backspace key to the end of the last row
        if i == 2:
            backspace_class = "key wide"
            row_keys.append(f'<button class="{backspace_class}" hx-post="/backspace" hx-trigger="click" hx-target="#game-container">←</button>')
        
        keyboard_elements.append(f'<div class="keyboard-row">{"".join(row_keys)}</div>')
    
    keyboard = f'<div class="keyboard" id="keyboard">{"".join(keyboard_elements)}</div>'
    
    # Create word length selector
    if len(game_state.guesses) == 0 and not game_state.current_guess:
        options = [5, 6, 7]
        buttons = []
        
        for length in options:
            cls = "selected" if length == game_state.word_length else ""
            buttons.append(
                f'<button class="{cls}" hx-post="/new-game/{length}" hx-trigger="click" hx-target="#game-container">{length}</button>'
            )
        
        word_length_selector = f'''
        <div class="word-length-selector">
            <p>Select word length:</p>
            <div>{"".join(buttons)}</div>
        </div>
        '''
    else:
        word_length_selector = ""
    
    # Create message element
    message_element = ""
    if game_state.message:
        message_element = f'<div class="message {game_state.message_type}" id="message">{game_state.message}</div>'
    
    # Create game over elements
    game_over_elements = ""
    if game_state.game_over:
        if game_state.won:
            congrats = f"Congratulations! You guessed the word in {len(game_state.guesses)} tries."
            game_over_elements += f'<div class="message success">{congrats}</div>'
        else:
            target_reveal = f"The word was: {game_state.target_word.upper()}"
            game_over_elements += f'<div class="message">{target_reveal}</div>'
        
        game_over_elements += f'''
        <div style="margin-top: 1rem;">
            <button hx-post="/new-game/{game_state.word_length}" hx-trigger="click" hx-target="#game-container">New Game</button>
        </div>
        '''
    
    # Combine all elements
    game_container = f'''
    <div id="game-container" class="game-container">
        <header>
            <h1>FASTile</h1>
        </header>
        {word_length_selector}
        {board}
        {message_element}
        {game_over_elements}
        {keyboard}
    </div>
    '''
    return game_container

# Start the server
serve()
