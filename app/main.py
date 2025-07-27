import os
# Import the corrected functions from your other files
from pdf_parser import parse_pdf
from heading_detector import analyze_and_find_headings
from output_generator import save_to_json

def process_all_pdfs():
    """
    Processes all PDF files in the input directory and saves the structured JSON output.
    """
    # These folder paths are fixed because they are defined by the Docker environment
    input_dir = "/app/input"
    output_dir = "/app/output"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Loop through every file in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            print(f"Processing {filename}...")
            pdf_path = os.path.join(input_dir, filename)
            
            # Call the functions in the correct order
            
            # a) Parse the PDF to get all text spans
            all_spans = parse_pdf(pdf_path)
            
            # b) Analyze the spans to get the final data object
            result = analyze_and_find_headings(all_spans)
            
            # c) Save the final data object to a JSON file
            output_filename = f"{os.path.splitext(filename)[0]}.json"
            output_path = os.path.join(output_dir, output_filename)
            save_to_json(result, output_path)

if __name__ == '__main__':
    process_all_pdfs()