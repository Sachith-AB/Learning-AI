import json

def process_posts(raw_file_path, process_file_path="data/processed_posts.json"):
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
    for post in posts:
        metadata = extract_metadatas(post['text'])


def extract_metadatas(post):
    return {
        'line_count': 10,
        'problem': '',
        'solution': ''
        
    }


if __name__  == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")