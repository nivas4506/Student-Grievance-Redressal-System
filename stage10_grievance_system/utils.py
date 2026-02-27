"""
WEEK 10 Utilities Module
"""

def log_action(msg):
    # This is an internal package utility
    print(f"[SYSTEM LOG] {msg}")

def format_category(cat_name):
    # This is an exported package utility
    return f"*** {cat_name.upper()} ***"
