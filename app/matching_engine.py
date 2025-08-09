import re
from typing import Dict, List, Tuple, Optional
from .embedding_system import EmbeddingSystem

class MatchingEngine:
    def __init__(self):
        self.embedding_system = EmbeddingSystem()
        self.processed_resumes = {}
    
    def add_resume(self, resume_id: str, resume_text: str, sections: Dict[str, str] = None, entities: Dict = None):
        self.processed_resumes[resume_id] = {
            'text': resume_text,
            'sections': sections or {},
            'entities': entities or {}
        }
        self.embedding_system.store_resume_embedding(resume_id, resume_text, sections)
    
    def match_job_to_resumes(self, job_description: str, top_k: int = 5, include_entities: bool = True) -> List[Dict]:
        if not self.processed_resumes:
            return []
        
        resume_texts = []
        resume_ids = []
        
        for resume_id, resume_data in self.processed_resumes.items():
            resume_texts.append(resume_data['text'])
            resume_ids.append(resume_id)
        
        top_matches = self.embedding_system.find_top_matches(job_description, resume_texts, top_k)
        
        results = []
        for idx, score in top_matches:
            resume_id = resume_ids[idx]
            resume_data = self.processed_resumes[resume_id]
            
            matched_terms = self._extract_matched_terms(job_description, resume_data['text'])
            
            result = {
                'resume_id': resume_id,
                'match_score': round(score * 100, 2),
                'raw_score': score,
                'text_length': len(resume_data['text']),
                'matched_terms': matched_terms,
                'sections': list(resume_data['sections'].keys()) if resume_data['sections'] else []
            }
            
            if include_entities and 'entities' in resume_data:
                result['entities'] = resume_data['entities']
            
            results.append(result)
        
        return results
    
    def match_single_resume(self, resume_id: str, job_description: str) -> Optional[Dict]:
        if resume_id not in self.processed_resumes:
            return None
        
        resume_data = self.processed_resumes[resume_id]
        match_result = self.embedding_system.match_resume_to_job(resume_id, job_description)
        
        if 'error' in match_result:
            return None
        
        matched_terms = self._extract_matched_terms(job_description, resume_data['text'])
        
        return {
            'resume_id': resume_id,
            'overall_score': round(match_result['overall_score'] * 100, 2),
            'raw_score': match_result['overall_score'],
            'section_scores': {k: round(v * 100, 2) for k, v in match_result['section_scores'].items()},
            'matched_terms': matched_terms,
            'text_length': len(resume_data['text']),
            'sections': list(resume_data['sections'].keys()) if resume_data['sections'] else []
        }
    
    def _extract_matched_terms(self, job_description: str, resume_text: str) -> List[str]:
        job_words = set(re.findall(r'\b\w+\b', job_description.lower()))
        resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
        
        common_words = job_words.intersection(resume_words)
        
        filtered_terms = []
        for word in common_words:
            if len(word) > 2 and word not in ['the', 'and', 'for', 'with', 'this', 'that', 'have', 'been', 'from', 'they', 'will', 'would', 'could', 'should']:
                filtered_terms.append(word)
        
        return sorted(filtered_terms)[:10]
    
    def get_resume_info(self, resume_id: str) -> Optional[Dict]:
        if resume_id not in self.processed_resumes:
            return None
        
        resume_data = self.processed_resumes[resume_id]
        return {
            'resume_id': resume_id,
            'text_length': len(resume_data['text']),
            'sections': list(resume_data['sections'].keys()) if resume_data['sections'] else []
        }
    
    def remove_resume(self, resume_id: str) -> bool:
        if resume_id in self.processed_resumes:
            del self.processed_resumes[resume_id]
            return True
        return False
    
    def clear_all(self):
        self.processed_resumes.clear()
        self.embedding_system.clear_cache()
    
    def get_stats(self) -> Dict:
        return {
            'total_resumes': len(self.processed_resumes),
            'embedding_cache_size': self.embedding_system.get_cache_stats()['embeddings_cache_size']
        } 