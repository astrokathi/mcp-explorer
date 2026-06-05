import asyncio
from langfuse.langchain import CallbackHandler
from langchain_core.runnables import RunnableLambda
import os
import time

async def main():
    print("Initializing Langfuse Callback...")
    langfuse_handler = CallbackHandler()
    
    print("Initializing Chain...")
    chain = RunnableLambda(lambda x: "Hello, " + x)
    
    print("Invoking Chain...")
    try:
        response = await chain.ainvoke(
            "world",
            config={"callbacks": [langfuse_handler]}
        )
        print(f"Chain responded: {response}")
    except Exception as e:
        print(f"Chain error: {e}")
        
    print("Waiting 5 seconds for background flush...")
    time.sleep(5)
    print("Done!")

asyncio.run(main())
