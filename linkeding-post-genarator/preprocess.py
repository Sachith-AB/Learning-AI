import json

def process_posts(raw_file_path, process_file_path="data/processed_posts.json"):
    details_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
    for post in posts:
        metadata = extract_metadata(post['text'])
        post_with_metadata = post | metadata
        details_posts.append(post_with_metadata)
        
        print(details_posts[0])


def extract_metadata(post):
    return {
        'line_count': 10,
        'problem': 'problem',
        'solution': 'solution'
        
    }


if __name__  == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")