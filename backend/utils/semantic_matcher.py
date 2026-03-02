from sentence_transformers import SentenceTransformer, util
import torch

# Load the model (this might take a few seconds the first time)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_similarity(resume_text, jd_text):
    """
    Calculates the cosine similarity between resume and job description.
    Returns a float between 0 and 1.
    """
    try:
        # Encode the texts into vectors
        embeddings = model.encode([resume_text, jd_text], convert_to_tensor=True)
        
        # Compute cosine similarity
        cosine_score = util.pytorch_cos_sim(embeddings[0], embeddings[1])
        
        # Return as a simple float
        return float(cosine_score.item())
    except Exception as e:
        print(f"Error in semantic matching: {e}")
        return 0.0