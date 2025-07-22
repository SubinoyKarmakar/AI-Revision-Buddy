import streamlit as st
import requests
import os

# Secure API key access
if "openrouter_api_key" in st.secrets:
    OPENROUTER_API_KEY = st.secrets["openrouter_api_key"]
else:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "YOUR_API_KEY_HERE")

# Simulated ChromaDB using a dictionary
chromadb_sim = {}

# Get explanation from OpenRouter
def get_topic_explanation(subject, topic):
    prompt = f"Explain the topic '{topic}' in '{subject}' in simple terms for student revision."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "🚫 Error: " + response.json().get("error", {}).get("message", "Something went wrong.")
    except Exception as e:
        return f"🚫 Exception occurred: {str(e)}"

# Simulate saving to ChromaDB
def mark_as_revised(subject, topic):
    key = f"{subject.lower()}-{topic.lower()}"
    chromadb_sim[key] = True

# Simulate LangChain memory
def already_revised(subject, topic):
    key = f"{subject.lower()}-{topic.lower()}"
    return chromadb_sim.get(key, False)

# Streamlit UI
st.title("🤖 AI Revision Buddy")
st.markdown("Let's start revising your topics!")

subject = st.text_input("Enter Subject")
topic = st.text_input("Enter Topic")

if st.button("Get Revision Notes"):
    if subject and topic:
        if already_revised(subject, topic):
            st.warning("⚠️ You’ve already revised this topic. Try another one.")
        else:
            with st.spinner("⏳ Fetching revision notes..."):
                explanation = get_topic_explanation(subject, topic)
            st.success("✅ Fetch completed!")
            st.subheader("📘 Revision Notes:")
            st.write(explanation)
            mark_as_revised(subject, topic)
    else:
        st.error("❌ Please enter both subject and topic.")
