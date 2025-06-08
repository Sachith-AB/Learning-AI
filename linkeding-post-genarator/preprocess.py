import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

def process_posts(raw_file_path, process_file_path="data/processed_posts.json"):
    details_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
    for post in posts:
        metadata = extract_metadata(post['text'])
        post_with_metadata = post | metadata
        details_posts.append(post_with_metadata)
    
    langs = get_all_languages(details_posts)
    for lang in langs:
        print(lang)


def get_all_languages(posts):
    languages = set()
    for post in posts:
        if 'tech_stack' in post:
            for category in ['front_end', 'back_end', 'additional']:
                if category in post['tech_stack']:
                    languages.update(post['tech_stack'][category])
    
    template = '''You are a technology recommender. For the given technologies:
    {languages}
    
    Return a JSON object with:
    - "frontend_recommendations": Array of suggested frontend technologies
    - "backend_recommendations": Array of suggested backend technologies
    - "database_recommendations": Array of suggested databases
    - "architecture_recommendations": Array of suggested architectures
    
    Return ONLY valid JSON, no additional text. Example:
    {{
        "frontend_recommendations": [...],
        "backend_recommendations": [...]
    }}'''
    
    pt = PromptTemplate.from_template(template)
    chain = pt | llm | JsonOutputParser()
    
    try:
        return chain.invoke({'languages': list(languages)})
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        return {}

def extract_metadata(post):
    template = '''
        You are given linkedin post about software projects. You need to extract number of lines,
        problem that solve from that software and what is the solution given from that software.
        Need json object with 3 keys called line_count, problem and solution.
        no preamble need
        Here is the actual post on with you need to perform that task:
        {post}
    '''
    
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post': post})
    
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs")
    
    return res


if __name__  == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")