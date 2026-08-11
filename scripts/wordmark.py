# Constructed geometric alphabet — chamfered, monoline. Only the glyphs we need.
# Each letter drawn in a 56x76 box; list of polylines (open) per glyph.
G = {
 'S': [[(50,6),(14,6),(6,15),(6,29),(14,38),(42,38),(50,47),(50,61),(42,70),(6,70)]],
 'O': [[(14,6),(42,6),(50,15),(50,61),(42,70),(14,70),(6,61),(6,15),(14,6)]],
 'U': [[(6,6),(6,61),(14,70),(42,70),(50,61),(50,6)]],
 'M': [[(6,70),(6,6),(28,33),(50,6),(50,70)]],
 'I': [[(15,6),(41,6)],[(28,6),(28,70)],[(15,70),(41,70)]],
 'K': [[(6,6),(6,70)],[(49,6),(10,38),(49,70)]],
 'D': [[(6,6),(35,6),(50,21),(50,55),(35,70),(6,70),(6,6)]],
 'E': [[(50,6),(6,6),(6,70),(50,70)],[(6,38),(37,38)]],
 'Y': [[(6,6),(28,35),(50,6)],[(28,35),(28,70)]],
 ' ': [],
}
ADV = {'I': 40, ' ': 30}

def wordmark(text, x0, y0, scale=1.0, tracking=16):
    """Return (svg_paths_string, total_width). y0 = top of cap height."""
    parts, pen = [], 0.0
    for ch in text.upper():
        w = ADV.get(ch, 56)
        for poly in G.get(ch, []):
            pts = " ".join(f"{x0 + (pen + px)*scale:.1f},{y0 + py*scale:.1f}" for px,py in poly)
            parts.append(f'<polyline points="{pts}"/>')
        pen += w + tracking
    return "".join(parts), (pen - tracking) * scale
