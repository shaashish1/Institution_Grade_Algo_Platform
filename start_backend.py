"""
Backend Startup Script
Starts the FastAPI backend server with proper Python path configuration
"""

import sys
import os

# Add project root and api directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.join(project_root, 'api')
sys.path.insert(0, project_root)
sys.path.insert(0, api_dir)

# Now import and run uvicorn
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Institution Grade Algo Trading Platform API")
    print("=" * 60)
    print(f"📁 Project Root: {project_root}")
    print(f"📁 API Directory: {api_dir}")
    print(f"🌐 Server URL: http://localhost:8000")
    print(f"📖 API Docs: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
