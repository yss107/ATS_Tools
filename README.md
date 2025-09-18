# Resume ATS Tool

A comprehensive tool for analyzing and optimizing resumes for Applicant Tracking Systems (ATS). This tool helps job seekers improve their resume's compatibility with ATS software used by employers to screen applications.

## Features

- **Multi-format Support**: Analyze PDF, DOCX, and TXT resume files
- **ATS Compatibility Scoring**: Get a score from 0-100 based on ATS best practices
- **Keyword Analysis**: Identify technical skills, soft skills, and industry keywords
- **Formatting Checks**: Detect ATS-unfriendly formatting issues
- **Personalized Recommendations**: Get specific suggestions to improve your resume
- **Command Line Interface**: Easy-to-use CLI with various options
- **JSON Export**: Save analysis results for further processing

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yss107/classic.git
cd classic
```

2. Run the setup script:
```bash
./setup.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Web Interface (Recommended)
1. Install Flask: `pip install flask` (or use requirements.txt)
2. Start the web server:
```bash
source venv/bin/activate
python web_app.py
```
3. Open your browser to `http://localhost:5000`
4. Upload your resume and get instant analysis!

### Command Line Interface
```bash
# Activate virtual environment
source venv/bin/activate

# Analyze a resume
python resume_ats.py sample_resume.txt
```

### Advanced Usage
```bash
# Analyze with specific keywords
python resume_ats.py resume.pdf --keywords python javascript react aws

# Save analysis to JSON file
python resume_ats.py resume.docx --output analysis.json

# Use multiple options
python resume_ats.py resume.pdf -k python -k docker -k kubernetes -o results.json -v
```

### Command Line Options
- `resume_file`: Path to the resume file (required)
- `--keywords, -k`: Additional keywords to check for (can be used multiple times)
- `--output, -o`: Save analysis results to JSON file
- `--verbose, -v`: Enable verbose output

## What the Tool Analyzes

### 1. ATS Compatibility Score (0-100)
- **80-100**: Excellent ATS compatibility
- **60-79**: Good compatibility with minor improvements needed
- **0-59**: Needs significant improvements

### 2. Keyword Analysis
- **Technical Skills**: Programming languages, frameworks, tools
- **Soft Skills**: Leadership, communication, teamwork
- **Business Skills**: Project management, strategic planning
- **Certifications**: Professional certifications and credentials

### 3. Formatting Checks
- Standard resume sections (Experience, Education, Skills)
- Contact information (email, phone)
- Date ranges for experience
- ATS-friendly formatting

### 4. Recommendations
- Specific suggestions for improvement
- Industry best practices
- ATS optimization tips

## Sample Output

```
=== Resume ATS Analysis ===
File: sample_resume.txt
Word Count: 387

ATS Compatibility Score: 85/100

Keywords Found:
  Technical Skills: python, javascript, react, node.js, sql, postgresql, mongodb, aws, docker, kubernetes, git, github, ci/cd, machine learning, tensorflow, pytorch, pandas, numpy, scikit-learn
  Soft Skills: leadership, communication, teamwork, analytical
  Business Skills: project management, agile, scrum
  Certifications: aws certified, scrum master

Recommendations:
  1. Use standard section headings (Experience, Education, Skills)
  2. Avoid tables, graphics, and complex formatting
  3. Use standard fonts (Arial, Calibri, Times New Roman)
  4. Save as both .docx and .pdf formats
  5. Include relevant keywords from job descriptions
```

## File Format Support

### Supported Formats
- **PDF**: `.pdf` files
- **Microsoft Word**: `.docx` files  
- **Plain Text**: `.txt` files

### Tips for Different Formats
- **PDF**: Ensure text is selectable (not image-based)
- **DOCX**: Use standard formatting, avoid complex layouts
- **TXT**: Simple format that works well with all ATS systems

## Best Practices for ATS-Friendly Resumes

1. **Use Standard Section Headers**
   - Experience / Work Experience
   - Education
   - Skills / Technical Skills
   - Summary / Professional Summary

2. **Include Relevant Keywords**
   - Use keywords from job descriptions
   - Include both spelled-out and abbreviated terms (e.g., "Search Engine Optimization (SEO)")

3. **Formatting Guidelines**
   - Use standard fonts (Arial, Calibri, Times New Roman)
   - Avoid tables, text boxes, and graphics
   - Use bullet points instead of special characters
   - Keep formatting simple and consistent

4. **Contact Information**
   - Include full name, phone number, email, and location
   - Use a professional email address
   - Add LinkedIn profile URL

5. **File Format**
   - Submit both .docx and .pdf versions when possible
   - Name files professionally (e.g., "FirstName_LastName_Resume.pdf")

## Development

### Running Tests
```bash
# Test with sample resume
python resume_ats.py sample_resume.txt

# Test with different file formats
python resume_ats.py resume.pdf
python resume_ats.py resume.docx
```

### Adding New Keywords
Edit the `keywords_database` in `resume_ats.py` to add industry-specific keywords.

## Dependencies

- `python-docx`: For reading DOCX files
- `PyPDF2`: For reading PDF files
- `textstat`: For readability analysis
- `nltk`: For text processing
- `click`: For command line interface
- `colorama`: For colored output

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please open an issue on GitHub or contact the maintainers.