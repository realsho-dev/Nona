import os
from dotenv import load_dotenv
from together import Together

# Load API Key
load_dotenv()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

# Get AI response using Together API
def get_ai_response(prompt, context=""):
    try:
        system_prompt = (
            "You are a helpful Discord bot named coco, created by Ayanokouji. "
            "Reply shortly and clearly using the recent chat context."
        )
        full_prompt = f"{system_prompt}\n\nRecent chat:\n{context}\n\nUser's message: {prompt}"

        response = client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Get last 50 messages, but focus on last 5 from chat and user
async def get_recent_context(channel, user, limit=50):
    try:
        messages = await channel.history(limit=limit).flatten()
        chat_msgs = [msg.content for msg in messages[:50]]
        user_msgs = [msg.content for msg in messages if msg.author == user][:50]
        return "\n".join(chat_msgs + user_msgs)
    except Exception as e:
        print(f"Context error: {e}")
        return ""

# Handle Discord messages
async def handle_discord_message(message, prefix='-ask'):
    if not (message.content.startswith(prefix) or (message.reference and prefix in message.content)):
        return

    user_input = message.content.replace(prefix, '').strip()
    context_msg = ""

    if message.reference:
        try:
            ref = await message.channel.fetch_message(message.reference.message_id)
            context_msg = ref.content
        except:
            pass

    recent_context = await get_recent_context(message.channel, message.author)
    full_context = f"{context_msg}\n{recent_context}".strip()
    reply = get_ai_response(user_input, full_context)
    await message.channel.send(reply)
