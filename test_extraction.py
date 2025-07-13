#!/usr/bin/env python3
"""
Test script to verify the improved CV extraction logic
"""

import re

def clean_phone_number(phone):
    """Clean and format phone number"""
    if not phone:
        return phone
    
    # Remove extra whitespace and normalize
    phone = re.sub(r'\s+', ' ', phone.strip())
    
    # Remove common prefixes that might be duplicated
    phone = re.sub(r'^\+?234\s*\+?234', '+234', phone)
    
    return phone

def clean_university_name(university):
    """Clean and format university name"""
    if not university:
        return university
    
    # Remove extra whitespace and normalize
    university = re.sub(r'\s+', ' ', university.strip())
    
    # Remove common date patterns that might be mixed in
    university = re.sub(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b', '', university)
    university = re.sub(r'\b\d{4}\s*-\s*\d{4}\b', '', university)
    university = re.sub(r'\b\d{4}\s*-\s*Present\b', '', university)
    
    # Remove location patterns that might be mixed in
    university = re.sub(r',\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*$', '', university)
    
    return university.strip()

def clean_grade(grade):
    """Clean and format grade information"""
    if not grade:
        return grade
    
    # Remove extra whitespace and normalize
    grade = re.sub(r'\s+', ' ', grade.strip())
    
    # Standardize common grade formats
    grade = re.sub(r'Second\s*Class\s*Upper', 'Second Class Upper', grade, flags=re.IGNORECASE)
    grade = re.sub(r'Second\s*Class\s*Lower', 'Second Class Lower', grade, flags=re.IGNORECASE)
    grade = re.sub(r'First\s*Class', 'First Class', grade, flags=re.IGNORECASE)
    grade = re.sub(r'Third\s*Class', 'Third Class', grade, flags=re.IGNORECASE)
    
    return grade

def clean_name(name):
    """Clean and format name"""
    if not name:
        return name
    
    # Remove extra whitespace and normalize
    name = re.sub(r'\s+', ' ', name.strip())
    
    # Remove common suffixes and prefixes that might be mixed in
    name = re.sub(r'\b(?:CV|Resume|Curriculum|Vitae)\b', '', name, flags=re.IGNORECASE)
    
    # Ensure proper capitalization
    name_parts = name.split()
    cleaned_parts = []
    for part in name_parts:
        if len(part) > 0:
            # Capitalize first letter, lowercase the rest
            cleaned_parts.append(part[0].upper() + part[1:].lower())
    
    return ' '.join(cleaned_parts)

def test_extraction():
    """Test the improved extraction logic with sample data"""
    
    # Test phone number cleaning
    print("Testing phone number cleaning:")
    test_phones = [
        "+234 813 228 7745",
        "+2348132287745",
        "+234 +234 813 228 7745",
        "8132287745",
        "+234 814 4642"
    ]
    
    for phone in test_phones:
        cleaned = clean_phone_number(phone)
        print(f"  {phone} -> {cleaned}")
    
    print("\nTesting university name cleaning:")
    test_universities = [
        "Nigerian Law School, Abuja Campus, Abuja",
        "Nov. 2023  Nigerian Law School    Port Harcourt , Nigeria.",
        "University of Lagos, Lagos, Nigeria",
        "Harvard University 2018-2022"
    ]
    
    for university in test_universities:
        cleaned = clean_university_name(university)
        print(f"  {university} -> {cleaned}")
    
    print("\nTesting grade cleaning:")
    test_grades = [
        "Second Class Upper",
        "Second Class Lower",
        "First Class Honours",
        "3.5 GPA",
        "85%"
    ]
    
    for grade in test_grades:
        cleaned = clean_grade(grade)
        print(f"  {grade} -> {cleaned}")
    
    print("\nTesting name cleaning:")
    test_names = [
        "ADESOLA OMOTEBIMI DARAMOLA",
        "Faith Ekowo",
        "John Doe CV",
        "MARY JANE SMITH"
    ]
    
    for name in test_names:
        cleaned = clean_name(name)
        print(f"  {name} -> {cleaned}")

if __name__ == "__main__":
    test_extraction() 