#!/usr/bin/env python3
"""
Script to manually refresh the Asana data cache
"""

from cached_asana_service import CachedAsanaService
import json
import os

def main():
    print("🔄 Refreshing Asana data cache...")
    
    service = CachedAsanaService()
    
    try:
        # Force fetch fresh data
        data = service.fetch_live_data()
        
        print("✅ Cache refreshed successfully!")
        print(f"📊 Project: {data['project']['name']}")
        print(f"📈 Total tasks: {data['total_tasks']}")
        print(f"✅ Completed tasks: {data['completed_tasks']}")
        print(f"👥 Team members: {len(data['assignee_stats'])}")
        
        # Show cache file info
        if os.path.exists(service.cache_file):
            cache_size = os.path.getsize(service.cache_file)
            print(f"💾 Cache file size: {cache_size} bytes")
        
    except Exception as e:
        print(f"❌ Error refreshing cache: {e}")
        print("💡 The dashboard will use mock data until cache is refreshed.")

if __name__ == "__main__":
    main() 