from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_skills, job_description):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_skills, job_description])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

def rank_jobs(resume_skills, job_listings):
    ranked_jobs = []
    for job in job_listings:
        score = calculate_similarity(resume_skills, job["job_description"])
        ranked_jobs.append((job, score))
    return sorted(ranked_jobs, key=lambda x: x[1], reverse=True)