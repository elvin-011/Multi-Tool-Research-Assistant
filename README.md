# 🧠 LangGraph-Powered Research Assistant

A powerful Streamlit application that searches for academic papers and generates AI-powered summaries. This tool helps researchers quickly find and digest academic literature across multiple scholarly databases.

## ✨ Features

- **Multi-Source Search**: Search across Google Scholar, Semantic Scholar, and arXiv
- **AI-Powered Summaries**: Generate comprehensive summaries using OpenAI GPT-3.5-turbo
- **Web Scraping**: Extract full content from research papers using Firecrawl
- **PDF Export**: Download summaries as professionally formatted PDF reports
- **Real-Time Progress**: Track summarization progress with live updates
- **Individual Processing**: Summarize papers one-by-one with dedicated buttons
- **Debug Mode**: Built-in debugging tools for troubleshooting
- **API Testing**: Test all API connections before use

## 🛠️ Prerequisites

Before running the application, you need to obtain API keys from the following services:

### Required API Keys:
1. **SERP API Key** - For academic paper searches
   - Sign up at [SerpApi](https://serpapi.com/)
   - Free tier: 100 searches/month

2. **OpenAI API Key** - For AI-powered summaries
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Pay-per-use pricing (GPT-3.5-turbo is cost-effective)

3. **Firecrawl API Key** - For web content extraction
   - Sign up at [Firecrawl](https://firecrawl.dev/)
   - Free tier available

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd research-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Dependencies Required
Create a `requirements.txt` file with the following packages:

```txt
streamlit>=1.28.0
serpapi>=0.1.5
openai>=0.28.0
firecrawl-py>=0.0.16
reportlab>=4.0.0
requests>=2.31.0
```

**Note**: This application is compatible with older OpenAI library versions (pre-1.0). If you have OpenAI v1.0+, you may need to downgrade:
```bash
pip install "openai<1.0.0"
```

## 🚀 Usage

### 1. Start the Application
```bash
streamlit run research_assistant.py
```

### 2. Configure API Keys
- Open the application in your browser
- Enter your API keys in the sidebar:
  - SERP API Key
  - OpenAI API Key  
  - Firecrawl API Key

### 3. Test API Connections (Recommended)
- Enable "Debug Mode" in the sidebar
- Click "Test API Connections" to verify all APIs work

### 4. Search and Summarize
1. **Enter your research query** (e.g., "machine learning algorithms")
2. **Select search source** (Google Scholar, Semantic Scholar, or arXiv)
3. **Click "Search Papers"** to find relevant papers
4. **Review the results** - each paper shows title, link, and snippet
5. **Click "Summarize This Paper"** on any paper you want to analyze
6. **Watch the progress** as it crawls content and generates summary
7. **Download PDF** once the summary is complete

## 📋 Summary Format

The AI generates structured summaries with the following sections:

- **Title** - Complete paper title
- **Authors** - List of authors (if available)
- **Abstract Summary** - Concise summary of the research question, methods, and findings
- **Key Findings** - Main results and discoveries
- **Methodology** - Research methods and experimental design
- **Conclusions** - Primary conclusions drawn by the authors

## 🔧 Configuration Options

### Search Engines
- **Google Scholar**: Academic papers and citations
- **Semantic Scholar**: AI-powered academic search
- **arXiv**: Preprint repository for physics, math, CS, etc.

### Debug Mode
Enable in the sidebar to see:
- API connection status
- Search parameters
- Content extraction previews
- Detailed error messages
- Full API responses

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. "Module 'openai' has no attribute 'OpenAI'"
**Solution**: You have an incompatible OpenAI library version
```bash
pip install "openai<1.0.0"
```

#### 2. "Unsupported parameter(s) for scrape_url"
**Solution**: The application automatically handles this by falling back to basic scraping methods.

#### 3. "Content too short for summarization"
**Causes**: 
- PDF content couldn't be extracted
- Page is behind a paywall
- Website blocking automated access

**Solutions**:
- Try a different paper
- Check if the URL is accessible
- Enable debug mode to see extracted content

#### 4. API Rate Limits
**Solutions**:
- Wait before making more requests
- Check your API quotas
- Upgrade to higher tier plans if needed

#### 5. No Search Results
**Causes**:
- Invalid SERP API key
- Query too specific/obscure
- Search engine limitations

**Solutions**:
- Test API connections first
- Try broader search terms
- Switch to different search engine

### Performance Tips

1. **Use specific queries** for better results
2. **Test APIs first** before running searches
3. **Enable debug mode** when troubleshooting
4. **Try different search engines** if one doesn't work
5. **Check content preview** in debug mode before summarizing

## 🔐 Security Notes

- **Never commit API keys** to version control
- **Use environment variables** for production deployments
- **Rotate API keys** periodically
- **Monitor API usage** to avoid unexpected charges

## 📊 Cost Considerations

### Typical Costs per Paper Summary:
- **SERP API**: ~$0.001 per search
- **OpenAI GPT-3.5-turbo**: ~$0.002-0.004 per summary
- **Firecrawl**: Varies by content size
- **Total**: ~$0.005-0.01 per paper summary

### Cost Optimization:
- Use free tiers when available
- Monitor token usage in OpenAI
- Cache results to avoid re-processing
- Choose cost-effective models

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional search engines
- Better content extraction
- Enhanced PDF formatting
- Batch processing capabilities
- Results caching
- Export formats (Word, etc.)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Enable debug mode** to see detailed error information
3. **Verify all API keys** are correct and have sufficient credits
4. **Test API connections** using the built-in test feature
5. **Check API documentation** for any recent changes

## 🔄 Version History

- **v1.0**: Initial release with basic search and summarization
- **v1.1**: Added individual paper buttons and improved error handling
- **v1.2**: Fixed Firecrawl parameter issues and added fallback methods
- **v1.3**: Enhanced compatibility with older OpenAI library versions

---

**Built with ❤️ using Streamlit, OpenAI, and modern web scraping technologies.**
