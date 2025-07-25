# app/heading_detector.py

def detect_headings(spans, stats):
    """
    Identifies Title, H1, H2, and H3 headings from a list of text spans
    using a heuristic-based approach.
    
    Returns:
        A list of detected headings, sorted by appearance.
    """
    headings = []
    
    body_text_size = stats["most_common_size"]
    
    # 1. First pass: Identify potential headings
    potential_headings = []
    for span in spans:
        is_bold = "bold" in span["font_name"].lower()
        is_larger_than_body = span["font_size"] > body_text_size
        
        # A heading is likely larger than body text, and often bold.
        if is_larger_than_body or (is_bold and span["font_size"] >= body_text_size):
            # A simple check for all-caps can also be a hint
            is_all_caps = span["text"].isupper() and len(span["text"]) > 1
            
            # Score the span based on how "heading-like" it is
            score = 0
            if is_larger_than_body:
                score += (span["font_size"] - body_text_size)
            if is_bold:
                score += 2 # Give a bonus for being bold
            if is_all_caps:
                score += 1

            if score > 0:
                potential_headings.append({**span, "score": score})

    if not potential_headings:
        return []

    # 2. Identify unique heading styles (font_size, font_name)
    heading_styles = sorted(
        list(set((h["font_size"], h["font_name"]) for h in potential_headings)),
        key=lambda x: x[0],
        reverse=True
    )

    # 3. Map styles to heading levels (H1, H2, etc.)
    # The largest font size is H1, the next is H2, and so on.
    style_to_level = {style: f"H{i+1}" for i, style in enumerate(heading_styles[:3])} # Limit to H1, H2, H3

    # 4. Final pass: Assign levels
    for heading in potential_headings:
        style = (heading["font_size"], heading["font_name"])
        if style in style_to_level:
            headings.append({
                "level": style_to_level[style],
                "text": heading["text"],
                "page_num": heading["page_num"]
            })
            
    # 5. Identify the document Title
    # The title is usually the very first major heading on the first page.
    if headings and headings[0]["page_num"] == 1:
        headings[0]["level"] = "Title"

    return headings