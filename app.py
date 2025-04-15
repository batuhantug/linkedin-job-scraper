import streamlit as st
from scraper import LinkedInJobScraper
import pandas as pd

def main():
    st.title("LinkedIn Job Scraper")
    
    # Create sidebar inputs
    st.sidebar.header("Search Parameters")
    
    # Basic search parameters
    keywords = st.sidebar.text_input("Job Keywords", "Python Developer")
    location = st.sidebar.text_input("Location", "")
    
    # Advanced filters
    st.sidebar.subheader("Advanced Filters")
    
    # Work Type filter
    work_type = st.sidebar.selectbox(
        "Work Type",
        ["Any", "Remote", "On-site", "Hybrid"]
    )
    
    # Experience Level filter
    experience_level = st.sidebar.selectbox(
        "Experience Level",
        ["Any", "Internship", "Entry", "Associate", "Mid-Senior", "Director", "Executive"]
    )
    
    # Job Type filter
    job_type = st.sidebar.selectbox(
        "Job Type",
        ["Any", "Full-time", "Part-time", "Contract", "Temporary", "Internship", "Volunteer"]
    )
    
    # Number of pages to scrape
    pages = st.sidebar.number_input("Number of Pages to Scrape", min_value=1, max_value=5, value=1)
    
    if st.sidebar.button("Search Jobs"):
        scraper = LinkedInJobScraper()
        
        # Show progress bar
        progress_bar = st.progress(0)
        jobs = []
        
        # Convert "Any" to None for the scraper
        work_type_param = None if work_type == "Any" else work_type
        experience_level_param = None if experience_level == "Any" else experience_level
        job_type_param = None if job_type == "Any" else job_type
        
        for page in range(1, pages + 1):
            st.text(f"Scraping page {page}...")
            page_jobs = scraper.search_jobs(
                keywords=keywords,
                location=location,
                work_type=work_type_param,
                experience_level=experience_level_param,
                job_type=job_type_param,
                page=page
            )
            jobs.extend(page_jobs)
            progress_bar.progress(page / pages)
        
        if jobs:
            # Convert to DataFrame
            df = pd.DataFrame(jobs)
            
            # Display filter summary
            st.subheader("Search Filters Applied:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"Work Type: {work_type}")
            with col2:
                st.write(f"Experience: {experience_level}")
            with col3:
                st.write(f"Job Type: {job_type}")
            
            # Display results
            st.success(f"Found {len(jobs)} jobs!")
            st.dataframe(df)
            
            # Add download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name="linkedin_jobs.csv",
                mime="text/csv"
            )
            
            # Add some basic analytics
            st.subheader("Job Search Analytics")
            if 'company' in df.columns:
                st.write("Top Companies Hiring:")
                st.bar_chart(df['company'].value_counts().head(10))
            
            if 'location' in df.columns:
                st.write("Top Locations:")
                st.bar_chart(df['location'].value_counts().head(10))
            
        else:
            st.error("No jobs found. Try different search terms or filters.")

if __name__ == "__main__":
    main() 