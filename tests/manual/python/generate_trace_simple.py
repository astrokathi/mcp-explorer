import os
from langfuse import Langfuse

print("Initializing Langfuse...")
langfuse = Langfuse()

print("Creating trace...")
trace = langfuse.trace(name="test-trace-direct", session_id="test-session-1")
trace.span(name="test-span", input="hello", output="world")

print("Flushing Langfuse...")
langfuse.flush()
print("Done!")
