from tuikit.exceptions import validate, InputError
from tuikit import logictools
import unicodedata
import textwrap
import time
import re

class Align:
    def right(self, arg: str) -> str:
        try: return wrap_text(arg.strip())
        except AttributeError: __err__(arg, "string")
    
    def center(self, arg, line: str = " ", 
               hue: str = "", line_hue: str = "", 
               pad: int = 0, get_pad: bool = False
               ) -> str | tuple:
        # Validate parameters
        validate(
            [line, str, "string"],
            [[hue, line_hue], str, "color"],
            [pad, int, "natural number", "less", 0],
            err=__err__
        )
        
        arg = str(arg)
        
        term_width = logictools.get_term_size(69) # ;)
        vis_width  = logictools.visual_width(arg)
    
        total_pad = max(term_width - vis_width, 0)
        left_pad  = total_pad // 2
        right_pad = total_pad - left_pad
    
        if get_pad:
            return left_pad, total_pad, right_pad

        left   = style_text(line *  left_pad, line_hue)
        right  = style_text(line * right_pad, line_hue)
        middle = style_text(arg, hue)
        
        if len(arg) > term_width:
            if pad: total_pad += pad * 2
            return wrap_text(middle, from_center=[hue, 
                line, line_hue, total_pad]) 
        
        return f"{left}{middle}{right}"
    
    def left(self, arg, pad: int = 4) -> str:
        validate(
            [pad, int,  "natural number", "less", 0],
            err=__err__
        )
        return wrap_text(str(arg), pad, pad)

def strip_ansi(s: str) -> str:
    if not isinstance(s, str): __err__(s, "string") 
    return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]','',s)

def visual_width(s: str) -> int:
    clean = strip_ansi(s)
    width = 0
    for ch in clean:
        width += 2 if unicodedata.east_asian_width(
            ch) in ['F', 'W'] else 1
    return width

def pluralize(n: int | float, word: str) -> str:
    # Validate parameters
    validate(
        [n, [int, float], "integer or float"],
        err=__err__
    )
    strip_ansi(word) # relegating validation
    
    if n == 1: return word
    else:
        if word.endswith('y') and len(word) > 3: 
            return word[:-1]+"ies"
        return word + 's'

def style_text(text, fg: str = "", bg: str = "",
               underline: bool = False,
               bold: bool = False) -> str:
    
    validate(
        [[fg, bg], str, "color"],
        [[underline, bold], bool, "boolean"],
        err=__err__
    )
    
    text = str(text)
    if has_unicode(text): text = preserve_codes(text)
    
    colors = {
        "black": 30, "red": 31, "green": 32, 
        "yellow": 33, "blue": 34, "magenta": 35,
        "cyan": 36, "white": 37,
        "gray": 90, "lightred": 91, "lightgreen": 92,
        "lightyellow": 93, "purple": 94,
        "lightmagenta": 95, "lightcyan": 96
    }

    for c in [fg, bg]:
        if c and c not in colors: __err__(c, "color")
    
    style = []
    
    if bold: style.append("1")
    if underline: style.append("4")
    if fg: style.append(str(colors[fg]))
    if bg: style.append(str(colors[bg] + 10))

    if style:
        return f"\033[{';'.join(style)}m{text}\033[0m"
    return text

def wrap_text(text: str, indent: int = 0, pad: int = 0, 
              inline: bool = False, order: str = '', 
              from_center: list = []) -> str:
    
    # Validate parameters
    validate(
      [[text, order], str, "string"],
      [[indent, pad], int, "natural number","less",0],
      [inline, bool, "boolean"],
      [from_center, list, "list"], err=__err__)
    
    width = logictools.get_term_size()
    styled_words = text.split()
    
    if from_center:
        h, l, lh, total_pad = from_center
        width -= total_pad
        centered, res = "", ""
        pos = 0
    
    # Adjust margin based on length of order
    # order is a tag for an ordered list (e.g., 1., a., 
    # IV., 10. etc)
    length = len(order) - 2 if inline else len(order)
    trailing = length / (10 ** len(str(length))
        ) if not inline else 0
    if length>9 and not inline: trailing = length*2/10
    margin = 1 + trailing
    
    # Insert line breaks
    line_len = len(order)
    result = order if not inline else ""
    
    if pad:
        result = " " * (pad-1)
        line_len = pad
    
    for i, word in enumerate(styled_words):
        used = line_len + visual_width(word)
        if used + margin > width:
            if from_center:
                text = " ".join(styled_words[pos:i])
                centered += align.center(text.strip(), 
                    line=l, hue=h, line_hue=lh) + "\n"
                pos = i
                res = word
            else: result += '\n' + ' ' * indent + word
            line_len = indent + visual_width(word)
        else:
            result += (' ' if result else '') + word
            if from_center: res += ' ' + word
            line_len += visual_width(word) + (margin / 
                (2 if margin >= 2 else 1))
                
    if not from_center: return result
    return centered + align.center(res, l, h, lh)

def has_unicode(s: str) -> bool:
    strip_ansi(s)
    for ch in s:
        if isunicode(ch): return True
    return False

def isunicode(s: str) -> bool:
    strip_ansi(s)
    return ord(s) in [9, 10, 13, 27]

def preserve_codes(s: str) -> str:
    strip_ansi(s)
    codes = {
          "\n": "\\n",
          "\r": "\\r",
          "\t": "\\t",
        "\x1b": "\\x1b"
    }
        
    preserved = [ch for ch in s]
    for c, r in codes.items():
        for i, ch in enumerate(preserved):
            if ch == c: preserved[i] = r
                
    return "".join(preserved)

def label(iterable: list|tuple|dict, hue: str = "cyan") -> list:
    return [style_text(head, fg=hue) for head in 
            iterable]

def iter_print(text, times: int, end: str = "\n", 
               delay: int | float = 0):
    
    validate(
     [times, int, "positive integer", "eqless", 0],
     [end, str, "string"],
     [delay, [int, float], "natural number", "less", 0],
     err=__err__
    )
    
    for _ in range(times):
        time.sleep(delay)
        print(text, end=end, flush=True)

def pad_args(*args) -> list[str]:
    return [str(n).zfill(2) for n in args]
    
def __err__(cause, required: str):
    raise InputError(cause=cause, required=required)
 