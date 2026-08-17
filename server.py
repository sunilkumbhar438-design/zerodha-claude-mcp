import os
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from kiteconnect import KiteConnect

mcp = FastMCP(
    "Zerodha",
    stateless_http=True,
    json_response=True
)

def kite():
    api_key = os.environ["KITE_API_KEY"]
    access_token = os.environ["KITE_ACCESS_TOKEN"]
    return KiteConnect(api_key=api_key, access_token=access_token)

@mcp.tool()
def get_ltp(instrument: str) -> dict:
    """Get the latest price. Example: NSE:INFY or NSE:NIFTY 50."""
    return kite().ltp(instrument)

@mcp.tool()
def get_positions() -> dict:
    """Get current Zerodha positions."""
    return kite().positions()

@mcp.tool()
def get_holdings() -> list:
    """Get Zerodha equity holdings."""
    return kite().holdings()

@mcp.tool()
def get_orders() -> list:
    """Get today's Zerodha orders."""
    return kite().orders()

@mcp.tool()
def get_margins() -> dict:
    """Get available Zerodha margins."""
    return kite().margins()

app = FastAPI()
app.mount("/", mcp.streamable_http_app())

@app.get("/health")
def health():
    return {"status": "ok"}
