import sys
import traceback

print("hellloooooooooo11")
print("Script started.")
print("Python paths:", sys.path)

try:
    import langgraph
    print("langgraph package location:", langgraph.__file__)
except ImportError as e:
    print("ImportError occurred!")
    traceback.print_exc()

print("Script finished.")
