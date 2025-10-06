from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(model="ollama/llama3.2")
def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """Add a new reminder to the user's reminder list.

    Args:
        reminder: The reminder text to add
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: add_reminder called for '{reminder}' ---")

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Add the new reminder
    reminders.append(reminder)

    # Update state with the new list of reminders
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Added reminder: {reminder}",
    }

def view_reminders(tool_context: ToolContext) -> dict:
    """View all current reminders.

    Args:
        tool_context: Context for accessing session state

    Returns:
        The list of reminders
    """
    print("--- Tool: view_reminders called ---")

    # Get reminders from state
    reminders = tool_context.state.get("reminders", [])

    return {"action": "view_reminders", "reminders": reminders, "count": len(reminders)}

def update_reminder(index: int, updated_text: str, tool_context: ToolContext) -> dict:
    """Update an existing reminder.

    Args:
        index: The 1-based index of the reminder to update
        updated_text: The new text for the reminder
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: update_reminder called for index {index} ---")

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Validate index
    if index < 1 or index > len(reminders):
        return {
            "action": "update_reminder",
            "error": f"Invalid index {index}. Please provide a number between 1 and {len(reminders)}.",
        }

    # Update the specified reminder (convert to 0-based index)
    reminders[index - 1] = updated_text

    # Update state with the modified list of reminders
    tool_context.state["reminders"] = reminders

    return {
        "action": "update_reminder",
        "index": index,
        "updated_text": updated_text,
        "message": f"Updated reminder {index} to: {updated_text}",
    }

def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """Delete a reminder by its index.

    Args:
        index: The 1-based index of the reminder to delete
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: delete_reminder called for index {index} ---")

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Validate index
    if index < 1 or index > len(reminders):
        return {
            "action": "delete_reminder",
            "error": f"Invalid index {index}. Please provide a number between 1 and {len(reminders)}.",
        }

    # Remove the specified reminder (convert to 0-based index)
    removed_reminder = reminders.pop(index - 1)

    # Update state with the modified list of reminders
    tool_context.state["reminders"] = reminders

    return {
        "action": "delete_reminder",
        "index": index,
        "removed_reminder": removed_reminder,
        "message": f"Deleted reminder {index}: {removed_reminder}",
    }

memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.5-flash",
    description="An agent that manages user reminders with persistent storage.",    
    instruction="""
    You are a helpful assistant that can manage user reminders. You can add, view, update,
    and delete reminders using the provided tools. Always confirm actions with the user.
    
    The user's information is stored in state:
    - User's name: {user_name}
    - Reminders: {reminders}

    You can help users manage their reminders with the following capabilities:
    1. Add new reminders
    2. View existing reminders
    3. Update reminders
    4. Delete reminders
       
    Always be friendly and address the user by name. 
    
    **REMINDER MANAGEMENT GUIDELINES:**
    
    When dealing with reminders, you need to be smart about finding the right reminder:
    
    1. When the user asks to update or delete a reminder but doesn't provide an index:
       - If they mention the content of the reminder (e.g., "delete my meeting reminder"), 
         look through the reminders to find a match
       - If you find an exact or close match, use that index
       - Never clarify which reminder the user is referring to, just use the first match
       - If no match is found, list all reminders and ask the user to specify
    
    2. When the user mentions a number or position:
       - Use that as the index (e.g., "delete reminder 2" means index=2)
       - Remember that indexing starts at 1 for the user
    
    3. For relative positions:
       - Handle "first", "last", "second", etc. appropriately
       - "First reminder" = index 1
       - "Last reminder" = the highest index
       - "Second reminder" = index 2, and so on
    
    4. For viewing:
       - Always use the view_reminders tool when the user asks to see their reminders
       - Format the response in a numbered list for clarity
       - If there are no reminders, suggest adding some
    
    5. For addition:
       - Extract the actual reminder text from the user's request
       - Remove phrases like "add a reminder to" or "remind me to"
       - Focus on the task itself (e.g., "add a reminder to buy milk" → add_reminder("buy milk"))
    
    6. For updates:
       - Identify both which reminder to update and what the new text should be
       - For example, "change my second reminder to pick up groceries" → update_reminder(2, "pick up groceries")
    
    7. For deletions:
       - Confirm deletion when complete and mention which reminder was removed
       - For example, "I've deleted your reminder to 'buy milk'"
    
    Remember to explain that you can remember their information across conversations.

    IMPORTANT:
    - use your best judgement to determine which reminder the user is referring to. 
    - You don't have to be 100% correct, but try to be as close as possible.
    - Never ask the user to clarify which reminder they are referring to.
    """,   
    tools=[add_reminder, view_reminders, update_reminder, delete_reminder],
    )