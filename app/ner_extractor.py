import spacy
import re
from typing import Dict, List, Set
from datetime import datetime

class NERExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.skill_patterns = [
            r'\b(?:Python|Java|JavaScript|C\+\+|C#|Ruby|PHP|Swift|Kotlin|Go|Rust|Scala|TypeScript|React|Angular|Vue|Node\.js|Django|Flask|Spring|Laravel|Express|MongoDB|PostgreSQL|MySQL|Redis|Docker|Kubernetes|AWS|Azure|GCP|Git|Jenkins|Jira|Agile|Scrum|Machine Learning|AI|Data Science|SQL|NoSQL|HTML|CSS|REST|API|GraphQL|Microservices|DevOps|CI/CD|TensorFlow|PyTorch|Scikit-learn|Pandas|NumPy|Spark|Hadoop|Jupyter|Tableau|Power BI|Looker|Salesforce|HubSpot|Zendesk|Slack|Teams|Zoom|Skype|Trello|Asana|Notion|Confluence|Bitbucket|GitHub|GitLab)\b',
            r'\b(?:Excel|Word|PowerPoint|Outlook|Photoshop|Illustrator|InDesign|Premiere|After Effects|AutoCAD|SolidWorks|MATLAB|R|SAS|SPSS)\b'
        ]
        
        self.education_keywords = {
            'degrees': ['bachelor', 'master', 'phd', 'doctorate', 'associate', 'diploma', 'certificate'],
            'fields': ['computer science', 'engineering', 'business', 'mathematics', 'statistics', 'economics', 'finance', 'marketing', 'management', 'information technology', 'data science', 'artificial intelligence', 'machine learning']
        }
        
        self.experience_keywords = ['experience', 'work', 'employment', 'job', 'position', 'role', 'career']
        
    def extract_entities(self, text: str) -> Dict:
        doc = self.nlp(text)
        
        entities = {
            'skills': self._extract_skills(text, doc),
            'education': self._extract_education(text, doc),
            'experience': self._extract_experience(text, doc),
            'companies': self._extract_companies(doc),
            'dates': self._extract_dates(doc),
            'locations': self._extract_locations(doc),
            'titles': self._extract_titles(doc)
        }
        
        return entities
    
    def _extract_skills(self, text: str, doc) -> List[str]:
        skills = set()
        
        for pattern in self.skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update(matches)
        
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
                if any(keyword in token.text.lower() for keyword in ['tech', 'tool', 'framework', 'library', 'platform']):
                    if not any(company_word in token.text.lower() for company_word in ['techcorp', 'startupxyz', 'stanford', 'mit']):
                        skills.add(token.text.strip())
        
        return sorted(list(skills))
    
    def _extract_education(self, text: str, doc) -> Dict:
        education_info = {
            'degrees': [],
            'institutions': [],
            'fields': [],
            'years': []
        }
        
        text_lower = text.lower()
        
        for degree in self.education_keywords['degrees']:
            if degree in text_lower:
                education_info['degrees'].append(degree.title())
        
        for field in self.education_keywords['fields']:
            if field in text_lower:
                education_info['fields'].append(field.title())
        
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                if any(edu_word in ent.text.lower() for edu_word in ['university', 'college', 'school', 'institute', 'academy']):
                    education_info['institutions'].append(ent.text)
        
        return education_info
    
    def _extract_experience(self, text: str, doc) -> Dict:
        experience_info = {
            'duration': [],
            'roles': [],
            'companies': []
        }
        
        text_lower = text.lower()
        
        for keyword in self.experience_keywords:
            if keyword in text_lower:
                experience_info['duration'].append(keyword)
        
        return experience_info
    
    def _extract_companies(self, doc) -> List[str]:
        companies = []
        skill_words = ['python', 'java', 'react', 'docker', 'aws', 'git', 'sql', 'javascript', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'spark', 'hadoop', 'tableau', 'power bi', 'slack', 'teams', 'zoom', 'skype', 'trello', 'asana', 'notion', 'confluence', 'bitbucket', 'github', 'gitlab']
        
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                text_lower = ent.text.lower()
                if not any(edu_word in text_lower for edu_word in ['university', 'college', 'school', 'institute', 'academy']):
                    if not any(skill_word in text_lower for skill_word in skill_words):
                        if len(ent.text.strip()) > 2:
                            if not any(char.isdigit() for char in ent.text):
                                companies.append(ent.text.strip())
        
        return list(set(companies))
    
    def _extract_dates(self, doc) -> List[str]:
        dates = []
        
        for ent in doc.ents:
            if ent.label_ == 'DATE':
                dates.append(ent.text)
        
        return dates
    
    def _extract_locations(self, doc) -> List[str]:
        locations = []
        skill_words = ['react', 'node.js', 'django', 'flask', 'postgresql', 'python', 'numpy', 'pandas', 'tensorflow', 'pytorch', 'spark', 'hadoop', 'tableau', 'power bi']
        
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                if not any(skill_word in ent.text.lower() for skill_word in skill_words):
                    if len(ent.text.strip()) > 1:
                        if not any(char.isdigit() for char in ent.text):
                            locations.append(ent.text.strip())
        
        return list(set(locations))
    
    def _extract_titles(self, doc) -> List[str]:
        titles = []
        
        for ent in doc.ents:
            if ent.label_ == 'WORK_OF_ART':
                if any(title_word in ent.text.lower() for title_word in ['manager', 'director', 'engineer', 'developer', 'analyst', 'specialist', 'coordinator', 'assistant', 'lead', 'senior', 'junior']):
                    titles.append(ent.text.strip())
        
        return list(set(titles))
    
    def get_structured_entities(self, text: str) -> Dict:
        entities = self.extract_entities(text)
        
        structured_output = {
            'skills': entities['skills'],
            'education': {
                'degrees': entities['education']['degrees'],
                'institutions': entities['education']['institutions'],
                'fields_of_study': entities['education']['fields']
            },
            'work_experience': {
                'companies': entities['companies'],
                'job_titles': entities['titles'],
                'locations': entities['locations'],
                'dates': entities['dates']
            },
            'summary': {
                'total_skills': len(entities['skills']),
                'total_companies': len(entities['companies']),
                'total_education': len(entities['education']['degrees']) + len(entities['education']['institutions'])
            }
        }
        
        return structured_output
