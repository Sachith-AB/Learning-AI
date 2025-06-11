from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

def generate_linkedin_post(name, problem, solution, tech_stack):
    prompt = f"""
        You are an AI assistant that creates engaging, professional, and impactful LinkedIn posts for tech project showcases.

        Create a LinkedIn post based on the following inputs:
        
        name:
        {name}
        
        Problem:
        {problem}
        
        Solution:
        {solution}

        Tech Stack:
        {', '.join(tech_stack)}
        
        Post Requirements:
        - when name give you add that also
        - Start with a strong intro (e.g., "Introducing", "We're proud to launch", "Excited to present")
        - Mention the problem briefly, then highlight the solution
        - Include the tech stack naturally
        - Use a friendly and inspiring tone
        - Keep it under 100 words if possible

        Now write the LinkedIn post:
    """
    
    pt = PromptTemplate.from_template(prompt)
    chain = pt | llm

    try:
        result = chain.invoke({})
        # If expecting JSON output, parse accordingly
        if isinstance(result, dict) and "post" in result:
            return result["post"]
        elif isinstance(result, str):
            return result.strip()
        else:
            return str(result)
    except OutputParserException as e:
        return f"Error generating post: {e}"
    
    
if __name__ == "__main__":
    name = "musicia"
    problem = "Music event organizers in Sri Lanka struggle with scattered communication and low visibility"
    solution = "A centralized platform for event planning, promotion, and ticketing"
    tech_stack = {
        "front_end": ["HTML", "CSS", "JavaScript"],
        "back_end": ["PHP", "MVC Architecture"],
        "database": ["MySQL"]
    }
    
    post = generate_linkedin_post(name, problem, solution, tech_stack)
    print(post)

