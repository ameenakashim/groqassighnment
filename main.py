import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor

class Character(BaseModel):
    name: str
    fact: List[str] = Field(..., description="A list of facts about the subject")

def query_groq_api(client, question):
    resp = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        response_model=Character,
    )
    return resp.model_dump_json(indent=2)

def main():
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("GROQ_API_KEY environment variable is not set.")
        return

    client = Groq(api_key=api_key)
    client = instructor.from_groq(client, mode=instructor.Mode.JSON)

    print("Welcome to the Groq API Question-Answer System!")
    print("Type 'quit' to exit the system.")

    while True:
        question = input("Ask your question: ")
        
        if question.lower() == 'quit':
            print("Exiting the system. Goodbye!")
            break
        
        response = query_groq_api(client, question)
        print(response)

if __name__ == "__main__":
    main()
    