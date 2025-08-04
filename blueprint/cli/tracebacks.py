"""Traceback printing."""

import bdb

import click
import jsonschema
import rich_click
from rich.traceback import install as rich_tracebacks

rich_tracebacks(
   show_locals=True,
   suppress=[
       bdb,
       click,
       jsonschema,
       rich_click,
   ]
)
