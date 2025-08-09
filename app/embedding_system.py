import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Optional
import torch

class EmbeddingSystem:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.embeddings_cache = {}
        self.text_cache = {}
    
    def get_embedding(self, text: str) -> np.ndarray:
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        embedding = self.model.encode(text)
        self.embeddings_cache[text] = embedding
        return embedding
    
    def get_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        embeddings = []
        for text in texts:
            embedding = self.get_embedding(text)
            embeddings.append(embedding)
        return np.array(embeddings)
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        embedding1 = self.get_embedding(text1)
        embedding2 = self.get_embedding(text2)
        
        similarity = cosine_similarity([embedding1], [embedding2])[0][0]
        return float(similarity)
    
    def calculate_similarity_batch(self, query_text: str, candidate_texts: List[str]) -> List[float]:
        query_embedding = self.get_embedding(query_text)
        candidate_embeddings = self.get_embeddings_batch(candidate_texts)
        
        similarities = cosine_similarity([query_embedding], candidate_embeddings)[0]
        return similarities.tolist()
    
    def store_resume_embedding(self, resume_id: str, text: str, sections: Dict[str, str] = None):
        full_embedding = self.get_embedding(text)
        
        self.text_cache[resume_id] = {
            'full_text': text,
            'full_embedding': full_embedding,
            'sections': sections or {}
        }
        
        if sections:
            section_embeddings = {}
            for section_name, section_text in sections.items():
                if section_text.strip():
                    section_embeddings[section_name] = self.get_embedding(section_text)
            
            self.text_cache[resume_id]['section_embeddings'] = section_embeddings
    
    def get_resume_embedding(self, resume_id: str) -> Optional[Dict]:
        return self.text_cache.get(resume_id)
    
    def match_resume_to_job(self, resume_id: str, job_description: str) -> Dict:
        if resume_id not in self.text_cache:
            return {'error': 'Resume not found'}
        
        resume_data = self.text_cache[resume_id]
        job_embedding = self.get_embedding(job_description)
        
        full_similarity = cosine_similarity([resume_data['full_embedding']], [job_embedding])[0][0]
        
        result = {
            'overall_score': float(full_similarity),
            'section_scores': {}
        }
        
        if 'section_embeddings' in resume_data:
            for section_name, section_embedding in resume_data['section_embeddings'].items():
                section_similarity = cosine_similarity([section_embedding], [job_embedding])[0][0]
                result['section_scores'][section_name] = float(section_similarity)
        
        return result
    
    def find_top_matches(self, query_text: str, candidate_texts: List[str], top_k: int = 5) -> List[Tuple[int, float]]:
        similarities = self.calculate_similarity_batch(query_text, candidate_texts)
        
        indexed_similarities = list(enumerate(similarities))
        indexed_similarities.sort(key=lambda x: x[1], reverse=True)
        
        return indexed_similarities[:top_k]
    
    def clear_cache(self):
        self.embeddings_cache.clear()
        self.text_cache.clear()
    
    def get_cache_stats(self) -> Dict:
        return {
            'embeddings_cache_size': len(self.embeddings_cache),
            'text_cache_size': len(self.text_cache)
        } 