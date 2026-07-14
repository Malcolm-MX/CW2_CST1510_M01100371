import streamlit as st
from groq import Groq
from app_model.db import connect_database
from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.it_tickets import get_all_it_tickets
from app_model.metadatas import get_all_datasets_metadata

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning("Please log in to access this page.")
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    st.stop()

st.title("Chat with Groq AI")

conn = connect_database()
cyber_data = get_all_cyber_incidents(conn)
tickets_data = get_all_it_tickets(conn)
metadata_data = get_all_datasets_metadata(conn)

severity_counts = cyber_data['severity'].value_counts().to_dict()
category_counts = cyber_data['category'].value_counts().to_dict()
status_counts = tickets_data['status'].value_counts().to_dict()
priority_counts = tickets_data['priority'].value_counts().to_dict()
dataset_names = metadata_data['name'].tolist()

SYSTEM_PROMPT = f"""You are an analyst assistant embedded in a Multi Domain
Intelligence Platform dashboard. You help the user understand three datasets:
cyber incidents, IT tickets, and dataset metadata.

Cyber Incidents summary:
- Total incidents: {len(cyber_data)}
- By severity: {severity_counts}
- By category: {category_counts}

IT Tickets summary:
- Total tickets: {len(tickets_data)}
- By status: {status_counts}
- By priority: {priority_counts}

Metadata summary:
- Registered datasets: {dataset_names}

Only answer questions about the cyber incidents, IT tickets, and
dataset metadata described above. This is a strict rule that you must follow please.
If the user asks about anything unrelated to these three datasets — including
general knowledge, weather, current events, or any other unrelated topic,
you must refuse and respond with exactly: "I can only answer questions about
the data, such as anything about the Cyber Incidents, IT Tickets or Metadata. Use
ChatGPT or Gemini or any other AI for unrelated questions." Do not answer
the off-topic question in any way, even partially, even if you know the answer."""

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for message in st.session_state.messages[1:]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("Ask about any of the datasets...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=st.session_state.messages
    )

    reply = completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

with st.sidebar:
    st.divider()
    if st.button ("Log Out"):
        st.session_state["logged_in"] = False
        st.switch_page("Home.py")