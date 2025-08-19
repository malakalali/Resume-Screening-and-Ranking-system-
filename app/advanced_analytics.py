import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime, date
import numpy as np

class AdvancedAnalytics:
    def __init__(self):
        self.skill_levels = {
            'beginner': ['basic', 'familiar', 'introductory', 'fundamental'],
            'intermediate': ['proficient', 'experienced', 'working knowledge', 'hands-on'],
            'advanced': ['expert', 'master', 'deep', 'extensive', 'senior', 'lead'],
            'expert': ['architect', 'principal', 'staff', 'distinguished', 'fellow']
        }
        
        self.experience_keywords = {
            'junior': ['junior', 'entry', 'associate', 'trainee', 'intern', 'graduate'],
            'mid': ['mid-level', 'intermediate', 'experienced', 'professional'],
            'senior': ['senior', 'lead', 'principal', 'staff', 'architect'],
            'executive': ['director', 'manager', 'head', 'chief', 'vp', 'cto', 'ceo']
        }
        
        self.salary_ranges = {
            'software_engineer': {
                'junior': (60000, 90000),
                'mid': (80000, 130000),
                'senior': (120000, 180000),
                'lead': (150000, 220000)
            },
            'data_scientist': {
                'junior': (70000, 100000),
                'mid': (90000, 140000),
                'senior': (130000, 190000),
                'lead': (160000, 240000)
            },
            'product_manager': {
                'junior': (65000, 95000),
                'mid': (85000, 140000),
                'senior': (130000, 190000),
                'lead': (160000, 250000)
            },
            'devops_engineer': {
                'junior': (65000, 95000),
                'mid': (85000, 140000),
                'senior': (130000, 180000),
                'lead': (150000, 220000)
            }
        }
        
        self.location_multipliers = {
            'san francisco': 1.4,
            'new york': 1.35,
            'seattle': 1.25,
            'austin': 1.15,
            'denver': 1.1,
            'remote': 0.95
        }
    
    def analyze_skill_gap(self, candidate_skills: List[str], required_skills: List[str]) -> Dict:
        candidate_skills_set = set(skill.lower() for skill in candidate_skills)
        required_skills_set = set(skill.lower() for skill in required_skills)
        
        missing_skills = required_skills_set - candidate_skills_set
        matching_skills = candidate_skills_set.intersection(required_skills_set)
        extra_skills = candidate_skills_set - required_skills_set
        
        coverage_percentage = len(matching_skills) / len(required_skills_set) * 100 if required_skills_set else 0
        
        skill_gap_score = max(0, 100 - coverage_percentage)
        
        return {
            'missing_skills': list(missing_skills),
            'matching_skills': list(matching_skills),
            'extra_skills': list(extra_skills),
            'coverage_percentage': round(coverage_percentage, 2),
            'skill_gap_score': round(skill_gap_score, 2),
            'total_required': len(required_skills_set),
            'total_matching': len(matching_skills),
            'total_missing': len(missing_skills)
        }
    
    def assess_experience_level(self, resume_text: str, entities: Dict) -> Dict:
        text_lower = resume_text.lower()
        
        experience_score = 0
        level_indicators = {}
        
        for level, keywords in self.experience_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            level_indicators[level] = count
            experience_score += count * self._get_level_weight(level)
        
        years_experience = self._extract_years_experience(resume_text, entities)
        
        job_titles = entities.get('work_experience', {}).get('job_titles', [])
        title_level = self._assess_title_level(job_titles)
        
        overall_level = self._determine_overall_level(experience_score, years_experience, title_level)
        
        return {
            'overall_level': overall_level,
            'years_experience': years_experience,
            'title_level': title_level,
            'experience_score': experience_score,
            'level_indicators': level_indicators,
            'confidence': self._calculate_confidence(entities)
        }
    
    def estimate_salary(self, job_title: str, experience_level: str, location: str = None, 
                       skills: List[str] = None, entities: Dict = None) -> Dict:
        base_role = self._categorize_job_title(job_title)
        
        if base_role not in self.salary_ranges:
            base_role = 'software_engineer'
        
        base_salary_range = self.salary_ranges[base_role].get(experience_level, 
                                                             self.salary_ranges[base_role]['mid'])
        
        location_multiplier = 1.0
        if location:
            location_lower = location.lower()
            for loc, multiplier in self.location_multipliers.items():
                if loc in location_lower:
                    location_multiplier = multiplier
                    break
        
        skill_bonus = self._calculate_skill_bonus(skills or [])
        experience_bonus = self._calculate_experience_bonus(entities)
        
        min_salary = int(base_salary_range[0] * location_multiplier * (1 + skill_bonus + experience_bonus))
        max_salary = int(base_salary_range[1] * location_multiplier * (1 + skill_bonus + experience_bonus))
        
        return {
            'salary_range': (min_salary, max_salary),
            'base_role': base_role,
            'experience_level': experience_level,
            'location_multiplier': location_multiplier,
            'skill_bonus': skill_bonus,
            'experience_bonus': experience_bonus,
            'estimated_midpoint': int((min_salary + max_salary) / 2),
            'confidence': self._calculate_salary_confidence(entities, skills)
        }
    
    def _extract_years_experience(self, resume_text: str, entities: Dict) -> float:
        dates = entities.get('work_experience', {}).get('dates', [])
        
        if not dates:
            return 0.0
        
        total_years = 0
        date_patterns = [
            r'(\d{4})\s*-\s*(\d{4})',
            r'(\d{4})\s*-\s*present',
            r'(\d{4})\s*-\s*current',
            r'(\d+)\s+years?',
            r'(\d+)\s+months?'
        ]
        
        for date_str in dates:
            for pattern in date_patterns:
                matches = re.findall(pattern, date_str.lower())
                if matches:
                    if len(matches[0]) == 2:
                        start_year, end_year = matches[0]
                        if end_year.isdigit():
                            total_years += int(end_year) - int(start_year)
                    elif 'years' in date_str:
                        total_years += int(matches[0])
                    elif 'months' in date_str:
                        total_years += int(matches[0]) / 12
        
        return round(total_years, 1)
    
    def _assess_title_level(self, job_titles: List[str]) -> str:
        if not job_titles:
            return 'mid'
        
        title_scores = {'junior': 0, 'mid': 0, 'senior': 0, 'executive': 0}
        
        for title in job_titles:
            title_lower = title.lower()
            for level, keywords in self.experience_keywords.items():
                if any(keyword in title_lower for keyword in keywords):
                    title_scores[level] += 1
        
        return max(title_scores, key=title_scores.get)
    
    def _determine_overall_level(self, experience_score: float, years_experience: float, title_level: str) -> str:
        if years_experience >= 10 or title_level == 'executive':
            return 'executive'
        elif years_experience >= 5 or title_level == 'senior' or experience_score >= 3:
            return 'senior'
        elif years_experience >= 2 or title_level == 'mid' or experience_score >= 1:
            return 'mid'
        else:
            return 'junior'
    
    def _get_level_weight(self, level: str) -> int:
        weights = {'junior': 1, 'mid': 2, 'senior': 3, 'executive': 4}
        return weights.get(level, 1)
    
    def _categorize_job_title(self, job_title: str) -> str:
        title_lower = job_title.lower()
        
        if any(word in title_lower for word in ['data', 'analytics', 'ml', 'ai', 'machine learning']):
            return 'data_scientist'
        elif any(word in title_lower for word in ['product', 'pm', 'manager']):
            return 'product_manager'
        elif any(word in title_lower for word in ['devops', 'infrastructure', 'platform']):
            return 'devops_engineer'
        else:
            return 'software_engineer'
    
    def _calculate_skill_bonus(self, skills: List[str]) -> float:
        premium_skills = ['machine learning', 'ai', 'python', 'aws', 'kubernetes', 'docker', 'react', 'node.js']
        skill_count = sum(1 for skill in skills if skill.lower() in premium_skills)
        return min(0.2, skill_count * 0.05)
    
    def _calculate_experience_bonus(self, entities: Dict) -> float:
        years = self._extract_years_experience("", entities)
        return min(0.15, years * 0.01)
    
    def _calculate_confidence(self, entities: Dict) -> float:
        confidence_factors = []
        
        if entities.get('work_experience', {}).get('companies'):
            confidence_factors.append(0.3)
        
        if entities.get('work_experience', {}).get('dates'):
            confidence_factors.append(0.3)
        
        if entities.get('education', {}).get('degrees'):
            confidence_factors.append(0.2)
        
        if entities.get('skills'):
            confidence_factors.append(0.2)
        
        return min(1.0, sum(confidence_factors))
    
    def _calculate_salary_confidence(self, entities: Dict, skills: List[str]) -> float:
        confidence = 0.5
        
        if entities.get('work_experience', {}).get('companies'):
            confidence += 0.2
        
        if entities.get('work_experience', {}).get('dates'):
            confidence += 0.2
        
        if skills and len(skills) > 5:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def generate_advanced_report(self, candidate_entities: Dict, job_requirements: Dict, 
                               job_title: str, location: str = None) -> Dict:
        candidate_skills = candidate_entities.get('skills', [])
        required_skills = job_requirements.get('skills', [])
        
        skill_gap = self.analyze_skill_gap(candidate_skills, required_skills)
        experience_assessment = self.assess_experience_level("", candidate_entities)
        salary_estimate = self.estimate_salary(
            job_title, 
            experience_assessment['overall_level'], 
            location, 
            candidate_skills, 
            candidate_entities
        )
        
        return {
            'skill_gap_analysis': skill_gap,
            'experience_assessment': experience_assessment,
            'salary_estimation': salary_estimate,
            'overall_recommendation': self._generate_recommendation(skill_gap, experience_assessment, salary_estimate)
        }
    
    def _generate_recommendation(self, skill_gap: Dict, experience: Dict, salary: Dict) -> str:
        if skill_gap['coverage_percentage'] >= 80 and experience['overall_level'] in ['senior', 'executive']:
            return "Strong Match - Highly Recommended"
        elif skill_gap['coverage_percentage'] >= 60 and experience['overall_level'] in ['mid', 'senior']:
            return "Good Match - Recommended"
        elif skill_gap['coverage_percentage'] >= 40:
            return "Moderate Match - Consider with Training"
        else:
            return "Weak Match - Not Recommended"
