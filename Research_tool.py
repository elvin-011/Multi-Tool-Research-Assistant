import os
import uuid
import streamlit as st
import langgraph as lg
from dotenv import load_dotenv, find_dotenv
import asyncio
from phi.tools.firecrawl import FirecrawlTools
# from firecrawl import AsyncFirecrawlApp
# from firecrawl import ScrapeOptions
import openai


# from langgraph import Node, Flow, run_flow
from serpapi import GoogleSearch
st.set_page_config(
    page_title="Hello",
    layout="wide",
)

st.title("Research Tool")
class SearchEngine:
    def user_input(self):
        query = st.text_input("Enter your search query",placeholder= "Name of the paper or topic")
        engine=st.multiselect("Select Search Engine", options=["Google Scholar", "Semantic Scholar", "arXiv"], default=["Google Scholar"])
        return query,engine

    def search(self, query, engine):
        serp_api=os.getenv("SERPAPI_KEY")
        if not serp_api:
            st.error("Please set the SERPAPI_KEY environment variable.")
            return None
        
        params = {
            "api_key": serp_api,
            "engine": engine[0].lower().replace(" ", "_"),  # Convert engine name to lowercase and replace spaces with underscores
            "num": 10,  # Number of results to return
            "q": query,
            "hl": "en"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        return results
    
    def display_results(self, results):
        for idx, result in enumerate(results.get("organic_results", [])):
            title = result.get("title", "No title")
            link = result.get("link", "No link")
            snippet = result.get("snippet", "No snippet")

            st.write(f"### {title}")
            st.write(f"🔗 [Link]({link})")
            st.write(f"📝 {snippet}")

            button_key = f"summary_button_{idx}"

            if st.button("Generate Summary", key=button_key):
                st.session_state["clicked_summary"] = {
                    "index": idx,
                    "title": title,
                    "link": link
                }
            st.write("---")
            
        if "clicked_summary" in st.session_state:
            selected = st.session_state["clicked_summary"]
            st.info(f"🔄 Generating summary for: {selected['title']}")
            return selected['link']
        else:
            st.info("Click 'Generate Summary' to get a summary of a result.")
    async def crawl(self,link):
        # Placeholder for crawling logic
        st.write(f"Crawling the link: {link}")
        firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        app = AsyncFirecrawlApp(api_key=firecrawl_api_key)
        response = await app.crawl_url(
            url=link,
            limit= 10,
            scrape_options = ScrapeOptions(
                formats= [ 'markdown' ],
                onlyMainContent= True,
                parsePDF= True,
                maxAge= 14400000
            )
        )
        return response
    def summarize(self, text):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
        model="gpt-4.1",  # or gpt-4 if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes academic research articles."},
            {"role": "user", "content": f"Summarize the following research article:\n\n{text}"}
        ],
        temperature=0.5,
        max_tokens=800  # limit to keep summary concise
        
    )
        return response.choices[0].message['content']
        
if __name__ == "__main__":
    load_dotenv(find_dotenv())
    search_engine = SearchEngine()
    
    query, engine = search_engine.user_input()
    
    if query and engine:
        results = search_engine.search(query, engine)
        if results:
            search_engine.display_results(results)
        else:
            st.error("No results found. Please try a different query or engine.")
 