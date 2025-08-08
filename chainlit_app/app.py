import chainlit as cl
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.rag import get_answer
@cl.on_chat_start
async def start():
    await cl.Message(content="👋 i m your health and fitness Coach so Ask me any health & fitness question!").send()

@cl.on_message
async def main(message: cl.Message):
    query = message.content
    answer = get_answer(query)
    await cl.Message(content=answer).send()
