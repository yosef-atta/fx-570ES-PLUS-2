"""Natural Textbook Display visual representation engine for 2D mathematical structures."""
import html
import re

def render_natural_math(expr_text: str, cursor_pos: int, is_natural: bool = True) -> str:
    """Formats an expression string with cursor for LCD display.
    In natural mode (MthIO), powers, roots, and fractions use rich HTML formatting."""
    # Insert cursor character
    pos = max(0, min(len(expr_text), cursor_pos))
    text_with_cursor = expr_text[:pos] + "│" + expr_text[pos:]

    if not is_natural:
        return html.escape(text_with_cursor)

    # Convert natural mathematical conventions to rich text
    # 1. Superscript powers like ^2, ^3, ^(x)
    s = html.escape(text_with_cursor)

    # Format square and cube symbols
    s = s.replace("²", "<sup>2</sup>")
    s = s.replace("³", "<sup>3</sup>")
    s = s.replace("⁻¹", "<sup>-1</sup>")

    # Format powers ^(...) or ^\d+
    s = re.sub(r'\^(\d+)', r'<sup>\1</sup>', s)

    # Format radicals: √(radicand)
    s = re.sub(r'√\(([^)]+)\)', r'<span style="border-top:1px solid #17271f;">&radic; \1</span>', s)

    return s
