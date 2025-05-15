import os
from dotenv import load_dotenv
from together import Together

# Load API key and initialize Together client
load_dotenv()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

# Get response from Together AI
def get_ai_response(prompt, context=""):
    try:
        system_prompt = (
            "You are a helpful Discord bot named coco, created by Ayanokouji. "
            "You answer shortly and clearly. Use recent messages and user info to personalize your response."
        )
        full_prompt = f"{system_prompt}\n\nRecent context:\n{context}\n\nUser's message: {prompt}"

        response = client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Get recent messages and build context with usernames and user IDs
async def build_context(channel, target_user, limit=50):
    try:
        messages = await channel.history(limit=limit).flatten()

        # Extract last 5 from chat (with author info)
        recent_chat = [
            f"{msg.author.name} ({msg.author.id}): {msg.content}"
            for msg in messages[:5]
        ]

        # Extract last 5 messages from the target user
        user_msgs = [
            f"{msg.author.name} ({msg.author.id}): {msg.content}"
            for msg in messages if msg.author == target_user
        ][:5]

        # If user is active but never used bot, we still gather info
        user_context = "\n".join(user_msgs)
        chat_context = "\n".join(recent_chat)

        return f"User info:\n{target_user.name} ({target_user.id})\n\nUser's past messages:\n{user_context}\n\nRecent chat:\n{chat_context}"
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
            context_msg = f"Replied to: {ref.author.name} - {ref.content}"
        except:
            pass

    user_context = await build_context(message.channel, message.author)
    full_context = f"{context_msg}\n{user_context}".strip()

    reply = get_ai_response(user_input, full_context)
    await message.channel.send(reply)