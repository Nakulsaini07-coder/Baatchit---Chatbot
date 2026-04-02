from __future__ import annotations
from fastmcp import FastMCP

mcp = FastMCP('arith')

def _as_number(x):
    '''Accept int/floats or numeric strings. raise clean error otherwise'''
    if isinstance(x, (int, float)):
        return x
    if isinstance(x, str):
        try:
            return float(x.strip())
        except ValueError:
            raise TypeError(f"Cannot convert {x} to a number")
    raise TypeError(f"Expected int, float, or numeric string, got {type(x)}")

@mcp.tool
async def add(a: float, b: float) -> float:
    ''' Return a + b'''
    return _as_number(a) + _as_number(b)

@mcp.tool
async def sub(a: float, b: float) -> float:
    ''' Return a - b'''
    return _as_number(a) - _as_number(b)

@mcp.tool
async def mul(a: float, b: float) -> float:
    ''' Return a * b'''
    return _as_number(a) * _as_number(b)

@mcp.tool
async def div(a: float, b: float) -> float:
    ''' Return a / b'''
    denominator = _as_number(b)
    if denominator == 0:
        raise ZeroDivisionError("Division by zero is not allowed")
    return _as_number(a) / denominator

@mcp.tool
async def pow(a: float, b: float) -> float:
    ''' Return a ** b'''
    return _as_number(a) ** _as_number(b)

@mcp.tool
async def modulous(a: float, b: float) -> float:
    ''' Return a % b'''
    denominator = _as_number(b)
    if denominator == 0:
        raise ZeroDivisionError("Modulus by zero is not allowed")
    return _as_number(a) % denominator

if __name__ == "__main__":
    mcp.run()