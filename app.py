import gradio as gr
import random

from module.llm import query_graph

def respond(message, chat_history):
    bot_message, cypher_query_text, query_results_text = query_graph(message)
    chat_history.append((message, bot_message))
    return "", chat_history, cypher_query_text, query_results_text

with gr.Blocks() as demo:
    gr.Markdown("# Movie information assistant\n### Using LLM RAG System to generate Cypher Query for Neo4j Database.")
    with gr.Row(10):
        with gr.Column(5):
            chatbot = gr.Chatbot()
            msg = gr.Textbox(label="Question", placeholder="Ask me about movies and I will provide you with the information you need.")

        with gr.Column(2):
            with gr.Row():
                cypher_query = gr.Textbox(label="Cypher Query", lines=7)
            with gr.Row():
                query_results = gr.Textbox(label="Query Results", lines=10)
        
        msg.submit(respond, [msg, chatbot], [msg, chatbot, cypher_query, query_results])

    with gr.Row(1):
        clear = gr.ClearButton([msg, chatbot, cypher_query, query_results])

demo.launch()