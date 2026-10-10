"""Natural Textbook Display visual representation engine for 2D mathematical structures."""
import html
import re

def render_natural_math(expr_text: str, cursor_pos: int, is_natural: bool = True, cursor_char: str = "│") -> str:
    """Formats an expression string with cursor for LCD display.
    In natural mode (MthIO), powers, roots, and fractions use rich HTML formatting."""
    # Insert cursor character
    pos = max(0, min(len(expr_text), cursor_pos))
    text_with_cursor = expr_text[:pos] + cursor_char + expr_text[pos:]

    if not is_natural:
        return html.escape(text_with_cursor)

    # Convert natural mathematical conventions to rich text
    s = html.escape(text_with_cursor)

    # Format mixed fraction text to Casio ⌟ symbol
    s = s.replace("mixed/", "⌟")

    # Format square and cube symbols
    s = s.replace("²", "<sup>2</sup>")
    s = s.replace("³", "<sup>3</sup>")
    s = s.replace("⁻¹", "<sup>-1</sup>")

    # Format powers ^(...) or ^\d+
    s = re.sub(r'\^(\d+)', r'<sup>\1</sup>', s)

    # Format radicals: √(radicand)
    s = re.sub(r'√\(([^)]+)\)', r'<span style="border-top:1px solid #17271f;">&radic; \1</span>', s)

    return s


def render_natural_result(result_text: str, is_natural: bool = True) -> str:
    """Formats an evaluation result string into 2D textbook format if in MthIO mode."""
    if not result_text:
        return ""
    if not is_natural:
        return html.escape(result_text)

    # 1. Mixed fraction: W N/D e.g. "2 1/3" or "-2 1/3" or "2⌟1⌟3"
    mixed_match = re.match(r'^(-?\d+)[\s⌟]+(\d+)[/⌟](\d+)$', result_text.strip())
    if mixed_match:
        whole, num, den = mixed_match.groups()
        return (
            f'<span style="font-size:20px; font-weight:bold; color:#141f16;">{whole}&nbsp;</span>'
            f'<table style="display:inline-table; vertical-align:middle; text-align:center; border-collapse:collapse; margin:0; padding:0;">'
            f'<tr><td style="border-bottom:2px solid #141f16; padding:0 3px; font-size:15px; font-weight:bold; color:#141f16; text-align:center;">{num}</td></tr>'
            f'<tr><td style="padding:0 3px; font-size:15px; font-weight:bold; color:#141f16; text-align:center;">{den}</td></tr>'
            f'</table>'
        )

    # 2. Simple fraction: N/D e.g. "109/9000", "-5/6" or "1⌟3"
    frac_match = re.match(r'^(-?\d+)[/⌟](\d+)$', result_text.strip())
    if frac_match:
        num, den = frac_match.groups()
        return (
            f'<table style="display:inline-table; vertical-align:middle; text-align:center; border-collapse:collapse; margin:0; padding:0;">'
            f'<tr><td style="border-bottom:2px solid #141f16; padding:0 4px; font-size:16px; font-weight:bold; color:#141f16; text-align:center;">{num}</td></tr>'
            f'<tr><td style="padding:0 4px; font-size:16px; font-weight:bold; color:#141f16; text-align:center;">{den}</td></tr>'
            f'</table>'
        )

    return html.escape(result_text)

