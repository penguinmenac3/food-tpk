import sys
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
    mode = "stdio"
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    if mode == "http":
        mcp.run(transport="http", host="127.0.0.1", port=13374)
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
