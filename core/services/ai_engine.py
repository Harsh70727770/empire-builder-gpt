from .gemini_service import generate_response

def generate_startup_plan(idea):
    prompt = f"""
    You are a professional startup consultant.

    Convert the idea into a structured startup plan.

    Idea: {idea}

    Format the response EXACTLY like this:

    ## Problem
    (Explain problem clearly)

    ## Solution
    (Explain solution)

    ## Target Audience
    (Who will use it)

    ## Revenue Model
    (How it will earn)

    ## Unique Selling Point
    (Why it's different)

    Keep it clean and professional.
    """
    return generate_response(prompt)


def generate_idea_score(idea):
    prompt = f"""
    Analyze this startup idea and give a score:

    Idea: {idea}

    Return:
    Market Demand (0-10)
    Competition Level (0-10)
    Profit Potential (0-10)
    Overall Score (0-100)

    Also explain briefly.
    """
    return generate_response(prompt)


def generate_roadmap(idea):
    prompt = f"""
    Create a 30-day execution roadmap for this startup idea:

    Idea: {idea}

    Include:
    Week 1
    Week 2
    Week 3
    Week 4

    Keep it practical and actionable.
    """
    return generate_response(prompt)


def generate_tech_stack(idea):
    prompt = f"""
    Suggest the best tech stack for this startup:

    Idea: {idea}

    Include:
    Frontend
    Backend
    Database
    APIs
    Deployment

    Keep it modern and scalable.
    """
    return generate_response(prompt)


# NEW OPTIMIZED FUNCTION (MAIN FIX)
def generate_full_startup(idea):
    prompt = f"""
    You are a professional startup consultant.
    
    Analyze this idea: {idea}
    
    Give response EXACTLY in this format:
    
    ## Startup Plan
    (Include Problem, Solution, Target Audience, Revenue Model, USP)
    
    ## Idea Score
    Market Demand (0-10)
    Competition Level (0-10)
    Profit Potential (0-10)
    Overall Score (0-100)
    
    ## Roadmap
    Week 1
    Week 2
    Week 3
    Week 4
    
    ## Tech Stack
    Frontend
    Backend
    Database
    APIs
    Deployment
    
    Keep it clean and structured.
    """
    return generate_response(prompt)