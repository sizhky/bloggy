#!/usr/bin/env python3
"""
Extract chapters from Flatland input.md into separate markdown files.
"""

import re
from pathlib import Path

def clean_markdown(text):
    """Clean up markdown content by removing HTML tags and formatting."""
    # Remove HTML tags like {=html}, <hgroup>, </hgroup>, etc.
    text = re.sub(r'```\{=html\}', '', text)
    text = re.sub(r'```', '', text)
    text = re.sub(r'<hgroup>', '', text)
    text = re.sub(r'</hgroup>', '', text)
    text = re.sub(r'\[\]\{[^}]+\}', '', text)  # Remove empty link anchors
    text = re.sub(r':::.+?:::', '', text, flags=re.DOTALL)  # Remove div blocks
    
    # Clean up HTML entities in inline code
    text = re.sub(r'`<abbr[^>]*>`\{=html\}([^`]+?)`</abbr>`\{=html\}', r'\1', text)
    text = re.sub(r'`<abbr>`\{=html\}', '', text)
    text = re.sub(r'`</abbr>`\{=html\}', '', text)
    
    # Fix figure paths
    text = re.sub(r'\(\.\/illustration-(\d+)\.svg\)', r'(figures/illustration-\1.svg)', text)
    
    # Remove image attributes in curly braces
    text = re.sub(r'\{#illustration-\d+[^}]+\}', '', text)
    
    # Clean up excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def extract_chapter_title(content):
    """Extract chapter title from content."""
    # Look for pattern like "### I" followed by a title
    match = re.search(r'###\s+([IVXLCDM]+)\n\n(.+?)(?:\n\n|$)', content)
    if match:
        chapter_num = match.group(1)
        title = match.group(2).strip()
        return f"Chapter {chapter_num}: {title}"
    return None

def split_chapters(input_file):
    """Read input file and split into chapters."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all chapter markers
    # Pattern: []{#chapter-X.xhtml} followed by ### X
    chapter_pattern = r'\[\]\{#chapter-(\d+)\.xhtml\}.*?(?=\[\]\{#chapter-\d+\.xhtml\}|\[\]\{#endnotes\.xhtml\}|$)'
    
    chapters = re.findall(chapter_pattern, content, re.DOTALL)
    
    # Manually split by chapter markers for better control
    parts = re.split(r'\[\]\{#chapter-(\d+)\.xhtml\}', content)
    
    chapter_data = []
    for i in range(1, len(parts), 2):
        if i+1 < len(parts):
            chapter_num = parts[i]
            chapter_content = parts[i+1]
            
            # Extract until next chapter or endnotes
            next_chapter_pos = chapter_content.find('[]{#chapter-')
            endnotes_pos = chapter_content.find('[]{#endnotes.xhtml}')
            
            if next_chapter_pos > 0:
                chapter_content = chapter_content[:next_chapter_pos]
            elif endnotes_pos > 0:
                chapter_content = chapter_content[:endnotes_pos]
            
            chapter_data.append((chapter_num, chapter_content))
    
    return chapter_data

def process_chapter(chapter_num, content):
    """Process individual chapter content."""
    # Clean the content
    content = clean_markdown(content)
    
    # Extract title
    title_match = re.search(r'###\s+([IVXLCDM]+)\s*\n\n(.+?)(?:\n\n|$)', content)
    if title_match:
        roman_num = title_match.group(1)
        title = title_match.group(2).strip()
        
        # Remove the chapter header from content (we'll add our own)
        content = re.sub(r'###\s+[IVXLCDM]+\s*\n\n.+?\n\n', '', content, count=1)
        
        # Create new formatted content
        formatted_content = f"# {title}\n\n{content}"
        return formatted_content
    
    return content

def main():
    input_file = Path(__file__).parent / 'input.md'
    output_dir = Path(__file__).parent
    
    print(f"Reading from: {input_file}")
    
    # Split into chapters
    chapters = split_chapters(input_file)
    
    print(f"Found {len(chapters)} chapters")
    
    # Process each chapter
    for chapter_num, content in chapters:
        # Process content
        processed_content = process_chapter(chapter_num, content)
        
        # Create filename
        filename = f"chapter-{int(chapter_num):02d}.md"
        output_path = output_dir / filename
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        print(f"Created: {filename}")
    
    print("\n✓ All chapters extracted successfully!")

if __name__ == '__main__':
    main()
