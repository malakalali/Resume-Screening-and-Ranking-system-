from typing import Dict, List, Optional
from .resume_processor import ResumeProcessor
from .matching_engine import MatchingEngine
from .advanced_analytics import AdvancedAnalytics

class ResumeMatcher:
    def __init__(self):
        self.processor = ResumeProcessor()
        self.matching_engine = MatchingEngine()
        self.analytics = AdvancedAnalytics()
    
    def add_resume_file(self, file_path: str) -> Dict:
        result = self.processor.process_resume_file(file_path)
        
        if result['success']:
            resume_data = self.processor.processed_resumes[result['resume_id']]
            self.matching_engine.add_resume(
                result['resume_id'],
                resume_data['text'],
                resume_data['sections'],
                resume_data.get('entities', {})
            )
        
        return result
    
    def add_resume_text(self, text: str, resume_id: str = None) -> Dict:
        result = self.processor.process_resume_text(text, resume_id)
        
        if result['success']:
            resume_data = self.processor.processed_resumes[result['resume_id']]
            self.matching_engine.add_resume(
                result['resume_id'],
                resume_data['text'],
                resume_data['sections'],
                resume_data.get('entities', {})
            )
        
        return result
    
    def find_matches(self, job_description: str, top_k: int = 5) -> List[Dict]:
        return self.matching_engine.match_job_to_resumes(job_description, top_k)
    
    def match_single_resume(self, resume_id: str, job_description: str) -> Optional[Dict]:
        return self.matching_engine.match_single_resume(resume_id, job_description)
    
    def get_resume_details(self, resume_id: str) -> Optional[Dict]:
        resume_info = self.processor.get_resume_info(resume_id)
        if not resume_info:
            return None
        
        match_info = self.matching_engine.get_resume_info(resume_id)
        
        return {
            'resume_id': resume_id,
            'text_length': resume_info['text_length'],
            'sections': resume_info['sections'],
            'processed_at': resume_info.get('processed_at', 0),
            'has_embedding': match_info is not None
        }
    
    def get_all_resumes(self) -> List[Dict]:
        return self.processor.get_all_resumes()
    
    def remove_resume(self, resume_id: str) -> bool:
        processor_removed = self.processor.remove_resume(resume_id)
        engine_removed = self.matching_engine.remove_resume(resume_id)
        return processor_removed or engine_removed
    
    def clear_all(self):
        self.processor.clear_all()
        self.matching_engine.clear_all()
    
    def get_stats(self) -> Dict:
        processor_stats = self.processor.get_stats()
        engine_stats = self.matching_engine.get_stats()
        
        return {
            'processor_stats': processor_stats,
            'engine_stats': engine_stats,
            'total_resumes': processor_stats['total_resumes']
        }
    
    def analyze_match_quality(self, job_description: str, top_k: int = 3) -> Dict:
        matches = self.find_matches(job_description, top_k)
        
        if not matches:
            return {
                'total_matches': 0,
                'average_score': 0,
                'score_range': (0, 0),
                'top_match_score': 0
            }
        
        scores = [match['match_score'] for match in matches]
        
        return {
            'total_matches': len(matches),
            'average_score': sum(scores) / len(scores),
            'score_range': (min(scores), max(scores)),
            'top_match_score': max(scores),
            'matches': matches
        }
    
    def analyze_skill_gap(self, resume_id: str, required_skills: List[str]) -> Dict:
        resume_data = self.processor.get_resume_info(resume_id)
        if not resume_data or 'entities' not in resume_data:
            return {'error': 'Resume not found or no entities available'}
        
        candidate_skills = resume_data['entities'].get('skills', [])
        return self.analytics.analyze_skill_gap(candidate_skills, required_skills)
    
    def assess_experience_level(self, resume_id: str) -> Dict:
        resume_data = self.processor.get_resume_info(resume_id)
        if not resume_data or 'entities' not in resume_data:
            return {'error': 'Resume not found or no entities available'}
        
        resume_text = self.processor.processed_resumes[resume_id]['text']
        entities = resume_data['entities']
        return self.analytics.assess_experience_level(resume_text, entities)
    
    def estimate_salary(self, resume_id: str, job_title: str, location: str = None) -> Dict:
        resume_data = self.processor.get_resume_info(resume_id)
        if not resume_data or 'entities' not in resume_data:
            return {'error': 'Resume not found or no entities available'}
        
        entities = resume_data['entities']
        skills = entities.get('skills', [])
        experience_assessment = self.assess_experience_level(resume_id)
        
        if 'error' in experience_assessment:
            return {'error': 'Unable to assess experience level'}
        
        return self.analytics.estimate_salary(
            job_title,
            experience_assessment['overall_level'],
            location,
            skills,
            entities
        )
    
    def generate_advanced_report(self, resume_id: str, job_requirements: Dict, 
                               job_title: str, location: str = None) -> Dict:
        resume_data = self.processor.get_resume_info(resume_id)
        if not resume_data or 'entities' not in resume_data:
            return {'error': 'Resume not found or no entities available'}
        
        entities = resume_data['entities']
        return self.analytics.generate_advanced_report(entities, job_requirements, job_title, location) 