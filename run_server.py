import os
import sys
import uvicorn

if __name__ == "__main__":
    # Ensure current directory is in sys.path
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(curr_dir, ".."))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    if curr_dir not in sys.path:
        sys.path.insert(0, curr_dir)

    print("==================================================================")
    print("  RESCUE-X: 3D Flood Intelligence & Evacuation Decision System   ")
    print("  Data Science with Python Value Added Course Project            ")
    print("==================================================================")
    print("Starting FastAPI Backend + Stitch UI Frontend on http://127.0.0.1:8000")
    print("Open your browser and navigate to: http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server.\n")

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

