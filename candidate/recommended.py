from django.contrib.auth.models import User
from hr.models import JobPost
from candidate.models import CandidateProfile, candidateApplication
from sklearn.feature_extraction.text import CountVectorizer  #count vector for actual document vector
from sklearn.metrics.pairwise import cosine_similarity     # A V . B V / |A| . |B|
# from __future__ import annotations
from typing import List, Tuple



try:
    from nltk.corpus import stopwords as nltk_stopwords  # use NLTK for stopwords 

    NLTK_STOP_WORDS = set(nltk_stopwords.words("english"))
except Exception:
    NLTK_STOP_WORDS = None


MIN_MATCH_SCORE = 0.25 # Minimum similarity score required to show a job in recommendations


def build_stopword_list_for_vectorizer():
    if NLTK_STOP_WORDS is not None:
        return list(NLTK_STOP_WORDS)  # Convert set to list for CountVectorizer
    return "english"


#weight priority distribute
def _build_candidate_text(profile: CandidateProfile) -> str:
    segments: List[str] = [] #creating list

    # High priority: Job Preferences (weight 3)
    if profile.job_preference_title:
        segments.append((profile.job_preference_title + " ") * 3)
    if profile.job_interest:
        segments.append((profile.job_interest + " ") * 3)
    if profile.preferred_industry:
        segments.append((profile.preferred_industry + " ") * 3)
    if profile.work_experience_description:
        segments.append((profile.work_experience_description + " ") * 3)

    # High priority: Education (weight 2)
    if profile.education_level:
        segments.append((str(profile.education_level) + " ") * 2)
    if profile.course_or_program:
        segments.append((profile.course_or_program + " ") * 2)

    # High priority: Skills & Career Summary (weight 2)
    if profile.skills:
        segments.append((profile.skills + " ") * 2)
    if profile.career_summary:
        segments.append((profile.career_summary + " ") * 2)

    # Low priority: still included but with normal weight
    if profile.preferred_job_level:
        segments.append(str(profile.preferred_job_level))
    if profile.preferred_job_type:
        segments.append(str(profile.preferred_job_type))
    if profile.work_experience is not None:
        segments.append(f"{profile.work_experience} years experience")

    return " ".join(segments).strip()



#Convert job form data into → text using _build_job_text()  (Create Dictionary)
def _build_job_text(job: JobPost) -> str:  
    parts: List[str] = []

    # Give more weight to the job title and company name
    if job.title:
        parts.append((job.title + " ") * 3)
    if job.CompanyName:
        parts.append((job.CompanyName + " ") * 2)
    if job.address:
        parts.append(job.address)

    # Required skills and metadata
    if job.required_skills:
        parts.append((job.required_skills + " ") * 2)
    if job.required_experience:
        parts.append(str(job.get_required_experience_display()))
    if job.required_education:
        parts.append(str(job.get_required_education_display()))

    if job.employment_type:
        parts.append(str(job.employment_type))
    if job.work_mode:
        parts.append(str(job.work_mode))

    return " ".join(parts).strip()



#convert it into multiple documents ( corpus )
def build_corpus(profile: CandidateProfile, jobs: List[JobPost]) -> List[str]:
    candidate_text = _build_candidate_text(profile)
    job_texts = []

    for job in jobs:
        job_text = _build_job_text(job)
        job_texts.append(job_text)

    corpus = [candidate_text] + job_texts
    return corpus


#When sorting, use the score value for ranking jobs. 
def sort_by_score(item: Tuple[JobPost, float]) -> float:
    job, score = item
    return score




def recommend_jobs_for_user(user: User, top_n: int = 20) -> List[Tuple[JobPost, float]]:#float is similarity_score
    
    # 1️) Get candidate profile
    try:
        profile = CandidateProfile.objects.get(user=user)
    except CandidateProfile.DoesNotExist:
        return []   # If no profile, no recommendation



    # 2️) Get jobs already applied by user (don’t recommend jobs the user already applied for)
    applied_job_ids = list(
        candidateApplication.objects
        .filter(user=user)
        .values_list("job_id", flat=True)
    )



    # 3️) Get jobs that user has NOT applied to (Retrieves all JobPost entries that the user hasn’t applied to yet.)
    available_jobs = list(
        JobPost.objects.exclude(id__in=applied_job_ids)
    )
    if not available_jobs:
        return []   # No jobs left



    corpus = build_corpus(profile, available_jobs)   #Build text corpus/collection (Corpus is essentially a list of strings, ready for vectorization.)
    stop_words = build_stopword_list_for_vectorizer()  # Build stopwords list


    # 64)  Convert text into Bag-of-Words vectors
    vectorizer = CountVectorizer(stop_words=stop_words)
    matrix = vectorizer.fit_transform(corpus).toarray()


   
    candidate_vector = matrix[0].reshape(1, -1)  # First row = candidate vector
    job_vectors = matrix[1:] # Remaining rows = job vectors



    # 5) Calculate cosine similarity for each job
    scored_jobs: List[Tuple[JobPost, float]] = []

    for index, job in enumerate(available_jobs):
        job_vector = job_vectors[index].reshape(1, -1)

        similarity_score = float(
            cosine_similarity(candidate_vector, job_vector)[0][0]
        )

        scored_jobs.append((job, similarity_score))



    # 6) Filter jobs based on minimum match score
    filtered_jobs = [
        (job, score)
        for job, score in scored_jobs
        if score >= MIN_MATCH_SCORE
    ]

    if not filtered_jobs:
        return []



    # 7) Sort jobs by score (highest first)
    filtered_jobs.sort(key=lambda x: x[1], reverse=True)


    # 8) Return top N jobs
    return filtered_jobs[:top_n]