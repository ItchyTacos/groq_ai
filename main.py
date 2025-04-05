from groq import Groq
from dotenv import load_dotenv
import os
import json
from datetime import datetime


#import API key
load_dotenv("key.env")

client = Groq(
    api_key = os.environ.get("GROQ_API_KEY")
)

#in case I want this in a library for some reason in future projects
def ask_question(question):

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                #plead with God to have some warm social interaction if else its cold :(
                "content": "You are a helpful ai assistant determined to give the most factual and responses to the questions the user asks. Act friendly please :)"
        },
            {
                "role": "user",
                #pop off queen, answer that question
                "content": f"{question}"
        }
        
        ],
        #meta model, 30 RPM 1000 RPD 6000 TPM 100000 TPD
        model="llama-3.3-70b-versatile"
    )

    # Dump response to variable
    response = chat_completion.model_dump()
    response["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Extract content and usage info
    usage = response.get("usage", "No usage info")
    content = response["choices"][0]["message"]["content"]

    # Save the full response in JSON format to the history directory
    with open("history/response_log.json", "w") as f:
        json.dump(response, f, indent=2)

    #return usage and response looking pretty
    return f"usage: {json.dumps(usage, indent=2)} \n\n AI: {content}"


#if running standalone
if __name__ == "__main__":


    while True:

        q = input("You: ")

        if q.lower().strip() in ["exit", "quit"]:
            break
        elif not q:
            print("Please enter a question")
        else:
            #if dont want to leave and isn't blank
            a = ask_question(q)
            print(a)