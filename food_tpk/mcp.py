from fastmcp import FastMCP
from .food_tpk import get_food

mcp = FastMCP("Food TPK in Karlsruhe - MCP Server")

@mcp.tool
def get_food_mcp() -> str:
    """
    Get the current week's food menu for the Technologiepark Karlsruhe (TPK) mensa
    known as Joel's Cantina as markdown table.
    """
    return get_food()

def main():
    mcp.run(transport="http", host="127.0.0.1", port=13374)

if __name__ == "__main__":
    main()
