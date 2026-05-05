from mcp.server.fastmcp import FastMCP
from datebase.crud import add_task

## три сущности: prompt, resource, tools

mcp = FastMCP('Demo')

@mcp.tool()
def tool_add_task(name, dateinsert, datefinish, status):
    """ add task in bd """
    add_task(name, dateinsert, datefinish, status)
    return "Ok!"

#@mcp.resource()
#def func():
#    pass
 
if __name__ == "__main__":
    mcp.run(transport="stdio")