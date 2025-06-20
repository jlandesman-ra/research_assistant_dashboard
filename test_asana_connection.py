#!/usr/bin/env python3
"""
Test script to verify Asana connection and data retrieval
"""

from asana_service import AsanaService
import json

def test_asana_connection():
    """Test the Asana connection and data retrieval"""
    
    print("🧪 Testing Asana Connection...")
    
    try:
        # Initialize service
        service = AsanaService()
        
        # Test project data retrieval
        print("📊 Fetching project data...")
        data = service.get_project_data()
        
        print("✅ Connection successful!")
        print(f"📋 Project: {data['project']['name']}")
        print(f"🏢 Workspace: {data['project']['workspace_name']}")
        print(f"📈 Total tasks: {data['total_tasks']}")
        print(f"✅ Completed tasks: {data['completed_tasks']}")
        print(f"👥 Team members: {len(data['assignee_stats'])}")
        
        # Show top performers
        print("\n🏆 Top performers (by average completion time):")
        for i, stat in enumerate(data['assignee_stats'][:5], 1):
            print(f"{i}. {stat['assignee']} - {stat['average_days']} days avg ({stat['total_tasks']} tasks)")
        
        # Show some task details
        print(f"\n📝 Sample tasks ({len(data['task_details'])} total):")
        for i, task in enumerate(data['task_details'][:3], 1):
            print(f"{i}. {task['task_name']} - {task['assignee']} ({task['duration_days']} days)")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_asana_connection()
    if success:
        print("\n🎉 All tests passed! The Asana integration is working correctly.")
    else:
        print("\n💥 Tests failed. Please check your configuration.") 