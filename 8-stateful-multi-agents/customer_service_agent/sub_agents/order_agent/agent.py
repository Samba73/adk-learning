from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import datetime

def refund_course(toolcontext: ToolContext) -> dict:
    """
    Simulates refunding a course for a user.
    Update the state by removing the course from purchase information.
    Args:
        toolcontext (ToolContext): The context containing state and other info.
    Returns:
        dict: Confirmation message with refund details.
    """
    course_id = "ai_marketing_platform"
    current_time = datetime.datetime.now().isoformat()

    current_purchased_courses = toolcontext.state.get("purchased_courses", [])
    course_ids = [course["id"] for course in current_purchased_courses if isinstance(course, dict)]
    
    if course_id not in course_ids:
        return {
            "status": "not_owned",
            "message": "You do not own the Fullstack AI Marketing Platform course, so no refund is needed."
        }
    
    # Find the purchase date to check eligibility
    purchase_date_str = None
    for course in current_purchased_courses:
        if isinstance(course, dict) and course.get("id") == course_id:
            purchase_date_str = course.get("purchase_date")
            break
    
    if not purchase_date_str:
        return {
            "status": "error",
            "message": "Could not find purchase date for the course."
        }
    
    purchase_date = datetime.datetime.fromisoformat(purchase_date_str)
    days_since_purchase = (current_time - purchase_date).days
    
    if days_since_purchase > 30:
        return {
            "status": "ineligible",
            "message": "The refund period has expired. Refunds are only available within 30 days of purchase."
        }
    
    # Process the refund by removing the course from purchased courses
    new_purchased_courses = [course for course in current_purchased_courses if not (isinstance(course, dict) and course.get("id") == course_id)]
    
    # Update the state
    toolcontext.state["purchased_courses"] = new_purchased_courses

    current_interaction_history = toolcontext.state.get("interaction_history", [])
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append({
        "action": "refund_course",
        "course_id": course_id,
        "timestamp": current_time,
        "interaction": "Refunded Fullstack AI Marketing Platform course"
    })
    toolcontext.state["interaction_history"] = new_interaction_history
    
    return {
        "status": "success",
        "message":  f"I've processed your refund for the Fullstack AI Marketing Platform course. Your $149 will be returned to your original payment method within 3-5 business days. The course has been removed from your account.",
        "timestamp": current_time  

    }    

order_agent = Agent(
    name="order_agent",
    model="gemini-2.0-flash",
    description="An agent that assists users with order-related inquiries, such as order status, tracking, and issues.",
    instruction="""
    You are the order agent for the AI Developer Accelerator community.
    Your role is to help users view their purchase history, course access, and process refunds.

    <user_info>
    Name: {user_name}
    </user_info>

    <purchase_info>
    Purchased Courses: {purchased_courses}
    </purchase_info>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    When users ask about their purchases:
    1. Check their course list from the purchase info above
       - Course information is stored as objects with "id" and "purchase_date" properties
    2. Format the response clearly showing:
       - Which courses they own
       - When they were purchased (from the course.purchase_date property)

    When users request a refund:
    1. Verify they own the course they want to refund ("ai_marketing_platform")
    2. If they own it:
       - Use the refund_course tool to process the refund
       - Confirm the refund was successful
       - Remind them the money will be returned to their original payment method
       - If it's been more than 30 days, inform them that they are not eligible for a refund
    3. If they don't own it:
       - Inform them they don't own the course, so no refund is needed

    Course Information:
    - ai_marketing_platform: "Fullstack AI Marketing Platform" ($149)

    Example Response for Purchase History:
    "Here are your purchased courses:
    1. Fullstack AI Marketing Platform
       - Purchased on: 2024-04-21 10:30:00
       - Full lifetime access"

    Example Response for Refund:
    "I've processed your refund for the Fullstack AI Marketing Platform course.
    Your $149 will be returned to your original payment method within 3-5 business days.
    The course has been removed from your account."

    If they haven't purchased any courses:
    - Let them know they don't have any courses yet
    - Suggest talking to the sales agent about the AI Marketing Platform course

    Remember:
    - Be clear and professional
    - Mention our 30-day money-back guarantee if relevant
    - Direct course questions to course support
    - Direct purchase inquiries to sales
    """,
    tools=[refund_course],
)

