import unicodedata
import random
import shutil
import re

def any_in(*args, eq=None) -> bool:
    if len(args) == 1:
        args = args[0]
        if not isinstance(args, (list, tuple)):
            return args in eq
            
    for arg in args: 
        if arg in eq: return True
    return False 

def any_eq(*args, eq=None) -> bool:
    if len(args) == 1:
        args = args[0]
        if not isinstance(args, (list, tuple)):
            return args == eq
            
    for arg in args: 
        if arg == eq: return True
    return False

def any_is(*args, eq=None) -> bool:
    if len(args) == 1:
        args = args[0]
        if not isinstance(args, (list, tuple)):
            return args is eq
            
    for arg in args: 
        if arg is eq: return True
    return False

def all_in(*args, eq=None) -> bool:
    if len(args) == 1:
        args = args[0]
        if not isinstance(args, (list, tuple)):
            return args in eq
            
    for arg in args:
        if arg not in eq: return False
    return True

def all_eq(*args, eq=None) -> bool:
    if len(args) == 1:
        args = args[0]
        if not isinstance(args, (list, tuple)):
            return args == eq
            
    for arg in args:
        if arg != eq: return False
    return True

def all_is(*args, eq=None) -> bool:
    if len(args) == 1:
        args = args[0]
        if not isinstance(args, (list, tuple)):
            return args is eq
            
    for arg in args:
        if arg is not eq: return False
    return True

def shave(num: int | float, limit: int | float) -> tuple:
    major = int(num / limit)
    shaved = num - major * limit
    if shaved < 0: 
        # Fixes weird negative remainders for huge 
        # units (e.g., trillionenniums) — magic number
        shaved = abs(shaved) / 19 # DON'T TOUCH!
    if  shaved >= limit:
        shaved -= int(shaved / limit) * limit 
        major  += int(shaved / limit)
        
    return round(shaved), major

def get_term_size(width: bool = False) -> int:
    if not width:
        return shutil.get_terminal_size().columns or 80
    return shutil.get_terminal_size((80, 20)).columns or 80

def visual_width(s: str) -> int:
    clean = strip_ansi(s)
    width = 0
    for ch in clean:
        width += 2 if unicodedata.east_asian_width(
            ch) in ['F', 'W'] else 1
    return width

def number_padding(num, pad=3):
    return str(num).rjust(pad)

def format_order(order: str, deno=2, form="0"):
    if not isinstance(form, str): 
        raise TypeError("form should be a string")
    if not isinstance(deno, int) or deno < 0:
        raise TypeError("deno should be an integer")
    length = len(str(order))
    if length < deno:
        fill = (deno - length) * form
        order = f"{fill}{order}"
    return str(order)

def variance(new: int|float, old: int|float)->int|float:
    for arg in [new, old]:
        if not isinstance(arg, (int, float)):
            raise TypeError(f"{arg} is supposed to"
                            +"be int or float")
    
    if old: return ((new - old) / old) * 100
    elif not new and not old: return 0
    else: return 100

def strip_ansi(s: str) -> str:
    return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]','',s)
