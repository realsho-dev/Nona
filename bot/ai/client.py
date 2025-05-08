import os
from dotenv import load_dotenv
from together import Together

# Load environment variables
load_dotenv()

# Setup Together API Key
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Initialize Together API client
client = Together(api_key=TOGETHER_API_KEY)

# Function to get response from AI model
def get_ai_response(prompt, context=None):
    try:
        # Predefined information to guide the AI's response
        predefined_info = """
        You are a Discord bot named coco, created by Ayanokouji, You have to help server members by answering their queries in a short and simple way.
        """
        
        # Combine predefined info with the user prompt and context (if any)
        if context:
            full_prompt = f"{predefined_info}\n\nContext (message you're replying to): {context}\n\nUser's question: {prompt}\n\nProvide a simple, clear response considering the context."
        else:
            full_prompt = f"{predefined_info}\n\nUser's message: {prompt}\n\nProvide a simple, clear response."

        # Sending the prompt to the AI model and getting the response
        response = client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=[{"role": "user", "content": full_prompt}]
        )
        
        if response and response.choices:
            return response.choices[0].message.content.strip()
        
        return "Error: No response from AI."
    except Exception as e:
        return f"Error: {str(e)}"

# Function to fetch last 50 messages from the channel and the user
async def fetch_chat_context(channel, user, message_limit=50):
    try:
        # Get the last 50 messages from the channel
        channel_messages = await channel.history(limit=message_limit).flatten()
        chat_history = [msg.content for msg in channel_messages]
        
        # Get the last 50 messages from the user
        user_messages = [msg.content for msg in channel_messages if msg.author == user]
        user_history = user_messages[-message_limit:]  # Only last 50 from the user
        
        # Combine chat history and user history
        context = {
            'chat': "\n".join(chat_history[-message_limit:]),  # Last 50 from the chat
            'user': "\n".join(user_history[-message_limit:])   # Last 50 from the user
        }
        
        return context
    except Exception as e:
        print(f"Error fetching context: {e}")
        return None

# Function to handle Discord message (this would be called from your Discord bot code)
async def handle_discord_message(message, bot_command_prefix='-'):
    # Ignore messages that start with bot's command prefix (like -help, -cmd, etc.)
    if message.content.startswith(bot_command_prefix) and not message.content.startswith('-ask'):
        return
        
    # Check if message starts with -ask or is a reply to another message with -ask
    if message.content.startswith('-ask') or (message.reference and '-ask' in message.content):
        # Get the replied message if exists
        context_message = None
        if message.reference:
            try:
                # Fetch the replied message
                replied_message = await message.channel.fetch_message(message.reference.message_id)
                context_message = replied_message.content
            except:
                pass
        
        # Remove -ask from the prompt
        user_prompt = message.content.replace('-ask', '').strip()

        # Fetch last 50 messages from the channel and the user for context
        context = await fetch_chat_context(message.channel, message.author)
        
        # Prepare the final context by adding the previous chat and user history to the prompt
        if context:
            full_context = f"Last 50 messages in the chat:\n{context['chat']}\n\nLast 50 messages from the user:\n{context['user']}\n\nUser's query: {user_prompt}"
        else:
            full_context = f"User's query: {user_prompt}"

        # Get AI response using the combined context
        response = get_ai_response(user_prompt, full_context)
        
        # Send the response back to Discord
        await message.channel.send(response)
