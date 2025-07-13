import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import PyPDF2
import re
import csv
import os
from pathlib import Path
import threading

class CVParser:
    def __init__(self, root):
        self.root = root
        self.root.title("CV Parser - Extract Information from PDF CVs")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        self.selected_files = []
        self.create_widgets()

    def create_widgets(self):
        # Main title
        title_label = tk.Label(
            self.root, 
            text="CV Parser", 
            font=("Arial", 24, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Description
        desc_label = tk.Label(
            self.root,
            text="Select PDF CV files to extract information (Name, Email, Phone, University, Grade)",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#34495e'
        )
        desc_label.pack(pady=10)
        
        # File selection frame
        file_frame = tk.Frame(self.root, bg='#f0f0f0')
        file_frame.pack(pady=20, padx=20, fill='x')
        
        # Select files button
        self.select_btn = tk.Button(
            file_frame,
            text="Select PDF Files",
            command=self.select_files,
            font=("Arial", 12),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.select_btn.pack(side='left', padx=(0, 10))
        
        # Clear files button
        self.clear_btn = tk.Button(
            file_frame,
            text="Clear Selection",
            command=self.clear_files,
            font=("Arial", 12),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.clear_btn.pack(side='left')
        
        # Selected files display
        files_frame = tk.Frame(self.root, bg='#f0f0f0')
        files_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(
            files_frame,
            text="Selected Files:",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor='w')
        
        self.files_listbox = tk.Listbox(
            files_frame,
            height=8,
            font=("Arial", 10),
            bg='white',
            relief='solid',
            borderwidth=1
        )
        self.files_listbox.pack(fill='both', expand=True, pady=(5, 0))
        
        scrollbar = tk.Scrollbar(files_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        self.files_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.files_listbox.yview)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            orient='horizontal',
            length=400,
            mode='determinate'
        )
        self.progress.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to parse CVs",
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#27ae60'
        )
        self.status_label.pack(pady=5)
        
        # Parse button
        self.parse_btn = tk.Button(
            self.root,
            text="Parse CVs and Export to CSV",
            command=self.parse_cvs,
            font=("Arial", 14, "bold"),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=30,
            pady=15,
            state='disabled'
        )
        self.parse_btn.pack(pady=20)
        
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF CV files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if files:
            self.selected_files = list(files)
            self.update_files_display()
            self.parse_btn.config(state='normal')
            self.status_label.config(text=f"Selected {len(self.selected_files)} file(s)")
            
    def clear_files(self):
        self.selected_files = []
        self.files_listbox.delete(0, tk.END)
        self.parse_btn.config(state='disabled')
        self.status_label.config(text="Ready to parse CVs")
        
    def update_files_display(self):
        self.files_listbox.delete(0, tk.END)
        for file in self.selected_files:
            filename = os.path.basename(file)
            self.files_listbox.insert(tk.END, filename)
            
    def extract_text_from_pdf(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""
            
    def clean_phone_number(self, phone):
        if not phone:
            return phone
        # Remove extra whitespace, dashes, parentheses, and normalize
        phone = re.sub(r'[\s\-\(\)]+', '', phone.strip())
        # Standardize +234 prefix for Nigerian numbers
        phone = re.sub(r'^0([7-9][0-1][0-9]{8})$', r'+234\1', phone)
        phone = re.sub(r'^\+?234\s*\+?234', '+234', phone)
        return phone
    
    def clean_university_name(self, university):
        if not university:
            return university
        university = re.sub(r'\s+', ' ', university.strip())
        # Remove dates (e.g., 2023-2024, Nov 2023)
        university = re.sub(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b', '', university)
        university = re.sub(r'\b\d{4}\s*-\s*\d{4}\b', '', university)
        university = re.sub(r'\b\d{4}\s*-\s*Present\b', '', university)
        # Remove specific locations only if they follow a comma
        university = re.sub(r',\s*(?:Lagos|Port Harcourt|Ondo|Enugu|Nigeria)\b', '', university)
        return university.strip()
    
    def clean_grade(self, grade):
        if not grade:
            return grade
        grade = re.sub(r'\s+', ' ', grade.strip())
        # Standardize grade formats
        grade = re.sub(r'Second\s*Class\s*Upper\s*(Division|Honours)?', 'Second Class Upper Division', grade, flags=re.IGNORECASE)
        grade = re.sub(r'Second\s*Class\s*Lower\s*(Division|Honours)?', 'Second Class Lower Division', grade, flags=re.IGNORECASE)
        grade = re.sub(r'First\s*Class\s*(Division|Honours)?', 'First Class', grade, flags=re.IGNORECASE)
        grade = re.sub(r'Third\s*Class\s*(Division|Honours)?', 'Third Class', grade, flags=re.IGNORECASE)
        return grade
    
    def clean_name(self, name):
        if not name:
            return name
        name = re.sub(r'\s+', ' ', name.strip())
        name = re.sub(r'\b(?:CV|Resume|Curriculum|Vitae)\b', '', name, flags=re.IGNORECASE)
        # Capitalize each word properly
        name_parts = name.split()
        cleaned_parts = [part[0].upper() + part[1:].lower() for part in name_parts if part]
        return ' '.join(cleaned_parts)
    
    def extract_information(self, text):
        info = {
            'Name': '',
            'Email': '',
            'Phone': '',
            'University': '',
            'Grade': ''
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            info['Email'] = email_match.group()
            
        # Extract phone number
        phone_patterns = [
            r'\+?234\s*[0-9]{3}\s*[0-9]{3}\s*[0-9]{4}',  # +234 XXX XXX XXXX
            r'\+?234\s*[0-9]{10}',  # +234XXXXXXXXXX
            r'\+?234\s*\(?0\)?[0-9]{3}\s*[0-9]{3}\s*[0-9]{4}',  # +234(0)XXX XXX XXXX
            r'0[7-9][0-1][0-9]{8}',  # 0XXXXXXXXXX
            r'\+?[0-9]{1,4}[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',  # International with dashes/parentheses
            r'\+?[0-9]{10,15}',  # Long international numbers
        ]
        for pattern in phone_patterns:
            phone_matches = re.findall(pattern, text)
            if phone_matches:
                info['Phone'] = self.clean_phone_number(max(phone_matches, key=len))
                break
                
        # Extract university
        university_keywords = [
            'university', 'college', 'institute', 'school', 'academy', 'polytechnic', 'law school'
        ]
        lines = text.split('\n')
        university_candidates = []
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            for keyword in university_keywords:
                if keyword in line_lower:
                    university_name = line.strip()
                    # Combine with previous/next lines if they seem part of the name
                    start_idx = max(0, i-1)
                    end_idx = min(len(lines), i+2)
                    for j in range(start_idx, end_idx):
                        if j != i and lines[j].strip():
                            if not any(word in lines[j].lower() for word in ['email', 'phone', 'address', 'cv', 'resume', 'curriculum', 'vitae', 'grade', 'gpa']):
                                university_name += ' ' + lines[j].strip()
                    university_name = re.sub(r'\s+', ' ', university_name).strip()
                    if len(university_name) > 5 and len(university_name) < 200:
                        university_candidates.append(university_name)
        
        if university_candidates:
            info['University'] = self.clean_university_name(max(university_candidates, key=len))
                
        # Extract grade
        grade_patterns = [
            r'Second\s*Class\s*Upper\s*(Division|Honours)?',
            r'Second\s*Class\s*Lower\s*(Division|Honours)?',
            r'First\s*Class\s*(Division|Honours)?',
            r'Third\s*Class\s*(Division|Honours)?',
            r'Pass\s*Class',
            r'Distinction',
            r'Merit',
            r'Credit',
            r'GPA[:\s]*([0-9]\.[0-9]{1,2})',
            r'([0-9]\.[0-9]{1,2})/[0-9]\.[0-9]{1,2}',
            r'([0-9]\.[0-9]{1,2})\s*GPA',
            r'([0-9]{1,2})%',
            r'([A-F][+-]?)\s*Grade',
            r'([A-F][+-]?)\s*\([0-9]\.[0-9]{1,2}\)',
        ]
        for pattern in grade_patterns:
            grade_matches = re.findall(pattern, text, re.IGNORECASE)
            if grade_matches:
                if isinstance(grade_matches[0], tuple):
                    info['Grade'] = self.clean_grade(grade_matches[0][0])
                else:
                    info['Grade'] = self.clean_grade(grade_matches[0])
                break
                
        # Extract name
        name_patterns = [
            r'^([A-Z\s]+)$',  # All-caps names in first lines
            r'Name[:\s]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\s*(?:CV|Resume|Curriculum\s*Vitae)',
            r'^([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){1,3})$',  # Mixed case names
        ]
        exclude_words = ['cv', 'resume', 'curriculum', 'vitae', 'email', 'phone', 'address', 
                        'university', 'college', 'institute', 'school', 'academy', 'polytechnic',
                        'law', 'second', 'first', 'third', 'class', 'upper', 'lower', 'nigeria']
        
        for i, line in enumerate(lines[:10]):
            line = line.strip()
            if len(line) > 0:
                for pattern in name_patterns:
                    name_match = re.match(pattern, line)
                    if name_match:
                        potential_name = name_match.group(1)
                        if not any(word in potential_name.lower() for word in exclude_words):
                            info['Name'] = self.clean_name(potential_name)
                            break
                if info['Name']:
                    break
        
        if not info['Name']:
            for pattern in name_patterns[1:]:
                name_match = re.search(pattern, text)
                if name_match:
                    potential_name = name_match.group(1)
                    if not any(word in potential_name.lower() for word in exclude_words):
                        info['Name'] = self.clean_name(potential_name)
                        break
        
        return info
        
    def parse_cvs(self):
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select PDF files first!")
            return
        self.parse_btn.config(state='disabled')
        self.select_btn.config(state='disabled')
        self.clear_btn.config(state='disabled')
        thread = threading.Thread(target=self.process_cvs)
        thread.daemon = True
        thread.start()
        
    def process_cvs(self):
        try:
            all_data = []
            total_files = len(self.selected_files)
            
            for i, pdf_path in enumerate(self.selected_files):
                progress = (i / total_files) * 100
                self.root.after(0, lambda p=progress: self.progress.config(value=p))
                self.root.after(0, lambda: self.status_label.config(text=f"Processing {i+1}/{total_files}: {os.path.basename(pdf_path)}"))
                text = self.extract_text_from_pdf(pdf_path)
                if text:
                    info = self.extract_information(text)
                    info['Filename'] = os.path.basename(pdf_path)
                    all_data.append(info)
            self.export_to_csv(all_data)
            self.root.after(0, lambda: self.progress.config(value=100))
            self.root.after(0, lambda: self.status_label.config(text=f"Successfully processed {len(all_data)} CV(s)"))
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Successfully processed {len(all_data)} CV(s)\nResults saved to 'cv_results.csv'"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
            self.root.after(0, lambda: self.status_label.config(text="Error occurred during processing"))
        finally:
            self.root.after(0, lambda: self.parse_btn.config(state='normal'))
            self.root.after(0, lambda: self.select_btn.config(state='normal'))
            self.root.after(0, lambda: self.clear_btn.config(state='normal'))
            
    def export_to_csv(self, data):
        if not data:
            return
        csv_file = 'cv_results.csv'
        fieldnames = ['Filename', 'Name', 'Email', 'Phone', 'University', 'Grade']
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

def main():
    try:
        import PyPDF2
    except ImportError:
        messagebox.showerror("Missing Package", 
                           "PyPDF2 is not installed. Please install it using:\npip install PyPDF2")
        return
    root = tk.Tk()
    app = CVParser(root)
    root.mainloop()

if __name__ == "__main__":
    main()
