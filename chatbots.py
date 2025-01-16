import os
import openai
from sentence_transformers import SentenceTransformer
import pandas as pd

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure the API key is set in the environment variables

# Load the model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load datasets
data_files = ['data/dataset.csv', 'data/train.csv']
mental_health_data = pd.concat([pd.read_csv(file) for file in data_files if os.path.exists(file)])
mental_health_data.dropna(subset=['Context', 'Response'], inplace=True)
mental_health_data.drop_duplicates(subset=['Context'], inplace=True)

# Precompute embeddings
mental_health_data['Context_Embedding'] = mental_health_data['Context'].apply(
    lambda x: model.encode(x, convert_to_tensor=True)
)

def generate_response(persona, query):
    persona_prompts = {
        "Abby": "You are Abby, a friendly and empathetic friend.",
        "Katherine": "You are Katherine, a mental health counselor.",
        "Alex": "You are Alex, a financial expert."
    }

    # Fetch the prompt for the persona
    prompt = persona_prompts.get(persona, f"You are a helpful assistant.\nQuery: {query}")

    try:
        # Use the correct method for generating a chat completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Ensure you are using a valid model
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message['content'].strip()

    except Exception as e:
        return f"Error: {e}"

def abby_chat(query):
    return generate_response("Abby", query)

def katherine_chat(query):
    return generate_response("Katherine", query)

def alex_chat(query):
    return generate_response("Alex", query)
