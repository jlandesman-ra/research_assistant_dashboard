#!/usr/bin/env python3
"""
Startup script for the Asana Task Analytics Dashboard
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Set default port
    port = int(os.environ.get('PORT', 5000))
    
    # Set debug mode based on environment
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🚀 Starting Asana Task Analytics Dashboard...")
    print(f"📊 Dashboard will be available at: http://localhost:{port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug
        )
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        sys.exit(1) 