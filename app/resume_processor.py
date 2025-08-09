import os
import uuid
import time
from typing import Dict, List, Optional, Tuple
from .document_parser import DocumentParser
from .embedding_system import EmbeddingSystem
from .ner_extractor import NERExtractor

class ResumeProcessor:
    def __init__(self):
        self.parser = DocumentParser()
        self.embedding_system = EmbeddingSystem()
        self.ner_extractor = NERExtractor()
        self.processed_resumes = {}
    
    def process_resume_file(self, file_path: str) -> Dict:
        success, result = self.parser.parse_document(file_path)
        
        if not success:
            return {
                'success': False,
                'error': result,
                'resume_id': None
            }
        
        resume_id = str(uuid.uuid4())
        sections = self.parser.extract_sections(result)
        entities = self.ner_extractor.get_structured_entities(result)
        
        self.embedding_system.store_resume_embedding(resume_id, result, sections)
        
        self.processed_resumes[resume_id] = {
            'file_path': file_path,
            'text': result,
            'sections': sections,
            'entities': entities,
            'processed_at': os.path.getmtime(file_path)
        }
        
        return {
            'success': True,
            'resume_id': resume_id,
            'text_length': len(result),
            'sections': list(sections.keys()),
            'file_path': file_path
        }
    
    def process_resume_text(self, text: str, resume_id: str = None) -> Dict:
        if not resume_id:
            resume_id = str(uuid.uuid4())
        
        sections = self.parser.extract_sections(text)
        entities = self.ner_extractor.get_structured_entities(text)
        self.embedding_system.store_resume_embedding(resume_id, text, sections)
        
        self.processed_resumes[resume_id] = {
            'text': text,
            'sections': sections,
            'entities': entities,
            'processed_at': time.time()
        }
        
        return {
            'success': True,
            'resume_id': resume_id,
            'text_length': len(text),
            'sections': list(sections.keys())
        }
    
    def match_resume_to_job(self, resume_id: str, job_description: str) -> Dict:
        if resume_id not in self.processed_resumes:
            return {
                'success': False,
                'error': 'Resume not found'
            }
        
        match_result = self.embedding_system.match_resume_to_job(resume_id, job_description)
        
        if 'error' in match_result:
            return {
                'success': False,
                'error': match_result['error']
            }
        
        resume_data = self.processed_resumes[resume_id]
        
        return {
            'success': True,
            'resume_id': resume_id,
            'overall_score': match_result['overall_score'],
            'section_scores': match_result['section_scores'],
            'resume_info': {
                'text_length': len(resume_data['text']),
                'sections': list(resume_data['sections'].keys())
            }
        }
    
    def find_best_matches(self, job_description: str, top_k: int = 5) -> List[Dict]:
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
            
            results.append({
                'resume_id': resume_id,
                'score': score,
                'text_length': len(resume_data['text']),
                'sections': list(resume_data['sections'].keys())
            })
        
        return results
    
    def get_resume_info(self, resume_id: str) -> Optional[Dict]:
        if resume_id not in self.processed_resumes:
            return None
        
        resume_data = self.processed_resumes[resume_id]
        return {
            'resume_id': resume_id,
            'text_length': len(resume_data['text']),
            'sections': resume_data['sections'],
            'entities': resume_data.get('entities', {}),
            'processed_at': resume_data.get('processed_at', 0)
        }
    
    def get_all_resumes(self) -> List[Dict]:
        results = []
        for resume_id, resume_data in self.processed_resumes.items():
            results.append({
                'resume_id': resume_id,
                'text_length': len(resume_data['text']),
                'sections': list(resume_data['sections'].keys()),
                'entities': resume_data.get('entities', {}),
                'processed_at': resume_data.get('processed_at', 0)
            })
        return results
    
    def remove_resume(self, resume_id: str) -> bool:
        if resume_id in self.processed_resumes:
            del self.processed_resumes[resume_id]
            return True
        return False
    
    def clear_all(self):
        self.processed_resumes.clear()
        self.embedding_system.clear_cache()
    
    def get_stats(self) -> Dict:
        total_skills = 0
        total_companies = 0
        total_education = 0
        
        for resume_data in self.processed_resumes.values():
            entities = resume_data.get('entities', {})
            total_skills += entities.get('summary', {}).get('total_skills', 0)
            total_companies += entities.get('summary', {}).get('total_companies', 0)
            total_education += entities.get('summary', {}).get('total_education', 0)
        
        return {
            'total_resumes': len(self.processed_resumes),
            'embedding_cache_size': self.embedding_system.get_cache_stats()['embeddings_cache_size'],
            'text_cache_size': self.embedding_system.get_cache_stats()['text_cache_size'],
            'total_skills_extracted': total_skills,
            'total_companies_extracted': total_companies,
            'total_education_extracted': total_education
        } 