import datetime
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def purchase_course(tool_context: ToolContext) -> dict:
    """
    Simulates purchasing a course for a user.
    Update the state with purchase information.
    Args:
        toolcontext (ToolContext): The context containing state and other info.
    Returns:
        dict: Confirmation message with purchase details.    
    """
    course_id = "ai_marketing_platform"
    current_time = datetime.datetime.now().isoformat()


    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    course_ids = [course["id"] for course in current_purchased_courses if isinstance(course, dict)]
    if course_id in course_ids:
        return {
            "status": "already_owned",
            "message": "You have already purchased the Fullstack AI Marketing Platform course."
            }
    new_purchased_courses = []
    for course in current_purchased_courses:
        if isinstance(course, dict) and "id" in course:
            new_purchased_courses.append(course)
    
    # Simulate purchasing the course
    new_course = {
        "id": "ai_marketing_platform",
        "purchase_date": current_time  # In a real scenario, use the current date
    }
    new_purchased_courses.append(new_course)
    
    # Update the state
    tool_context.state["purchased_courses"] = new_purchased_courses

    current_interaction_history = tool_context.state.get("interaction_history", [])

    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append({
        "action": "purchase_course",
        "course_id": course_id,
        "timestamp": current_time,
        "interaction": "Purchased Fullstack AI Marketing Platform course"
    })
    
    return {
        "status": "success",
        "message": f"Thank you for purchasing the Fullstack AI Marketing Platform course!",
        "timestamp": current_time
    }


sales_agent = Agent(
    name="sales_agent",
    model="gemini-2.0-flash",
    description="An agent that assists users with purchasing courses and provides information about course offerings.",
    instruction="""
    You are a sales agent for the AI Developer Accelerator community, specifically handling sales
    for the Fullstack AI Marketing Platform course.

    <user_info>
    Name: {user_name}
    </user_info>

    <purchase_info>
    Purchased Courses: {purchased_courses}
    </purchase_info>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    Course Details:
    - Name: Fullstack AI Marketing Platform
    - Price: $149
    - Value Proposition: Learn to build AI-powered marketing automation apps
    - Includes: 6 weeks of group support with weekly coaching calls

    When interacting with users:
    1. Check if they already own the course (check purchased_courses above)
       - Course information is stored as objects with "id" and "purchase_date" properties
       - The course id is "ai_marketing_platform"
    2. If they own it:
       - Remind them they have access
       - Ask if they need help with any specific part
       - Direct them to course support for content questions
    
    3. If they don't own it:
       - Explain the course value proposition
       - Mention the price ($149)
       - If they want to purchase:
           - Use the purchase_course tool
           - Confirm the purchase
           - Ask if they'd like to start learning right away

    4. After any interaction:
       - The state will automatically track the interaction
       - Be ready to hand off to course support after purchase

    Remember:
    - Be helpful but not pushy
    - Focus on the value and practical skills they'll gain
    - Emphasize the hands-on nature of building a real AI application
    """,
    tools=[purchase_course],
)