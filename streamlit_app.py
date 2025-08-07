import re
import streamlit as st
from serpapi import GoogleSearch
import openai
from firecrawl import FirecrawlApp
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import io
from datetime import datetime

st.set_page_config(page_title="Research Assistant", layout="wide")
st.title("🧠 LangGraph-Powered Research Assistant")

# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'selected_paper' not in st.session_state:
    st.session_state.selected_paper = None
if 'summarizing' not in st.session_state:
    st.session_state.summarizing = False

# Sidebar API keys input
st.sidebar.header("🔑 Enter Your API Keys")
serpapi_key = st.sidebar.text_input("SERP API Key", type="password")
openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
firecrawl_key = st.sidebar.text_input("Firecrawl API Key", type="password")

# Debug section
st.sidebar.header("🐛 Debug")
debug_mode = st.sidebar.checkbox("Enable Debug Mode")

if debug_mode:
    st.sidebar.write("API Keys Status:")
    st.sidebar.write("- SERP API:", "✅" if serpapi_key else "❌")
    st.sidebar.write("- OpenAI API:", "✅" if openai_key else "❌")
    st.sidebar.write("- Firecrawl API:", "✅" if firecrawl_key else "❌")

if not all([serpapi_key, openai_key, firecrawl_key]):
    st.warning("⚠️ Please enter all API keys in the sidebar to use the tool.")
    st.stop()

# Set OpenAI API key (compatible with older versions)
openai.api_key = openai_key

# Test API connections
if st.sidebar.button("🧪 Test API Connections"):
    st.sidebar.info("Testing connections...")
    
    # Test OpenAI (using older API format)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        st.sidebar.success("✅ OpenAI connected")
    except Exception as e:
        st.sidebar.error(f"❌ OpenAI failed: {str(e)[:100]}...")
    
    # Test Firecrawl
    try:
        firecrawl = FirecrawlApp(api_key=firecrawl_key)
        st.sidebar.success("✅ Firecrawl initialized")
    except Exception as e:
        st.sidebar.error(f"❌ Firecrawl failed: {str(e)[:100]}...")

def clean_filename(title):
    return re.sub(r'[^a-zA-Z0-9_]', '_', title.strip())

def generate_pdf(title, summary_text, source_link, user_query):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=16, spaceAfter=20)
    metadata_style = ParagraphStyle('Metadata', parent=styles['Normal'], fontSize=9, spaceAfter=6, alignment=TA_JUSTIFY)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, alignment=TA_JUSTIFY, spaceAfter=12)
    story = []
    story.append(Paragraph("Research Summary Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", metadata_style))
    story.append(Paragraph(f"Search Query: {user_query}", metadata_style))
    story.append(Paragraph(f"Source URL: {source_link}", metadata_style))
    story.append(Paragraph(f"Document Title: {title}", metadata_style))
    story.append(Spacer(1, 20))

    for line in summary_text.split('\n'):
        line = line.strip()
        if line.startswith('**') and line.endswith('**'):
            heading = line.strip('*').strip()
            story.append(Paragraph(heading, styles['Heading2']))
        elif line:
            formatted_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            formatted_line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', formatted_line)
            story.append(Paragraph(formatted_line, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def summarize_paper(paper_data, query):
    """Function to summarize a single paper"""
    title = paper_data.get("title", "No title")
    link = paper_data.get("link", "No link")
    
    try:
        # Step 1: Initialize
        st.info("🚀 **Starting summarization process...**")
        
        # Step 2: Initialize Firecrawl
        st.info("🌐 **Step 1/3:** Initializing web crawler...")
        firecrawl = FirecrawlApp(api_key=firecrawl_key)
        
        # Step 3: Crawl content
        st.info("🌐 **Step 2/3:** Crawling article content (this may take 30-60 seconds)...")
        
        try:
            # Try with basic parameters that should work
            response = firecrawl.scrape_url(url=link)
        except Exception as crawl_error:
            st.warning(f"Firecrawl method failed: {str(crawl_error)[:100]}...")
            st.info("🔄 Trying basic URL fetch...")
            try:
                import requests
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                resp = requests.get(link, headers=headers, timeout=30)
                response = {'content': resp.text}
            except Exception as requests_error:
                st.error(f"All crawling methods failed. Requests error: {str(requests_error)[:100]}...")
                return None

        # Extract content
        content = ""
        if isinstance(response, dict):
            content = (response.get('content') or 
                     response.get('markdown') or 
                     response.get('text') or str(response))
        else:
            content = str(response)

        st.success(f"✅ Content crawled successfully! ({len(content)} characters)")
        
        if debug_mode:
            st.text_area("Crawled Content Preview:", value=content[:500] + "...", height=150)
        
        if len(content.strip()) < 100:
            st.error("❌ Content too short for summarization")
            st.text_area("Full content:", content, height=200)
            return None

        # Step 4: Generate summary
        st.info("🤖 **Step 3/3:** Generating AI summary...")
        
        system_prompt = """You are a research assistant. Summarize this academic paper with the following structure:

**Title**
[Paper title]

**Authors** 
[Authors if available]

**Abstract Summary**
[Brief summary of the abstract]

**Key Findings**
[Main findings and results]

**Methodology**
[Research methods used]

**Conclusions**
[Main conclusions]

Keep it concise but comprehensive."""

        try:
            # Using older OpenAI API format
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.3,
                max_tokens=2000,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Summarize this paper:\n\n{content[:6000]}"}
                ],
            )
            summary = response.choices[0].message["content"]
            
            st.success("✅ **Summary generated successfully!**")
            
            # Display summary
            st.markdown("---")
            st.markdown("## 📋 **Generated Summary**")
            st.markdown(summary)
            
            # Generate PDF download
            try:
                pdf_bytes = generate_pdf(title, summary, link, query)
                st.download_button(
                    "📑 Download Summary as PDF",
                    pdf_bytes,
                    file_name=f"{clean_filename(title)}.pdf",
                    mime="application/pdf",
                    key=f"download_pdf_{hash(link)}"
                )
            except Exception as pdf_error:
                st.warning(f"PDF generation failed: {pdf_error}")
            
            return summary
            
        except Exception as openai_error:
            st.error(f"❌ OpenAI API Error: {str(openai_error)}")
            return None

    except Exception as e:
        st.error(f"❌ Process failed: {str(e)}")
        if debug_mode:
            import traceback
            st.code(traceback.format_exc())
        return None

