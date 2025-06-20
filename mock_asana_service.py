from datetime import datetime, timedelta
import random

class MockAsanaService:
    def __init__(self):
        self.project_id = '1209273054819416'
    
    def get_project_data(self):
        """
        Return mock project data for testing
        """
        # Generate mock assignee data
        assignees = [
            "John Smith (john.smith@company.com)",
            "Sarah Johnson (sarah.johnson@company.com)",
            "Mike Davis (mike.davis@company.com)",
            "Emily Wilson (emily.wilson@company.com)",
            "David Brown (david.brown@company.com)"
        ]
        
        # Generate mock task details
        task_details = []
        assignee_stats = []
        
        for assignee in assignees:
            # Generate random number of tasks for each assignee
            num_tasks = random.randint(3, 12)
            durations = []
            
            for i in range(num_tasks):
                # Generate random duration between 1 and 30 days
                duration = random.randint(1, 30)
                durations.append(duration)
                
                # Generate task details
                created_date = datetime.now() - timedelta(days=random.randint(30, 90))
                completed_date = created_date + timedelta(days=duration)
                
                task_details.append({
                    'task_name': f"Task {i+1} for {assignee.split(' ')[0]}",
                    'assignee': assignee,
                    'created_at': created_date.isoformat(),
                    'completed_at': completed_date.isoformat(),
                    'duration_days': duration
                })
            
            # Calculate stats for this assignee
            avg_duration = sum(durations) / len(durations)
            assignee_stats.append({
                'assignee': assignee,
                'average_days': round(avg_duration, 2),
                'total_tasks': len(durations),
                'min_days': min(durations),
                'max_days': max(durations),
                'total_days': sum(durations)
            })
        
        # Sort by average days (descending)
        assignee_stats.sort(key=lambda x: x['average_days'], reverse=True)
        
        return {
            'project': {
                'name': 'Sample Research Project',
                'workspace_name': 'Research Team',
                'gid': self.project_id
            },
            'total_tasks': len(task_details),
            'completed_tasks': len(task_details),
            'assignee_stats': assignee_stats,
            'task_details': task_details
        } 