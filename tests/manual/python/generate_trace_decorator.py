import os
from langfuse.decorators import observe, langfuse_context

@observe()
def my_test_function():
    print("Inside traced function")
    return "Hello world"

print("Running traced function...")
my_test_function()

print("Flushing...")
langfuse_context.flush()
print("Done!")