# Main interface
query = st.text_input("🔍 Enter your research query:")
engine = st.selectbox("Select search source:", ["Google Scholar", "Semantic Scholar", "arXiv"])

# Search Papers
if query:
    if st.button("🚀 Search Papers", type="primary"):
        try:
            with st.spinner("🔍 Searching papers..."):
                search_params = {
                    "api_key": serpapi_key,
                    "engine": engine.lower().replace(" ", "_"),
                    "q": query,
                    "num": 10,
                    "hl": "en"
                }
                
                if debug_mode:
                    st.write("Search Parameters:", search_params)
                
                search = GoogleSearch(search_params)
                search_results = search.get_dict()
                
                if debug_mode:
                    st.write("API Response Keys:", list(search_results.keys()))
                
                results = search_results.get("organic_results", [])
                if not results:
                    results = search_results.get("results", [])
                
                if not results:
                    st.warning("No results found.")
                    if debug_mode:
                        st.json(search_results)
                    st.stop()
                
                # Store results in session state
                st.session_state.search_results = results
                # Reset selection states
                st.session_state.selected_paper = None
                st.session_state.summarizing = False
                
        except Exception as e:
            st.error(f"Search failed: {str(e)}")
            if debug_mode:
                import traceback
                st.code(traceback.format_exc())
            st.stop()

# Display search results with individual buttons
if st.session_state.search_results:
    st.subheader(f"📚 Search Results ({len(st.session_state.search_results)} papers found)")
    st.markdown("*Click on any paper below to summarize it:*")
    
    for i, res in enumerate(st.session_state.search_results):
        title = res.get("title", "No title")
        link = res.get("link", "No link")
        snippet = res.get("snippet", "")
        
        # Create a container for each paper
        with st.container():
            st.markdown("---")
            
            # Paper info
            st.markdown(f"### 📄 Paper #{i+1}")
            st.markdown(f"**Title:** {title}")
            st.markdown(f"**Link:** {link}")
            st.markdown(f"**Snippet:** {snippet[:200]}{'...' if len(snippet) > 200 else ''}")
            
            # Button for this specific paper
            button_key = f"summarize_paper_{i}"
            if st.button(f"🤖 Summarize This Paper", key=button_key, type="secondary"):
                st.session_state.selected_paper = i
                st.session_state.summarizing = True
                st.rerun()

# Handle summarization when a paper is selected
if st.session_state.selected_paper is not None and st.session_state.summarizing:
    paper_index = st.session_state.selected_paper
    selected_paper = st.session_state.search_results[paper_index]
    
    st.markdown("---")
    st.markdown(f"## 🔄 Processing Paper #{paper_index + 1}")
    st.markdown(f"**Title:** {selected_paper.get('title', 'No title')}")
    
    # Run summarization
    summary = summarize_paper(selected_paper, query)
    
    # Reset state after processing
    st.session_state.selected_paper = None
    st.session_state.summarizing = False

# Initial message
if not st.session_state.search_results:
    st.info("👆 Enter a research query above and click 'Search Papers' to get started!")