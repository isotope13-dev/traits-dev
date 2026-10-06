"""Transpiler stdlib template control: maps DSL calls to emitted Python
snippets. The __import__ calls below are quoted template text produced by
register_lib_call lambdas, never executed by this file.
"""
from ..registry import register_lib, register_lib_call


def register():
    register_lib("pickle", None)

    register_lib_call("pickle", "dumps",
        lambda a: f"__import__('pickle').dumps({a[0]})")

    register_lib_call("pickle", "to_base64",
        lambda a: f"__import__('base64').b64encode(__import__('pickle').dumps({a[0]}))")

    register_lib_call("pickle", "compress",
        lambda a: f"__import__('zlib').compress(__import__('pickle').dumps({a[0]}))")
