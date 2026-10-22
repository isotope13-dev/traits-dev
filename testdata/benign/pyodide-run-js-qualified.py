"""Read a browser title through Pyodide's JavaScript bridge."""
import pyodide.code

def title():
    return pyodide.code.run_js("document.title")
