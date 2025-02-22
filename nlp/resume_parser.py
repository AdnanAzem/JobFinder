from transformers import pipeline
from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    # Check if the file is a PDF
    if not file_path.lower().endswith(".pdf"):
        raise ValueError("The file must be a PDF.")
    
    # Extract text from the PDF
    reader = PdfReader(file_path)
    text = "".join(page.extract_text() for page in reader.pages)
    return text

def extract_skills(text):
    classifier = pipeline("token-classification", model="dslim/bert-base-NER")
    entities = classifier(text)
    
    # Extract skills from MISC entities
    skills = [entity["word"] for entity in entities if entity["entity"] in ["MISC", "B-MISC", "I-MISC"]]
    
    # Merge subwords
    merged_skills = []
    current_skill = ""
    for skill in skills:
        if skill.startswith("##"):
            current_skill += skill[2:]  # Merge subwords
        else:
            if current_skill:
                merged_skills.append(current_skill)
            current_skill = skill
    if current_skill:
        merged_skills.append(current_skill)
    
    # Normalize skills
    skill_mapping = {
        "js": "JavaScript",
        "reactjs": "React",
        "html5": "HTML",
        "css3": "CSS",
        "cplusplus": "C++",
        "csharp": "C#",
        "ml": "Machine Learning",
        "dl": "Deep Learning",
        "ai": "Artificial Intelligence",
        "aws cloud": "AWS",
        "azure cloud": "Azure"
    }
    normalized_skills = []
    for skill in merged_skills:
        skill_lower = skill.lower()
        if skill_lower in skill_mapping:
            normalized_skills.append(skill_mapping[skill_lower])
        else:
            normalized_skills.append(skill)
    
    # Filter valid skills
    valid_skills = [
        "Python", "Java", "JavaScript", "SQL", "Machine Learning", "Data Analysis",
        "React", "HTML", "CSS", "C++", "C#", "Git", "Docker", "Linux", "AWS",
        "Azure", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn", "Flutter", "Dart"
    ]
    filtered_skills = list({skill for skill in normalized_skills if skill in valid_skills})
    
    print("Extracted Skills:", filtered_skills)  # Debug: Print extracted skills
    return filtered_skills

def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)
    skills = extract_skills(text)
    return {"content": text, "skills": skills}