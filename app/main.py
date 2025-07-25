# app/main.py
import os
from pdf_parser import parse_pdf_for_text_properties
from heading_detector import detect_headings
from output_generator import generate_json_output

# These paths are based on the Docker environment
INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def process_all_pdfs():
    """
    Processes all PDF files in the input directory and saves JSON output.
    """
    print("Starting Round 1A processing...")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
    
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        input_path = os.path.join(INPUT_DIR, pdf_file)
        
        # Step 1: Parse the PDF
        spans, stats = parse_pdf_for_text_properties(input_path)
        
        # Step 2: Detect headings from the parsed data
        headings = detect_headings(spans, stats)
        
        # Step 3: Generate the JSON output
        base_name = os.path.splitext(pdf_file)[0]
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.json")
        generate_json_output(headings, output_path)
        
        print(f"Successfully generated JSON for {pdf_file} at {output_path}")

if __name__ == "__main__":
    process_all_pdfs()