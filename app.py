import gradio as gr
import random
def update(name):
    return f"Welcome to Gradio, {name}!"

with gr.Blocks() as demo:
    gr.Markdown("# Movie information assistant\n### Using LLM RAG System to generate Cypher Query for Neo4j Database.")
    with gr.Row(10):
        with gr.Column(5):
            chatbot = gr.Chatbot()
            msg = gr.Textbox(label="Question", placeholder="Ask me about movies and I will provide you with the information you need.")

            def respond(message, chat_history):
                bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
                chat_history.append((message, bot_message))
                return "", chat_history

            msg.submit(respond, [msg, chatbot], [msg, chatbot])
        with gr.Column(2):
            with gr.Row(2):
                cypher_query = gr.Textbox(label="Cypher Query", lines=7)
            with gr.Row(2):
                query_results = gr.Textbox(label="Query Results", lines=10)

    with gr.Row(1):
        clear = gr.ClearButton([msg, chatbot])

    #     inp = gr.Textbox(placeholder="What is your name?")
    #     out = gr.Textbox()
    # btn = gr.Button("Run")
    # btn.click(fn=update, inputs=inp, outputs=out)

demo.launch()