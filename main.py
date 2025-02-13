# %%
import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor

class Subject(BaseModel):
    title: str
    details: List[str] = Field(..., description="A list of facts about the topic")

def get_topic_from_user():
    return input("Enter a topic to explore (or 'exit' to quit): ")

def fetch_info(query):
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("Error: GROQ_API_KEY environment variable is not set.")
        return

    groq_client = Groq(api_key=api_key)
    groq_client = instructor.from_groq(groq_client, mode=instructor.Mode.TOOLS)

    response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": f"Tell me about {query}"}],
        response_model=Subject,
    )
    
    print(response.model_dump_json(indent=2))

if __name__ == "__main__":
    while True:
        topic = get_topic_from_user()
        if topic.lower() == 'exit':
            break
        fetch_info(topic)



