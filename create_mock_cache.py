#!/usr/bin/env python3
"""
Script to create a mock cache file with sample data
"""

import json
import time
from datetime import datetime, timedelta

def create_mock_cache():
    """Create a mock cache file with sample Asana data"""
    
    # Sample data that matches the expected format
    mock_data = {
        'project': {
            'name': 'Research Assistant Dashboard',
            'workspace_name': 'Development Team',
            'gid': '1209273054819416'
        },
        'total_tasks': 45,
        'completed_tasks': 38,
        'assignee_stats': [
            {
                'assignee': 'John Smith (john.smith@company.com)',
                'average_days': 7.2,
                'total_tasks': 12,
                'min_days': 2,
                'max_days': 15,
                'total_days': 86
            },
            {
                'assignee': 'Sarah Johnson (sarah.j@company.com)',
                'average_days': 5.8,
                'total_tasks': 10,
                'min_days': 1,
                'max_days': 12,
                'total_days': 58
            },
            {
                'assignee': 'Mike Davis (mike.davis@company.com)',
                'average_days': 4.5,
                'total_tasks': 8,
                'min_days': 1,
                'max_days': 8,
                'total_days': 36
            },
            {
                'assignee': 'Lisa Chen (lisa.chen@company.com)',
                'average_days': 6.1,
                'total_tasks': 8,
                'min_days': 2,
                'max_days': 11,
                'total_days': 49
            }
        ],
        'task_details': [
            {
                'task_name': 'Design user interface mockups',
                'assignee': 'John Smith (john.smith@company.com)',
                'created_at': '2024-01-15T09:00:00',
                'completed_at': '2024-01-22T16:30:00',
                'duration_days': 7,
                'completed': True
            },
            {
                'task_name': 'Implement authentication system',
                'assignee': 'Sarah Johnson (sarah.j@company.com)',
                'created_at': '2024-01-10T14:00:00',
                'completed_at': '2024-01-16T11:00:00',
                'duration_days': 6,
                'completed': True
            },
            {
                'task_name': 'Set up database schema',
                'assignee': 'Mike Davis (mike.davis@company.com)',
                'created_at': '2024-01-08T10:00:00',
                'completed_at': '2024-01-12T15:00:00',
                'duration_days': 4,
                'completed': True
            },
            {
                'task_name': 'Create API documentation',
                'assignee': 'Lisa Chen (lisa.chen@company.com)',
                'created_at': '2024-01-20T13:00:00',
                'completed_at': '2024-01-26T17:00:00',
                'duration_days': 6,
                'completed': True
            },
            {
                'task_name': 'Write unit tests',
                'assignee': 'John Smith (john.smith@company.com)',
                'created_at': '2024-01-25T09:00:00',
                'completed_at': '2024-02-02T14:00:00',
                'duration_days': 8,
                'completed': True
            },
            {
                'task_name': 'Review code changes',
                'assignee': 'Sarah Johnson (sarah.j@company.com)',
                'created_at': '2024-06-18T10:00:00',
                'completed_at': None,
                'duration_days': None,
                'completed': False
            },
            {
                'task_name': 'Update deployment scripts',
                'assignee': 'Mike Davis (mike.davis@company.com)',
                'created_at': '2024-06-19T14:00:00',
                'completed_at': None,
                'duration_days': None,
                'completed': False
            },
            {
                'task_name': 'Finalize project documentation',
                'assignee': 'Lisa Chen (lisa.chen@company.com)',
                'created_at': '2024-06-20T09:00:00',
                'completed_at': None,
                'duration_days': None,
                'completed': False
            }
        ]
    }
    
    # Create cache structure
    cache_data = {
        'timestamp': time.time(),
        'data': mock_data
    }
    
    # Save to cache file
    try:
        with open('asana_cache.json', 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        print("✅ Mock cache created successfully!")
        print(f"📊 Project: {mock_data['project']['name']}")
        print(f"📈 Total tasks: {mock_data['total_tasks']}")
        print(f"✅ Completed tasks: {mock_data['completed_tasks']}")
        print(f"👥 Team members: {len(mock_data['assignee_stats'])}")
        print(f"💾 Cache file: asana_cache.json")
        print("\n🚀 The dashboard will now load with this sample data!")
        
    except Exception as e:
        print(f"❌ Error creating mock cache: {e}")

if __name__ == "__main__":
    create_mock_cache() 