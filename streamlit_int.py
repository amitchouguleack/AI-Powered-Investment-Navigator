from finpilot_agent import get_stock_summary, ask_llm
import streamlit as st
from css.markdown import css
from css.sidebar import sidebar
from css.footer import footer

# Page configuration
st.set_page_config(page_title="AI-Powered Investment Navigator")


# Custom CSS for better styling
st.markdown(f'{css()}', unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Main header
st.markdown('<h1 class="main-header">💼 AI-Powered Investment Navigator</h1>',
            unsafe_allow_html=True)


st.markdown("Ask about any stock and get beginner-friendly, risk-aware insights.",
            unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 About")
    st.markdown(f'{sidebar()}', unsafe_allow_html=True)

    st.header("🛠️ Quick Actions")
    if st.button("Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.rerun()

    st.header("💡 Example Queries")
    st.markdown("""
    Try asking:
    - "What's the current price of AAPL?"
    - "Show me analyst recommendations for Tesla"
    - "Give me fundamentals for Microsoft"
    - "Compare GOOGL and META stock performance"
    """)

# Main chat interface
col1, col2 = st.columns([9, 1])

with col1:
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message agent-message">
                <strong>FinPilot:</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(message["content"])

    # Chat input
    user_input = st.chat_input(
        "Ask me about stocks, market analysis, or financial data...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append(
            {"role": "user", "content": user_input})

        # Display user message immediately
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {user_input}
        </div>
        """, unsafe_allow_html=True)

        # Get agent response
        with st.spinner("FinPilot is analyzing..."):
            try:
                summary = get_stock_summary(user_input.upper())
                prompt = f"Here is the data for {user_input.upper()}: {summary}. What do you recommend?"
                agent_response = ask_llm(prompt)

                # Add agent response to chat history
                st.session_state.messages.append(
                    {"role": "agent", "content": agent_response})

                # Display agent response
                st.markdown(f"""
                <div class="chat-message agent-message">
                    <strong>FinPilot:</strong>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(agent_response)

            except Exception as e:
                error_message = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append(
                    {"role": "agent", "content": error_message})

        # Rerun to update the chat display
        st.rerun()

# Footer
st.markdown("---")
st.markdown(f'{footer()}', unsafe_allow_html=True)
