from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database.models import session, Match

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_similarity(resume_skills, job_description):
    # Encode the resume skills and job description
    skills_embedding = model.encode(resume_skills, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    
    # Calculate cosine similarity
    similarity = util.cos_sim(skills_embedding, job_embedding)
    return similarity.item()

def rank_jobs(resume_skills, job_listings):
    ranked_jobs = []
    for job in job_listings:
        score = calculate_similarity(resume_skills, job["job_description"])
        ranked_jobs.append((job, score))
    return sorted(ranked_jobs, key=lambda x: x[1], reverse=True)
