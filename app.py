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
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f8fffe 0%, #f0f8ff 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        text-align: center;
        box-shadow: 0 12px 40px rgba(16, 185, 129, 0.25);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        margin: 0;
    }
    
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.15);
        text-align: center;
        margin: 1rem 0;
        border: 2px solid #e8f5e8;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #10b981, #3b82f6);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(16, 185, 129, 0.25);
        border-color: #10b981;
    }
    
    .metric-card h3 {
        color: #059669;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }
    
    .resume-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 5px solid #10b981;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.12);
        border: 2px solid #e8f5e8;
        transition: all 0.3s ease;
    }
    
    .resume-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(16, 185, 129, 0.2);
        border-color: #10b981;
    }
    
    .match-score {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
        text-shadow: none;
    }
    
    .keyword-tag {
        background: linear-gradient(135deg, #dbeafe 0%, #d1fae5 100%);
        color: #1d4ed8;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 600;
        border: 2px solid #e8f5e8;
        transition: all 0.3s ease;
    }
    
    .keyword-tag:hover {
        background: linear-gradient(135deg, #bfdbfe 0%, #a7f3d0 100%);
        transform: translateY(-1px);
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    .entity-section {
        background: linear-gradient(135deg, #f0f9ff 0%, #ecfdf5 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border: 2px solid #e8f5e8;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .entity-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #10b981, #3b82f6);
    }
    
    .entity-section:hover {
        border-color: #10b981;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
        transform: translateY(-2px);
    }
    
    .entity-tag {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
    }
    
    .entity-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4);
    }
    
    .entity-label {
        font-weight: 700;
        color: #059669;
        margin-bottom: 0.8rem;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #e8f5e8;
        padding-bottom: 0.5rem;
        display: inline-block;
    }
    
    .entity-item {
        background: white;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        margin: 0.3rem;
        display: inline-block;
        font-size: 0.85rem;
        border: 2px solid #e8f5e8;
        color: #374151;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .entity-item:hover {
        border-color: #10b981;
        background: #f0fdf4;
        transform: translateY(-1px);
    }
    
    /* Custom Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        color: white;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
    }
    
    /* Custom Input Styles */
    .stTextInput > div > div > input {
        border: 2px solid #e8f5e8;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    .stTextArea > div > div > textarea {
        border: 2px solid #e8f5e8;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    /* Custom Selectbox Styles */
    .stSelectbox > div > div > div {
        border: 2px solid #e8f5e8;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div > div:focus-within {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    /* Custom Checkbox Styles */
    .stCheckbox > label {
        color: #059669;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Custom Expander Styles */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f0f9ff 0%, #ecfdf5 100%);
        border: 2px solid #e8f5e8;
        border-radius: 12px;
        color: #059669;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    /* Success/Info/Warning Messages */
    .stSuccess {
        background: linear-gradient(135deg, #ecfdf5 0%, #f0f9ff 100%);
        border: 2px solid #10b981;
        border-radius: 12px;
        color: #059669;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #eff6ff 0%, #ecfdf5 100%);
        border: 2px solid #3b82f6;
        border-radius: 12px;
        color: #1d4ed8;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 2px solid #f59e0b;
        border-radius: 12px;
        color: #d97706;
    }
    
    /* File Uploader */
    .stFileUploader > div > div {
        border: 2px dashed #10b981;
        border-radius: 12px;
        background: linear-gradient(135deg, #f0fdf4 0%, #f0f9ff 100%);
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #059669;
        background: linear-gradient(135deg, #ecfdf5 0%, #eff6ff 100%);
    }
    
    /* Section Headers */
    h3 {
        color: #059669;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.4rem;
    }
    
    /* Advanced Analytics Dashboard */
    .advanced-dashboard {
        background: linear-gradient(135deg, #f0f9ff 0%, #ecfdf5 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid #e8f5e8;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.1);
    }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 2px solid #e8f5e8;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.08);
    }
    
    /* Summary Metrics */
    .summary-metrics {
        background: linear-gradient(135deg, #ecfdf5 0%, #f0f9ff 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #10b981;
    }
    
    /* Chart Titles */
    .chart-title {
        color: #059669;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Entity Placeholder Text */
    .entity-placeholder {
        background: #f8fafc;
        color: #64748b;
        padding: 1rem;
        border-radius: 8px;
        border: 2px dashed #cbd5e1;
        text-align: center;
        font-style: italic;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        display: block;
    }
    
    /* Empty Section Styling */
    .entity-section:empty::after {
        content: 'No data available';
        display: block;
        text-align: center;
        color: #64748b;
        font-style: italic;
        padding: 1rem;
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
                                st.markdown("**📊 Resume Analysis**")
                                
                                entities = match['entities']
                                
                                # Create organized columns for better layout
                                entity_col1, entity_col2 = st.columns(2)
                                
                                with entity_col1:
                                    # Skills Section
                                    if entities.get('skills'):
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">🛠️ Technical Skills</div>', unsafe_allow_html=True)
                                        skills_html = " ".join([f'<span class="entity-tag">{skill}</span>' for skill in entities['skills'][:8]])
                                        st.markdown(skills_html, unsafe_allow_html=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    else:
                                        # Empty skills section with placeholder
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">🛠️ Technical Skills</div>', unsafe_allow_html=True)
                                        st.markdown('<span class="entity-placeholder">No technical skills detected</span>', unsafe_allow_html=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # Education Section
                                    if entities.get('education', {}).get('degrees') or entities.get('education', {}).get('institutions'):
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">🎓 Education & Certifications</div>', unsafe_allow_html=True)
                                        
                                        if entities['education'].get('degrees'):
                                            st.markdown("**Degrees:**")
                                            degrees_html = " ".join([f'<span class="entity-item">{degree}</span>' for degree in entities['education']['degrees'][:3]])
                                            st.markdown(degrees_html, unsafe_allow_html=True)
                                        
                                        if entities['education'].get('institutions'):
                                            st.markdown("**Institutions:**")
                                            institutions_html = " ".join([f'<span class="entity-item">{institution}</span>' for institution in entities['education']['institutions'][:3]])
                                            st.markdown(institutions_html, unsafe_allow_html=True)
                                        
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    else:
                                        # Empty education section with placeholder
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">🎓 Education & Certifications</div>', unsafe_allow_html=True)
                                        st.markdown('<span class="entity-placeholder">No education information detected</span>', unsafe_allow_html=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # Dates Section
                                    if entities.get('work_experience', {}).get('dates'):
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">📅 Key Dates & Timeline</div>', unsafe_allow_html=True)
                                        dates_html = " ".join([f'<span class="entity-item">{date}</span>' for date in entities['work_experience']['dates'][:3]])
                                        st.markdown(dates_html, unsafe_allow_html=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    else:
                                        # Empty dates section with placeholder
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">📅 Key Dates & Timeline</div>', unsafe_allow_html=True)
                                        st.markdown('<span class="entity-placeholder">No date information detected</span>', unsafe_allow_html=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                
                                with entity_col2:
                                    # Companies Section
                                    if entities.get('work_experience', {}).get('companies'):
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">🏢 Companies & Organizations</div>', unsafe_allow_html=True)
                                        companies_html = " ".join([f'<span class="entity-item">{company}</span>' for company in entities['work_experience']['companies'][:5]])
                                        st.markdown(companies_html, unsafe_allow_html=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    else:
                                        # Empty companies section with placeholder
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">🏢 Companies & Organizations</div>', unsafe_allow_html=True)
                                        st.markdown('<span class="entity-placeholder">No company information detected</span>', unsafe_allow_html=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # Locations Section
                                    if entities.get('work_experience', {}).get('locations'):
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">📍 Geographic Locations</div>', unsafe_allow_html=True)
                                        locations_html = " ".join([f'<span class="entity-item">{location}</span>' for location in entities['work_experience']['locations'][:3]])
                                        st.markdown(locations_html, unsafe_allow_html=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    else:
                                        # Empty locations section with placeholder
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">📍 Geographic Locations</div>', unsafe_allow_html=True)
                                        st.markdown('<span class="entity-placeholder">No location information detected</span>', unsafe_allow_html=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # Job Titles Section
                                    if entities.get('work_experience', {}).get('titles'):
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">👔 Job Titles & Roles</div>', unsafe_allow_html=True)
                                        titles_html = " ".join([f'<span class="entity-item">{title}</span>' for title in entities['work_experience']['titles'][:4]])
                                        st.markdown(titles_html, unsafe_allow_html=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    else:
                                        # Empty job titles section with placeholder
                                        st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                        st.markdown('<div class="entity-label">👔 Job Titles & Roles</div>', unsafe_allow_html=True)
                                        st.markdown('<span class="entity-placeholder">No job titles detected</span>', unsafe_allow_html=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                
                                # Summary statistics in a clean row
                                if entities:
                                    st.markdown('<div class="entity-section">', unsafe_allow_html=True)
                                    st.markdown("**📈 Resume Summary**")
                                    
                                    summary_stats = []
                                    if entities.get('skills'): summary_stats.append(f"**{len(entities['skills'])} Skills**")
                                    if entities.get('education', {}).get('degrees'): summary_stats.append(f"**{len(entities['education']['degrees'])} Degrees**")
                                    if entities.get('work_experience', {}).get('companies'): summary_stats.append(f"**{len(entities['work_experience']['companies'])} Companies**")
                                    if entities.get('work_experience', {}).get('locations'): summary_stats.append(f"**{len(entities['work_experience']['locations'])} Locations**")
                                    if entities.get('work_experience', {}).get('titles'): summary_stats.append(f"**{len(entities['work_experience']['titles'])} Job Titles**")
                                    if entities.get('work_experience', {}).get('dates'): summary_stats.append(f"**{len(entities['work_experience']['dates'])} Dates**")
                                    
                                    if summary_stats:
                                        st.markdown(" • ".join(summary_stats))
                                    else:
                                        st.markdown('<span class="entity-placeholder">No entities extracted from this resume</span>', unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f'<div class="match-score">{match["match_score"]}%</div>', unsafe_allow_html=True)
                            st.markdown("**Match Score**")
                            
                            if show_entities and 'entities' in match:
                                entities = match['entities']
                                
                                st.markdown("---")
                                st.markdown("**📊 Quick Stats**")
                                
                                # Show key metrics in a clean format
                                if entities.get('skills'):
                                    st.markdown(f"🛠️ **{len(entities['skills'])} Skills**")
                                if entities.get('work_experience', {}).get('companies'):
                                    st.markdown(f"🏢 **{len(entities['work_experience']['companies'])} Companies**")
                                if entities.get('education', {}).get('degrees'):
                                    st.markdown(f"🎓 **{len(entities['education']['degrees'])} Degrees**")
                            
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
                    st.markdown('<div class="advanced-dashboard">', unsafe_allow_html=True)
                    st.markdown("### 🔍 Advanced Analytics Dashboard")
                    
                    # Top row with metrics
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
                    
                    # Summary Statistics
                    if matches:
                        st.markdown("---")
                        st.markdown("### 📊 Summary Statistics")
                        
                        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
                        
                        with summary_col1:
                            avg_score = sum(match['match_score'] for match in matches) / len(matches)
                            st.metric("📈 Average Match Score", f"{avg_score:.1f}%")
                        
                        with summary_col2:
                            top_score = max(match['match_score'] for match in matches)
                            st.metric("🏆 Highest Score", f"{top_score:.1f}%")
                        
                        with summary_col3:
                            total_candidates = len(matches)
                            st.metric("👥 Total Candidates", f"{total_candidates}")
                        
                        with summary_col4:
                            strong_matches = len([m for m in matches if m['match_score'] >= 80])
                            st.metric("✅ Strong Matches", f"{strong_matches}")
                    
                    # Charts and visualizations
                    if matches:
                        st.markdown("---")
                        st.markdown("### 📈 Visual Analytics")
                        
                        # Match Score Distribution Chart
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**🎯 Match Score Distribution**")
                            match_scores = [match['match_score'] for match in matches]
                            candidate_names = [f"Resume {i+1}" for i in range(len(matches))]
                            
                            # Create a bar chart using plotly
                            try:
                                import plotly.express as px
                                import plotly.graph_objects as go
                                
                                fig = px.bar(
                                    x=candidate_names,
                                    y=match_scores,
                                    color=match_scores,
                                    color_continuous_scale='RdYlGn',
                                    title="Match Scores by Candidate",
                                    labels={'x': 'Candidates', 'y': 'Match Score (%)', 'color': 'Score'}
                                )
                                fig.update_layout(
                                    height=400,
                                    showlegend=False,
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)'
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            except ImportError:
                                # Fallback to simple chart
                                chart_data = pd.DataFrame({
                                    'Candidate': candidate_names,
                                    'Match Score': match_scores
                                })
                                st.bar_chart(chart_data.set_index('Candidate'))
                        
                        with col2:
                            st.markdown("**🛠️ Skill Coverage Analysis**")
                            if preferred_skills and matches:
                                required_skills = [skill.strip() for skill in preferred_skills.split('\n') if skill.strip()]
                                if required_skills:
                                    # Calculate skill coverage for each candidate
                                    skill_coverage_data = []
                                    for i, match in enumerate(matches[:5]):  # Top 5 candidates
                                        skill_gap = st.session_state.matcher.analyze_skill_gap(match['resume_id'], required_skills)
                                        if 'error' not in skill_gap:
                                            skill_coverage_data.append({
                                                'Candidate': f"Resume {i+1}",
                                                'Coverage': skill_gap['coverage_percentage'],
                                                'Missing': len(skill_gap['missing_skills']),
                                                'Extra': len(skill_gap['extra_skills'])
                                            })
                                    
                                    if skill_coverage_data:
                                        try:
                                            # Create skill coverage chart
                                            coverage_df = pd.DataFrame(skill_coverage_data)
                                            
                                            fig = go.Figure()
                                            fig.add_trace(go.Bar(
                                                name='Coverage %',
                                                x=coverage_df['Candidate'],
                                                y=coverage_df['Coverage'],
                                                marker_color='#10b981'
                                            ))
                                            fig.add_trace(go.Bar(
                                                name='Missing Skills',
                                                x=coverage_df['Candidate'],
                                                y=coverage_df['Missing'],
                                                marker_color='#ef4444'
                                            ))
                                            fig.add_trace(go.Bar(
                                                name='Extra Skills',
                                                x=coverage_df['Candidate'],
                                                y=coverage_df['Extra'],
                                                marker_color='#3b82f6'
                                            ))
                                            
                                            fig.update_layout(
                                                title="Skill Coverage Analysis",
                                                barmode='group',
                                                height=400,
                                                plot_bgcolor='rgba(0,0,0,0)',
                                                paper_bgcolor='rgba(0,0,0,0)'
                                            )
                                            st.plotly_chart(fig, use_container_width=True)
                                        except Exception as e:
                                            st.error(f"Chart error: {e}")
                    
                    # Experience Level Distribution
                    if matches:
                        st.markdown("---")
                        st.markdown("### 👥 Experience Level Analysis")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**📊 Experience Level Distribution**")
                            experience_data = []
                            for match in matches:
                                experience = st.session_state.matcher.assess_experience_level(match['resume_id'])
                                if 'error' not in experience:
                                    experience_data.append(experience['overall_level'])
                            
                            if experience_data:
                                # Count experience levels
                                from collections import Counter
                                level_counts = Counter(experience_data)
                                
                                try:
                                    fig = px.pie(
                                        values=list(level_counts.values()),
                                        names=list(level_counts.keys()),
                                        title="Experience Level Distribution",
                                        color_discrete_sequence=px.colors.qualitative.Set3
                                    )
                                    fig.update_layout(height=400)
                                    st.plotly_chart(fig, use_container_width=True)
                                except Exception as e:
                                    st.error(f"Chart error: {e}")
                        
                        with col2:
                            st.markdown("**💰 Salary Range Analysis**")
                            if job_title and matches:
                                salary_data = []
                                for match in matches:
                                    salary = st.session_state.matcher.estimate_salary(match['resume_id'], job_title, location)
                                    if 'error' not in salary:
                                        salary_data.append({
                                            'Candidate': f"Resume {len(salary_data)+1}",
                                            'Min': salary['estimated_min'],
                                            'Max': salary['estimated_max'],
                                            'Midpoint': salary['estimated_midpoint']
                                        })
                                
                                if salary_data:
                                    try:
                                        salary_df = pd.DataFrame(salary_data)
                                        
                                        fig = go.Figure()
                                        fig.add_trace(go.Bar(
                                            name='Min Salary',
                                            x=salary_df['Candidate'],
                                            y=salary_df['Min'],
                                            marker_color='#f59e0b'
                                        ))
                                        fig.add_trace(go.Bar(
                                            name='Max Salary',
                                            x=salary_df['Candidate'],
                                            y=salary_df['Max'],
                                            marker_color='#10b981'
                                        ))
                                        
                                        fig.update_layout(
                                            title="Salary Range by Candidate",
                                            barmode='group',
                                            height=400,
                                            yaxis_title="Salary ($)",
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            paper_bgcolor='rgba(0,0,0,0)'
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                    except Exception as e:
                                        st.error(f"Chart error: {e}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
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