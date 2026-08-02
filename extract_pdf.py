import sys
try:
    import PyPDF2
    
    pdf_path = r'c:\farmer_market\Doc\SAMPLE MCA MINI PROJECT REPORT FORMAT.pdf'
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        print(f"Total pages: {len(pdf_reader.pages)}\n")
        print("="*80)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            print(f"\n--- Page {page_num + 1} ---\n")
            print(text)
            print("\n" + "="*80)
            
except ImportError:
    print("PyPDF2 not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    print("Please run the script again.")
except Exception as e:
    print(f"Error: {e}")
