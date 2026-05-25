from typing import Dict, List
from openai import OpenAI
import os

    # TODO: Define system prompt
    # TODO: Set context in messages
    # TODO: Add chat history
    # TODO: Creaet OpenAI Client
    # TODO: Send request to OpenAI
    # TODO: Return response


def generate_response(openai_key: str, user_message: str, context: str, 
                     conversation_history: List[Dict], model: str = "gpt-3.5-turbo") -> str:
    """Generate response using OpenAI with context"""

    client = OpenAI(api_key=openai_key,
                base_url="https://openai.vocareum.com/v1")

    chat_history = []

    system_prompt = '''You are a NASA mission intelligence assistant for a retrieval-augmented generation system.
    Instructions:
    - Use the provided context as your main evidence.
    - Answer only with information supported by the context unless the user explicitly asks for general knowledge.
    - If the answer is not in the context, say that the retrieved documents do not provide enough information.
    - Do not invent facts or sources.
    - If multiple sources disagree, mention the disagreement briefly.
    - Keep the response concise but complete enough to answer the question.
    - Start with the direct answer, then include short supporting details.
    '''

     # Adding system prompt on top of the history
    chat_history.append({"role": "system", "content": system_prompt})

    chat_history.extend(conversation_history)
    
    if context:
        user_message = f'''{user_message}
        
        given the context:
        {context}
        '''        
    
    chat_history.append({"role":"user", "content":user_message})
    
    response = client.chat.completions.create(
        messages = chat_history,
        model=model,
        max_tokens=512
    )

    generated_response = response.choices[0].message.content

    return generated_response


# User for local testing
if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY_VOC")
    x = generate_response(
        api_key,
        "Hi, this is Sami, do you know what I like this most?",
        "Sami loves fishes, and reads in the morning",
        []
    )
    print(x)