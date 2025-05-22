#!/usr/bin/env python3
"""
Interactive Google Autocomplete CLI Tool
Fetches and displays Google search autocomplete suggestions for user-provided keywords.
"""

import requests
import json
import sys
from urllib.parse import quote
import arabic_reshaper
from bidi.algorithm import get_display
import os

# Load language configurations
def load_language_config():
    """
    Load language configurations from external file.
    Returns a dictionary of language settings.
    """
    config_path = 'language_config.json'
    default_config = {
        'languages': {
            '1': {'code': 'en', 'name': 'English', 'rtl': False},
            '2': {'code': 'he', 'name': 'Hebrew', 'rtl': True}
        }
    }
    
    if not os.path.exists(config_path):
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        return default_config
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_google_autocomplete(keyword, lang="en"):
    """
    Fetch Google autocomplete suggestions for a given keyword.
    
    Args:
        keyword (str): The search keyword
        lang (str): Language code (default: "en")
    
    Returns:
        list: List of autocomplete suggestions
    """
    try:
        # URL encode the keyword to handle special characters
        encoded_keyword = quote(keyword)
        url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={encoded_keyword}&hl={lang}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse JSON response - suggestions are in the second element
        suggestions = json.loads(response.text)[1]
        return suggestions
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Please check your internet connection.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching suggestions: {e}")
        return []
    except (IndexError, json.JSONDecodeError):
        print("❌ Unexpected response format from Google.")
        return []

def process_rtl_text(text, is_rtl):
    """
    Process text based on its direction (RTL or LTR).
    
    Args:
        text (str): The text to process
        is_rtl (bool): Whether the text is RTL
    
    Returns:
        str: Processed text
    """
    if is_rtl:
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)
    return text

def display_suggestions(keyword, suggestions, is_rtl=False):
    """
    Display the autocomplete suggestions in a formatted way.
    
    Args:
        keyword (str): The original search keyword
        suggestions (list): List of suggestions to display
        is_rtl (bool): Whether the text is RTL
    """
    processed_keyword = process_rtl_text(keyword, is_rtl)
    print(f"\n🔍 Autocomplete suggestions for '{processed_keyword}':")
    print("=" * (len(processed_keyword) + 35))
    
    if not suggestions:
        print("No suggestions found.")
        return
    
    for i, suggestion in enumerate(suggestions, 1):
        processed_suggestion = process_rtl_text(suggestion, is_rtl)
        print(f"{i:2d}. {processed_suggestion}")
    
    print(f"\nFound {len(suggestions)} suggestion(s)")

def get_language_choice():
    """
    Let user choose language for autocomplete.
    
    Returns:
        tuple: (language code, is_rtl)
    """
    config = load_language_config()
    languages = config['languages']
    
    print("\n🌐 Select language:")
    for key, lang_info in languages.items():
        print(f"{key:2s}. {lang_info['name']} ({lang_info['code']})")
    
    while True:
        choice = input("\nEnter choice (1-2, or press Enter for English): ").strip()
        
        if not choice:  # Default to English
            return 'en', False
        
        if choice in languages:
            lang_info = languages[choice]
            return lang_info['code'], lang_info['rtl']
        
        print("❌ Invalid choice. Please enter a number between 1-2.")

def main():
    """
    Main interactive loop for the CLI tool.
    """
    print("🚀 Google Autocomplete Suggestion Tool")
    print("=" * 40)
    
    # Get language preference
    lang, is_rtl = get_language_choice()
    
    print(f"\n✅ Language set to: {lang}")
    print("\n💡 Tips:")
    print("  - Type 'quit', 'exit', or 'q' to exit")
    print("  - Type 'lang' to change language")
    print("  - Press Ctrl+C to exit anytime")
    
    try:
        while True:
            print("\n" + "-" * 40)
            keyword = input("🔤 Enter keyword to search: ").strip()
            
            # Handle exit commands
            if keyword.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Handle language change
            if keyword.lower() == 'lang':
                lang, is_rtl = get_language_choice()
                print(f"✅ Language changed to: {lang}")
                continue
            
            # Validate input
            if not keyword:
                print("❌ Please enter a valid keyword.")
                continue
            
            # Fetch and display suggestions
            print(f"\n⏳ Fetching suggestions for '{process_rtl_text(keyword, is_rtl)}'...")
            suggestions = get_google_autocomplete(keyword, lang)
            display_suggestions(keyword, suggestions, is_rtl)
            
            # Ask if user wants to continue
            continue_choice = input("\n❓ Search another keyword? (y/n): ").strip().lower()
            if continue_choice in ['n', 'no']:
                print("\n👋 Thanks for using Google Autocomplete Tool!")
                break
                
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()