# app/pdf_parser.py
import fitz  # PyMuPDF
import collections

def parse_pdf_for_text_properties(pdf_path):
    """
    Opens a PDF and extracts text blocks with their properties.
    
    Returns:
        A tuple containing:
        - A list of all text spans (dictionaries with text, font_size, font_name, bbox, page_num).
        - A dictionary with document-level statistics (most common font size and name).
    """
    doc = fitz.open(pdf_path)
    all_spans = []
    font_sizes = collections.Counter()
    font_names = collections.Counter()
    
    for page_num, page in enumerate(doc):
        # Using get_text("dict") gives us structured data
        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_DEFAULT)["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        # Collect properties for each text span
                        span_info = {
                            "text": span["text"].strip(),
                            "font_size": round(span["size"]),
                            "font_name": span["font"],
                            "bbox": span["bbox"], # (x0, y0, x1, y1)
                            "page_num": page_num + 1
                        }
                        if span_info["text"]:
                            all_spans.append(span_info)
                            font_sizes[span_info["font_size"]] += 1
                            font_names[span_info["font_name"]] += 1

    doc.close()

    # Calculate statistics
    stats = {
        "most_common_size": font_sizes.most_common(1)[0][0] if font_sizes else 12,
        "most_common_font": font_names.most_common(1)[0][0] if font_names else "Helvetica"
    }

    return all_spans, stats