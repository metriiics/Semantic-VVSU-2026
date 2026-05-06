from mcp.server.fastmcp import FastMCP
from datebase.crud import DBaseQuery

## три сущности: prompt, resource, tools

mcp = FastMCP('Demo')

# @mcp.tool()
# def tool_create_task(name, dateinsert, datefinish, status):
#    """ create task in bd """
#    DBaseQuery.create_task(name, dateinsert, datefinish, status)
#    return "Ok!"

@mcp.tool()
def tool_read_task():
    """ read task in bd """
    tasks = DBaseQuery.read_task()
    return tasks

#@mcp.resource()
#def func():
#    pass
 
if __name__ == "__main__":
    mcp.run(transport="stdio")