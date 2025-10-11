from google.adk.agents import Agent
import yfinance as yf
import datetime
from dotenv import load_dotenv
load_dotenv()

def get_stock_price(ticker:str)-> dict:
    """Fetches the stock price for a given ticker symbol."""

    print(f"Fetching stock price for {ticker}")

    try:
        stock = yf.Ticker(ticker)
        current_price = stock.info.get("currentPrice")

        if current_price is None:
            return {
                "Statsus": "Failed",
                "error": "Could not fetch current price."
                } 
        current_time = datetime.datetime.now().isoformat()

        return {
            "Status": "Success",
            "ticker": ticker,
            "current_price": current_price,
            "timestamp": current_time
        }
        
    except Exception as e:
        print(f"Error fetching stock price for {ticker}: {str(e)}")
        return {"error": str(e)}

stock_analyst = Agent(
    name="Stock_Analyst",
    model="gemini-2.0-flash",
    description="An agent that helps users track stock prices.",
    instruction="""
    You are a helpful stock market assistant that helps users track their stocks of interest.
    
    When asked about stock prices:
    1. Use the get_stock_price tool to fetch the latest price for the requested stock(s)
    2. Format the response to show each stock's current price and the time it was fetched
    3. If a stock price couldn't be fetched, mention this in your response
    
    Example response format:
    "Here are the current prices for your stocks:
    - GOOG: $175.34 (updated at 2024-04-21 16:30:00)
    - TSLA: $156.78 (updated at 2024-04-21 16:30:00)
    - META: $123.45 (updated at 2024-04-21 16:30:00)"
    """,
    tools=[get_stock_price]
)