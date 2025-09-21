#!/usr/bin/env python3
"""
Resume ATS Tool - Analyze and optimize resumes for Applicant Tracking Systems
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import docx
import PyPDF2
import textstat
import click
from colorama import init, Fore, Style
import nltk
from collections import Counter

# Initialize colorama for cross-platform colored output
init()

class ResumeATSAnalyzer:
    """Main class for analyzing resumes for ATS compatibility"""
    
    def __init__(self):
        self.keywords_database = self._load_keywords_database()
        self._ensure_nltk_data()
    
    def _ensure_nltk_data(self):
        """Ensure required NLTK data is downloaded"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
    
    def _load_keywords_database(self) -> Dict[str, List[str]]:
        """Load common ATS keywords by category"""
        return {
            "technical_skills": [
                "python", "java", "javascript", "react", "angular", "vue", "node.js",
                "sql", "mysql", "postgresql", "mongodb", "docker", "kubernetes",
                "aws", "azure", "gcp", "git", "github", "gitlab", "ci/cd",
                "machine learning", "data science", "artificial intelligence",
                "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn"
            ],
            "soft_skills": [
                "leadership", "communication", "teamwork", "problem solving",
                "analytical", "creative", "adaptable", "organized", "detail-oriented",
                "time management", "project management", "collaboration"
            ],
            "business_skills": [
                "project management", "agile", "scrum", "budget management",
                "strategic planning", "business analysis", "stakeholder management",
                "process improvement", "change management", "risk management"
            ],
            "certifications": [
                "pmp", "scrum master", "aws certified", "azure certified",
                "google cloud", "cissp", "comptia", "cisco", "microsoft certified"
            ]
        }
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX file: {str(e)}")
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT file: {str(e)}")
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from resume file based on extension"""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.pdf':
            return self.extract_text_from_pdf(str(file_path))
        elif extension == '.docx':
            return self.extract_text_from_docx(str(file_path))
        elif extension == '.txt':
            return self.extract_text_from_txt(str(file_path))
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    def analyze_keywords(self, text: str) -> Dict[str, any]:
        """Analyze keywords in the resume text"""
        text_lower = text.lower()
        found_keywords = {}
        
        for category, keywords in self.keywords_database.items():
            found = []
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    found.append(keyword)
            found_keywords[category] = found
        
        return found_keywords
    
    def check_ats_formatting(self, text: str) -> Dict[str, any]:
        """Check ATS-friendly formatting"""
        issues = []
        suggestions = []
        
        # Check for basic sections
        sections = ['experience', 'education', 'skills', 'summary', 'objective']
        found_sections = []
        
        for section in sections:
            if re.search(rf'\b{section}\b', text, re.IGNORECASE):
                found_sections.append(section)
        
        if len(found_sections) < 3:
            issues.append("Missing standard resume sections")
            suggestions.append("Include sections like Experience, Education, Skills, and Summary")
        
        # Check for contact information
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        
        if not re.search(email_pattern, text):
            issues.append("No email address found")
            suggestions.append("Include a professional email address")
        
        if not re.search(phone_pattern, text):
            issues.append("No phone number found")
            suggestions.append("Include a phone number")
        
        # Check for dates
        date_patterns = [
            r'\b\d{4}\s*[-–]\s*\d{4}\b',  # 2020-2023
            r'\b\d{4}\s*[-–]\s*present\b',  # 2020-present
            r'\b[A-Za-z]+\s+\d{4}\b'  # January 2020
        ]
        
        dates_found = False
        for pattern in date_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                dates_found = True
                break
        
        if not dates_found:
            issues.append("No date ranges found for experience")
            suggestions.append("Include date ranges for work experience and education")
        
        return {
            "issues": issues,
            "suggestions": suggestions,
            "found_sections": found_sections
        }
    
    def calculate_ats_score(self, text: str, job_keywords: List[str] = None) -> Dict[str, any]:
        """Calculate ATS compatibility score"""
        score = 100
        deductions = []
        
        # Analyze formatting
        formatting_analysis = self.check_ats_formatting(text)
        
        # Deduct points for formatting issues
        formatting_deduction = len(formatting_analysis["issues"]) * 10
        score -= formatting_deduction
        if formatting_deduction > 0:
            deductions.append(f"Formatting issues (-{formatting_deduction} points)")
        
        # Analyze keywords
        keyword_analysis = self.analyze_keywords(text)
        total_keywords = sum(len(keywords) for keywords in keyword_analysis.values())
        
        if total_keywords < 10:
            keyword_deduction = (10 - total_keywords) * 2
            score -= keyword_deduction
            deductions.append(f"Insufficient keywords (-{keyword_deduction} points)")
        
        # Check readability
        readability_score = textstat.flesch_reading_ease(text)
        if readability_score < 60:  # Below "standard" level
            readability_deduction = 10
            score -= readability_deduction
            deductions.append(f"Complex readability (-{readability_deduction} points)")
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        return {
            "score": score,
            "deductions": deductions,
            "keyword_count": total_keywords,
            "readability_score": readability_score,
            "formatting_issues": len(formatting_analysis["issues"])
        }
    
    def generate_recommendations(self, text: str, analysis: Dict) -> List[str]:
        """Generate recommendations for improving ATS compatibility"""
        recommendations = []
        
        # Add formatting suggestions
        formatting_analysis = self.check_ats_formatting(text)
        recommendations.extend(formatting_analysis["suggestions"])
        
        # Keyword recommendations
        keyword_analysis = self.analyze_keywords(text)
        for category, keywords in keyword_analysis.items():
            if len(keywords) < 3:
                recommendations.append(f"Add more {category.replace('_', ' ')} keywords")
        
        # Length recommendations
        word_count = len(text.split())
        if word_count < 300:
            recommendations.append("Resume is too short - aim for 400-800 words")
        elif word_count > 1000:
            recommendations.append("Resume is too long - consider condensing to 1-2 pages")
        
        # General ATS tips
        recommendations.extend([
            "Use standard section headings (Experience, Education, Skills)",
            "Avoid tables, graphics, and complex formatting",
            "Use standard fonts (Arial, Calibri, Times New Roman)",
            "Save as both .docx and .pdf formats",
            "Include relevant keywords from job descriptions"
        ])
        
        return recommendations
    
    def analyze_resume(self, file_path: str, job_keywords: List[str] = None) -> Dict[str, any]:
        """Complete resume analysis"""
        try:
            # Extract text
            text = self.extract_text(file_path)
            
            # Perform analysis
            keyword_analysis = self.analyze_keywords(text)
            formatting_analysis = self.check_ats_formatting(text)
            score_analysis = self.calculate_ats_score(text, job_keywords)
            recommendations = self.generate_recommendations(text, score_analysis)
            
            return {
                "file_path": file_path,
                "text_length": len(text),
                "word_count": len(text.split()),
                "keywords": keyword_analysis,
                "formatting": formatting_analysis,
                "score": score_analysis,
                "recommendations": recommendations,
                "success": True
            }
        
        except Exception as e:
            return {
                "file_path": file_path,
                "error": str(e),
                "success": False
            }


def print_analysis_results(analysis: Dict[str, any]):
    """Print formatted analysis results"""
    if not analysis["success"]:
        print(f"{Fore.RED}Error analyzing {analysis['file_path']}: {analysis['error']}{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}=== Resume ATS Analysis ==={Style.RESET_ALL}")
    print(f"File: {analysis['file_path']}")
    print(f"Word Count: {analysis['word_count']}")
    
    # Print ATS Score
    score = analysis["score"]["score"]
    if score >= 80:
        color = Fore.GREEN
    elif score >= 60:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    
    print(f"\n{Fore.CYAN}ATS Compatibility Score: {color}{score}/100{Style.RESET_ALL}")
    
    if analysis["score"]["deductions"]:
        print(f"\n{Fore.YELLOW}Score Deductions:{Style.RESET_ALL}")
        for deduction in analysis["score"]["deductions"]:
            print(f"  • {deduction}")
    
    # Print Keywords Found
    print(f"\n{Fore.CYAN}Keywords Found:{Style.RESET_ALL}")
    for category, keywords in analysis["keywords"].items():
        if keywords:
            print(f"  {category.replace('_', ' ').title()}: {', '.join(keywords)}")
    
    # Print Formatting Issues
    if analysis["formatting"]["issues"]:
        print(f"\n{Fore.RED}Formatting Issues:{Style.RESET_ALL}")
        for issue in analysis["formatting"]["issues"]:
            print(f"  • {issue}")
    
    # Print Recommendations
    print(f"\n{Fore.CYAN}Recommendations:{Style.RESET_ALL}")
    for i, rec in enumerate(analysis["recommendations"][:10], 1):  # Limit to top 10
        print(f"  {i}. {rec}")


@click.command()
@click.argument('resume_file', type=click.Path(exists=True))
@click.option('--keywords', '-k', multiple=True, help='Additional keywords to check for')
@click.option('--output', '-o', type=click.Path(), help='Output analysis to JSON file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(resume_file, keywords, output, verbose):
    """
    Resume ATS Tool - Analyze resumes for ATS compatibility
    
    RESUME_FILE: Path to the resume file (PDF, DOCX, or TXT)
    """
    analyzer = ResumeATSAnalyzer()
    
    # Convert keywords tuple to list
    job_keywords = list(keywords) if keywords else None
    
    print(f"{Fore.CYAN}Analyzing resume: {resume_file}{Style.RESET_ALL}")
    
    # Analyze the resume
    analysis = analyzer.analyze_resume(resume_file, job_keywords)
    
    # Print results
    print_analysis_results(analysis)
    
    # Save to JSON if requested
    if output:
        with open(output, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\n{Fore.GREEN}Analysis saved to: {output}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()