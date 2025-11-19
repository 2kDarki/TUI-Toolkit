from .textools import style_text, Align
from . import logictools  
import os

def spacer(times):
    for _ in range(times): print()

def underline(line: str="—", hue: str="", alone=False):
    term_width = logictools.get_term_size(True)
    if alone: print()
    print(style_text(line*term_width, hue))
    if alone: print()

def make_progress_bar(pct, width=20):
    filled = int(pct * width)
    return "█" * filled + "▒" * (width - filled)

def rated_bar(pct, width=20):
    control = int(pct * width)
    filled = min(int(pct * width), 7)
    line = "_" * int(pct * 24)
    first = "█" * filled + "▒" * (7 - filled)
    rate = format_int(f"{(pct * 100):.2f}")
    last = "▒" * 7
    if pct > 0.6:
        pct -= 0.6
        filled = min(int(pct * width), 7)
        last = "█" * filled + "▒" * (7 - filled)
        
    return line, f"{first}{rate}%{last}"

def clear(header=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    if header:
        header = Align.center(f"{header}", 0, 1)
        print(header)