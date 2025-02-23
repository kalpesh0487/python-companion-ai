from flask import Blueprint, request, jsonify
from models import Companion, Message
from database import db
from datetime import datetime
import os
import requests
import json

chat_bp = Blueprint('chat', __name__)

class MemoryManager:
    @staticmethod
    def read_latest_history(companion_key):
        messages = Message.query.filter_by(
            companion_id=companion_key['companion_id']
        ).order_by(Message.created_at.desc()).limit(10).all()
        return "\n".join([f"{'User: ' if msg.role == 'user' else ''}{msg.content}" for msg in messages])

    @staticmethod
    def seed_chat_history(seed, separator, companion_key):
        new_message = Message(
            content=seed,
            companion_id=companion_key['companion_id'],
            role="system"
        )
        db.session.add(new_message)
        db.session.commit()

    @staticmethod
    def write_to_history(content, companion_key, role="system"):
        new_message = Message(
            content=content,
            companion_id=companion_key['companion_id'],
            role=role
        )
        db.session.add(new_message)
        db.session.commit()

@chat_bp.route('/api/chat/<string:chat_id>', methods=['POST'])
def chat(chat_id):
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Get the companion
        companion = Companion.query.get_or_404(chat_id)
        
        # Create a new message for the user's prompt
        user_message = Message(
            content=prompt,
            companion_id=chat_id,
            role="user"
        )
        db.session.add(user_message)
        db.session.commit()

        name = companion.name
        companion_key = {
            "companion_id": chat_id,
            "modelName": "llama2-13b"
        }

        memory_manager = MemoryManager()
        
        # Get chat history
        recent_chat_history = memory_manager.read_latest_history(companion_key)
        print(recent_chat_history)

        # If no history, seed it
        if not recent_chat_history:
            memory_manager.seed_chat_history(companion.seed, "\n\n", companion_key)
            recent_chat_history = memory_manager.read_latest_history(companion_key)

        # Prepare the message for the Groq API
        messages = [
            {
                "role": "system",
                "content": f"""You are {name}. {companion.instructions}
                You should respond naturally without prefixing who is speaking.
                Include emotions when appropriate but don't overuse them.
                Use the chat history for context but focus on answering the current question."""
            },
            {
                "role": "system",
                "content": f"Recent conversation history:\n{recent_chat_history}"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        # Make request to Groq API
        headers = {
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={
                "model": "mixtral-8x7b-32768",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            }
        )

        if response.status_code != 200:
            return jsonify({"error": "Failed to get response from Groq API"}), 500

        response_data = response.json()
        assistant_message = response_data['choices'][0]['message']['content'].strip()

        # Save the response to history
        memory_manager.write_to_history(assistant_message, companion_key)

        return jsonify({
            "response": assistant_message,
            "companionId": chat_id
        })

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500
