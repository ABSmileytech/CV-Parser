# CV Parser Application

A simple and user-friendly CV Parser that extracts information from PDF CV files and exports the results to a CSV file.

## Features

- ✅ Parse multiple PDF CV files at once
- ✅ Extract key information: Name, Email, Phone, University, Grade
- ✅ User-friendly GUI interface
- ✅ Export results to CSV file
- ✅ Works on Windows
- ✅ Progress tracking
- ✅ Error handling

## What You Need to Install

### 1. Python
First, you need to install Python on your computer:
- Go to [python.org](https://www.python.org/downloads/)
- Download the latest version for Windows
- During installation, make sure to check "Add Python to PATH"

### 2. Required Python Packages
After installing Python, you need to install the required package. Open Command Prompt or PowerShell and run:

```bash
pip install PyPDF2==3.0.1
```

## How to Use the Application

### Step 1: Run the Application
1. Open Command Prompt or PowerShell
2. Navigate to the cv_parser folder:
   ```bash
   cd path\to\cv_parser
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Step 2: Using the GUI
1. **Select PDF Files**: Click the "Select PDF Files" button to choose your CV files
2. **Review Selection**: The selected files will appear in the list
3. **Parse CVs**: Click "Parse CVs and Export to CSV" to start processing
4. **Get Results**: The application will create a `cv_results.csv` file with all extracted information

### Step 3: View Results
- Open the generated `cv_results.csv` file with Excel or any spreadsheet application
- The file will contain columns: Filename, Name, Email, Phone, University, Grade

## What Information is Extracted

The application looks for and extracts:

1. **Name**: Full name of the person
2. **Email**: Email address (various formats)
3. **Phone**: Phone number (US and international formats)
4. **University**: Educational institution name
5. **Grade**: GPA, percentage, or letter grade

## Troubleshooting

### Common Issues:

1. **"PyPDF2 is not installed" error**
   - Solution: Run `pip install PyPDF2==3.0.1`

2. **"Python is not recognized" error**
   - Solution: Make sure Python is installed and added to PATH

3. **PDF files not being processed**
   - Make sure the PDF files are not password-protected
   - Ensure the PDF files contain text (not just images)

4. **No information extracted**
   - The CV format might be different from what the parser expects
   - Try with different CV formats

## File Structure

```
cv_parser/
├── main.py              # Main application file
├── requirements.txt     # Required packages
├── README.md           # This file
└── cv_results.csv      # Generated results (after running)
```

## Tips for Best Results

1. **PDF Quality**: Use PDF files that contain actual text (not scanned images)
2. **File Format**: Ensure CVs are in standard formats with clear sections
3. **Information Placement**: The parser works best when information is clearly labeled
4. **Multiple Files**: You can select multiple PDF files at once for batch processing

## How It Works (For Beginners)

The application uses:
- **tkinter**: Creates the graphical user interface
- **PyPDF2**: Reads and extracts text from PDF files
- **Regular Expressions (regex)**: Finds patterns like email addresses and phone numbers
- **CSV**: Saves the extracted data in a spreadsheet format

## Support

If you encounter any issues:
1. Make sure all requirements are installed
2. Check that your PDF files are not corrupted
3. Try with a simple PDF file first to test the application

## Example Output

The CSV file will look like this:

| Filename | Name | Email | Phone | University | Grade |
|----------|------|-------|-------|------------|-------|
| john_cv.pdf | John Smith | john@email.com | 555-123-4567 | University of Technology | 3.8 |
| jane_cv.pdf | Jane Doe | jane@email.com | 555-987-6543 | State College | A+ |

---

**Note**: This application is designed for educational and personal use. Always respect privacy and data protection laws when processing CVs. 