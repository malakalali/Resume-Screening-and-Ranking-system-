import streamlit as st
import sys
import os
import tempfile
import time
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
from app.resume_matcher import ResumeMatcher

st.set_page_config(
    page_title="Resume Screening App",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .resume-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .match-score {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .keyword-tag {
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.8rem;
    }
    .gradient-text {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .entity-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
    }
    .entity-tag {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .entity-label {
        font-weight: 600;
        color: #667eea;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .entity-item {
        background: white;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.8rem;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-header"><h1>🎯 Resume Screening App</h1><p>AI-Powered Resume Matching with NLP</p></div>', unsafe_allow_html=True)

    if 'matcher' not in st.session_state:
        st.session_state.matcher = ResumeMatcher()
        st.session_state.resumes_processed = 0

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📁 Upload Resumes")
        uploaded_files = st.file_uploader(
            "Choose resume files (PDF or DOCX)",
            type=['pdf', 'docx'],
            accept_multiple_files=True,
            help="Upload one or more resume files"
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name

                    result = st.session_state.matcher.add_resume_file(tmp_file_path)
                    
                    if result['success']:
                        st.success(f"✅ {uploaded_file.name} processed successfully!")
                        st.session_state.resumes_processed += 1
                    else:
                        st.error(f"❌ Error processing {uploaded_file.name}: {result['error']}")
                    
                    os.unlink(tmp_file_path)

    with col2:
        st.markdown("### 📊 Statistics")
        stats = st.session_state.matcher.get_stats()
        
        col2a, col2b, col2c = st.columns(3)
        with col2a:
            st.markdown(f'<div class="metric-card"><h3>📄 Total Resumes</h3><div class="match-score">{stats["total_resumes"]}</div></div>', unsafe_allow_html=True)
        
        with col2b:
            st.markdown(f'<div class="metric-card"><h3>🧠 Cache Size</h3><div class="match-score">{stats["processor_stats"]["embedding_cache_size"]}</div></div>', unsafe_allow_html=True)
        
        with col2c:
            total_skills = stats["processor_stats"].get("total_skills_extracted", 0)
            st.markdown(f'<div class="metric-card"><h3>🛠️ Skills Extracted</h3><div class="match-score">{total_skills}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown("### 🎯 Job Description")
    
    with st.expander("📝 Job Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input(
                "Job Title",
                placeholder="e.g., Senior Software Engineer, Data Scientist, Product Manager"
            )
        
        with col2:
            location = st.text_input(
                "Location",
                placeholder="e.g., San Francisco, CA or Remote"
            )
        
        responsibilities = st.text_area(
            "Responsibilities",
            height=120,
            placeholder="Enter key responsibilities (one per line):\n• Lead development team\n• Design system architecture\n• Collaborate with stakeholders"
        )
        
        requirements = st.text_area(
            "Requirements",
            height=120,
            placeholder="Enter requirements (one per line):\n• 5+ years experience\n• Bachelor's degree\n• Python programming"
        )
        
        preferred_skills = st.text_area(
            "Preferred Skills",
            height=120,
            placeholder="Enter preferred skills (one per line):\n• Machine Learning\n• AWS\n• React\n• Docker"
        )
    
    def format_job_description(title, loc, resp, req, skills):
        sections = []
        
        if title:
            sections.append(f"**Job Title:** {title}")
        
        if loc:
            sections.append(f"**Location:** {loc}")
        
        if resp:
            sections.append("**Responsibilities:**")
            resp_lines = [line.strip() for line in resp.split('\n') if line.strip()]
            for line in resp_lines:
                if line.startswith('•'):
                    sections.append(line)
                else:
                    sections.append(f"• {line}")
        
        if req:
            sections.append("**Requirements:**")
            req_lines = [line.strip() for line in req.split('\n') if line.strip()]
            for line in req_lines:
                if line.startswith('•'):
                    sections.append(line)
                else:
                    sections.append(f"• {line}")
        
        if skills:
            sections.append("**Preferred Skills:**")
            skill_lines = [line.strip() for line in skills.split('\n') if line.strip()]
            for line in skill_lines:
                if line.startswith('•'):
                    sections.append(line)
                else:
                    sections.append(f"• {line}")
        
        return '\n\n'.join(sections) if sections else ""
    
    job_description = format_job_description(job_title, location, responsibilities, requirements, preferred_skills)
    
    if job_description:
        with st.expander("👀 Preview Job Description", expanded=False):
            st.markdown(job_description)
    
            col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            show_entities = st.checkbox("📊 Show Extracted Entities", value=True, help="Display skills, education, companies, and other extracted information")
        with col2:
            show_advanced = st.checkbox("🔍 Advanced Analytics", value=False, help="Show skill gap analysis, experience assessment, and salary estimation")
        with col3:
            top_k = st.selectbox("Number of Results", [3, 5, 10], index=1)

    if st.button("🚀 Find Matches", type="primary", use_container_width=True):
        if not job_description.strip():
            st.error("Please enter at least one job detail (title, location, responsibilities, requirements, or preferred skills)")
            return
        
        if stats["total_resumes"] == 0:
            st.error("Please upload at least one resume first")
            return

        with st.spinner("Analyzing resumes..."):
            matches = st.session_state.matcher.find_matches(job_description, top_k=top_k)
            
            if matches:
                st.markdown("### 🎯 Top Matches")
                
                for i, match in enumerate(matches):
                    with st.container():
                        st.markdown(f'<div class="resume-card">', unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Resume {match['resume_id'][:8]}...**")
                            st.markdown(f"📏 **Length:** {match['text_length']} characters")
                            
                            if match['matched_terms']:
                                st.markdown("**🔍 Matched Keywords:**")
                                keywords_html = " ".join([f'<span class="keyword-tag">{term}</span>' for term in match['matched_terms'][:8]])
                                st.markdown(keywords_html, unsafe_allow_html=True)
                            
                            if show_entities and 'entities' in match:
                                st.markdown("---")
                                st.markdown("**📊 Extracted Entities:**")
                                
                                entities = match['entities']
                                
                                if entities.get('skills'):
                                    st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                    st.markdown('<div class="entity-label">🛠️ Skills</div>', unsafe_allow_html=True)
                                    skills_html = " ".join([f'<span class="entity-tag">{skill}</span>' for skill in entities['skills'][:10]])
                                    st.markdown(skills_html, unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                if entities.get('education', {}).get('degrees') or entities.get('education', {}).get('institutions'):
                                    st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                    st.markdown('<div class="entity-label">🎓 Education</div>', unsafe_allow_html=True)
                                    
                                    if entities['education'].get('degrees'):
                                        st.markdown("**Degrees:**")
                                        degrees_html = " ".join([f'<span class="entity-item">{degree}</span>' for degree in entities['education']['degrees']])
                                        st.markdown(degrees_html, unsafe_allow_html=True)
                                    
                                    if entities['education'].get('institutions'):
                                        st.markdown("**Institutions:**")
                                        institutions_html = " ".join([f'<span class="entity-item">{institution}</span>' for institution in entities['education']['institutions']])
                                        st.markdown(institutions_html, unsafe_allow_html=True)
                                    
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                if entities.get('work_experience', {}).get('companies'):
                                    st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                    st.markdown('<div class="entity-label">🏢 Companies</div>', unsafe_allow_html=True)
                                    companies_html = " ".join([f'<span class="entity-item">{company}</span>' for company in entities['work_experience']['companies'][:8]])
                                    st.markdown(companies_html, unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                if entities.get('work_experience', {}).get('dates'):
                                    st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                    st.markdown('<div class="entity-label">📅 Dates</div>', unsafe_allow_html=True)
                                    dates_html = " ".join([f'<span class="entity-item">{date}</span>' for date in entities['work_experience']['dates'][:5]])
                                    st.markdown(dates_html, unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                if entities.get('work_experience', {}).get('locations'):
                                    st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                    st.markdown('<div class="entity-label">📍 Locations</div>', unsafe_allow_html=True)
                                    locations_html = " ".join([f'<span class="entity-item">{location}</span>' for location in entities['work_experience']['locations'][:5]])
                                    st.markdown(locations_html, unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f'<div class="match-score">{match["match_score"]}%</div>', unsafe_allow_html=True)
                            st.markdown("**Match Score**")
                            
                            if show_entities and 'entities' in match:
                                entities = match['entities']
                                summary = entities.get('summary', {})
                                
                                st.markdown("---")
                                st.markdown("**📈 Entity Summary:**")
                                st.markdown(f"• Skills: {summary.get('total_skills', 0)}")
                                st.markdown(f"• Companies: {summary.get('total_companies', 0)}")
                                st.markdown(f"• Education: {summary.get('total_education', 0)}")
                            
                            if show_advanced and 'entities' in match:
                                st.markdown("---")
                                st.markdown("**🔍 Advanced Analytics:**")
                                
                                required_skills = []
                                if preferred_skills:
                                    required_skills = [skill.strip() for skill in preferred_skills.split('\n') if skill.strip()]
                                
                                if required_skills:
                                    skill_gap = st.session_state.matcher.analyze_skill_gap(match['resume_id'], required_skills)
                                    if 'error' not in skill_gap:
                                        st.markdown(f"**Skill Gap:** {skill_gap['coverage_percentage']}% coverage")
                                        if skill_gap['missing_skills']:
                                            st.markdown(f"Missing: {', '.join(skill_gap['missing_skills'][:3])}")
                                
                                experience = st.session_state.matcher.assess_experience_level(match['resume_id'])
                                if 'error' not in experience:
                                    st.markdown(f"**Experience:** {experience['overall_level'].title()} ({experience['years_experience']} years)")
                                
                                if job_title:
                                    salary = st.session_state.matcher.estimate_salary(match['resume_id'], job_title, location)
                                    if 'error' not in salary:
                                        st.markdown(f"**Salary:** ${salary['estimated_midpoint']:,}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                if show_advanced:
                    st.markdown("### 🔍 Advanced Analytics Dashboard")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**📊 Skill Gap Analysis**")
                        if preferred_skills:
                            required_skills = [skill.strip() for skill in preferred_skills.split('\n') if skill.strip()]
                            if required_skills and matches:
                                avg_coverage = 0
                                total_candidates = 0
                                for match in matches[:3]:
                                    skill_gap = st.session_state.matcher.analyze_skill_gap(match['resume_id'], required_skills)
                                    if 'error' not in skill_gap:
                                        avg_coverage += skill_gap['coverage_percentage']
                                        total_candidates += 1
                                
                                if total_candidates > 0:
                                    avg_coverage = avg_coverage / total_candidates
                                    st.metric("Average Skill Coverage", f"{avg_coverage:.1f}%")
                    
                    with col2:
                        st.markdown("**👨‍💼 Experience Assessment**")
                        if matches:
                            experience_levels = []
                            for match in matches[:3]:
                                experience = st.session_state.matcher.assess_experience_level(match['resume_id'])
                                if 'error' not in experience:
                                    experience_levels.append(experience['overall_level'])
                            
                            if experience_levels:
                                most_common = max(set(experience_levels), key=experience_levels.count)
                                st.metric("Most Common Level", most_common.title())
                    
                    with col3:
                        st.markdown("**💰 Salary Estimation**")
                        if job_title and matches:
                            salaries = []
                            for match in matches[:3]:
                                salary = st.session_state.matcher.estimate_salary(match['resume_id'], job_title, location)
                                if 'error' not in salary:
                                    salaries.append(salary['estimated_midpoint'])
                            
                            if salaries:
                                avg_salary = sum(salaries) / len(salaries)
                                st.metric("Average Salary", f"${avg_salary:,.0f}")
                
                analysis = st.session_state.matcher.analyze_match_quality(job_description, top_k=3)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Average Score", f"{analysis['average_score']:.1f}%")
                
                with col2:
                    st.metric("Score Range", f"{analysis['score_range'][0]:.1f}% - {analysis['score_range'][1]:.1f}%")
                
                with col3:
                    st.metric("Top Match", f"{analysis['top_match_score']:.1f}%")
                
                if analysis['average_score'] > 50:
                    st.success("🎉 Excellent matches found!")
                elif analysis['average_score'] > 30:
                    st.info("👍 Good matches found")
                else:
                    st.warning("⚠️ Low match scores - consider refining the job description")

    st.markdown("---")
    
    with st.expander("🔧 Advanced Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear All Resumes", type="secondary"):
                st.session_state.matcher.clear_all()
                st.session_state.resumes_processed = 0
                st.rerun()
        
        with col2:
            if st.button("📈 View Detailed Stats", type="secondary"):
                stats = st.session_state.matcher.get_stats()
                st.json(stats)

if __name__ == "__main__":
    main() 