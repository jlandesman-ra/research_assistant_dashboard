import asana
from datetime import datetime, timedelta
import pandas as pd
from collections import defaultdict
from config import Config
import json
import os
import time
import ssl
import urllib3

# Disable SSL warnings and verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CachedAsanaService:
    def __init__(self):
        self.cache_file = 'asana_cache.json'
        self.cache_duration = 24 * 60 * 60  # 24 hours in seconds
        
        # Initialize Asana client with working configuration
        # You'll need to get your personal access token from:
        # https://app.asana.com/0/my-apps
        ASANA_ACCESS_TOKEN = '2/1209642836801514/1210056798486740:cd38597d2fdb5a951348cbd4709855cb'
        
        # Configure client
        configuration = asana.Configuration()
        configuration.access_token = ASANA_ACCESS_TOKEN
        configuration.timeout = 30  # 30 second timeout
        
        # Disable SSL verification to avoid certificate issues
        configuration.verify_ssl = False
        
        self.api_client = asana.ApiClient(configuration)
        
        # Create API instances
        self.workspaces_api = asana.WorkspacesApi(self.api_client)
        self.projects_api = asana.ProjectsApi(self.api_client)
        self.tasks_api = asana.TasksApi(self.api_client)
    
    def is_cache_valid(self):
        """Check if cache exists and is still valid"""
        if not os.path.exists(self.cache_file):
            return False
        
        try:
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is older than 24 hours
            cache_time = cache_data.get('timestamp', 0)
            current_time = time.time()
            
            return (current_time - cache_time) < self.cache_duration
        except:
            return False
    
    def save_cache(self, data):
        """Save data to cache file"""
        cache_data = {
            'timestamp': time.time(),
            'data': data
        }
        
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            print(f"Data cached successfully at {datetime.now()}")
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def load_cache(self):
        """Load data from cache file"""
        try:
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
            return cache_data.get('data')
        except Exception as e:
            print(f"Error loading cache: {e}")
            return None
    
    def get_all_tasks(self, workspace_gid, project_gid=None):
        """Fetch all tasks from a workspace or specific project"""
        tasks = []
        opts = {
            'opt_fields': 'name,assignee,assignee.name,assignee.email,created_at,completed_at,completed'
        }
        
        try:
            if project_gid:
                # Get tasks from specific project
                opts['project'] = project_gid
                result = self.tasks_api.get_tasks_for_project(project_gid, opts)
                for task in result:
                    tasks.append(task)
            else:
                # Get all tasks from workspace
                opts['workspace'] = workspace_gid
                result = self.tasks_api.get_tasks(opts)
                for task in result:
                    tasks.append(task)
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            raise e
        
        return tasks
    
    def calculate_task_durations(self, tasks):
        """Calculate duration for each task and group by assignee"""
        assignee_durations = defaultdict(list)
        task_details = []
        
        for task in tasks:
            # Skip tasks without assignee
            if not task.get('assignee'):
                continue
            
            try:
                # Parse created date
                created_at = datetime.fromisoformat(task['created_at'].replace('Z', '+00:00'))
                
                # Get assignee info
                assignee_name = task['assignee'].get('name', 'Unknown')
                assignee_email = task['assignee'].get('email', '')
                
                # Store duration by assignee (only for completed tasks)
                assignee_key = f"{assignee_name} ({assignee_email})" if assignee_email else assignee_name
                
                # Check if task is completed
                is_completed = task.get('completed', False)
                completed_at = None
                duration_days = None
                
                if is_completed and task.get('completed_at'):
                    # Parse completed date
                    completed_at = datetime.fromisoformat(task['completed_at'].replace('Z', '+00:00'))
                    # Calculate duration in days
                    duration_hours = (completed_at - created_at).total_seconds() / 3600
                    duration_days = duration_hours / 24
                    # Store duration by assignee (only for completed tasks)
                    assignee_durations[assignee_key].append(duration_days)
                
                # Store task details (both completed and open tasks)
                task_details.append({
                    'task_name': task['name'],
                    'assignee': assignee_key,
                    'created_at': created_at.isoformat(),
                    'completed_at': completed_at.isoformat() if completed_at else None,
                    'duration_days': duration_days,
                    'completed': is_completed
                })
            except Exception as e:
                print(f"Error processing task {task.get('name', 'Unknown')}: {e}")
                continue
        
        return assignee_durations, task_details
    
    def calculate_averages(self, assignee_durations):
        """Calculate average duration per assignee"""
        averages = {}
        
        for assignee, durations in assignee_durations.items():
            if durations:
                avg_duration = sum(durations) / len(durations)
                averages[assignee] = {
                    'average_days': round(avg_duration, 2),
                    'total_tasks': len(durations),
                    'min_days': min(durations),
                    'max_days': max(durations),
                    'total_days': sum(durations)
                }
        
        return averages
    
    def fetch_live_data(self):
        """Fetch fresh data from Asana"""
        print("Fetching fresh data from Asana...")
        
        try:
            # Get project details
            opts = {'opt_fields': 'name,workspace,workspace.name'}
            project = self.projects_api.get_project(Config.PROJECT_GID, opts)
            workspace_gid = project['workspace']['gid']
            
            # Fetch tasks from the specific project
            all_tasks = self.get_all_tasks(workspace_gid, Config.PROJECT_GID)
            
            # Calculate durations
            assignee_durations, task_details = self.calculate_task_durations(all_tasks)
            
            if not task_details:
                return {
                    'project': project,
                    'total_tasks': len(all_tasks),
                    'completed_tasks': 0,
                    'assignee_stats': [],
                    'task_details': []
                }
            
            # Calculate averages
            averages = self.calculate_averages(assignee_durations)
            
            # Format data for API response
            assignee_stats = []
            for assignee, stats in averages.items():
                assignee_stats.append({
                    'assignee': assignee,
                    'average_days': stats['average_days'],
                    'total_tasks': stats['total_tasks'],
                    'min_days': stats['min_days'],
                    'max_days': stats['max_days'],
                    'total_days': stats['total_days']
                })
            
            # Sort by average days (descending)
            assignee_stats.sort(key=lambda x: x['average_days'], reverse=True)
            
            data = {
                'project': {
                    'name': project['name'],
                    'workspace_name': project['workspace']['name'],
                    'gid': project['gid']
                },
                'total_tasks': len(all_tasks),
                'completed_tasks': len(task_details),
                'assignee_stats': assignee_stats,
                'task_details': task_details
            }
            
            # Save to cache
            self.save_cache(data)
            return data
            
        except Exception as e:
            print(f"Error fetching live data: {e}")
            raise e
    
    def get_project_data(self, force_refresh=False):
        """Get project data from cache or fetch fresh data"""
        # Check if cache is valid (unless force refresh is requested)
        if not force_refresh and self.is_cache_valid():
            print("Loading data from cache...")
            cached_data = self.load_cache()
            if cached_data:
                return cached_data
        
        # Cache is invalid, doesn't exist, or force refresh requested
        try:
            return self.fetch_live_data()
        except Exception as e:
            print(f"Failed to fetch live data: {e}")
            # Try to load stale cache as fallback
            cached_data = self.load_cache()
            if cached_data:
                print("Using stale cache as fallback...")
                return cached_data
            else:
                # Return empty data if everything fails
                return {
                    'project': {
                        'name': 'Project Unavailable',
                        'workspace_name': 'Unknown',
                        'gid': Config.PROJECT_GID
                    },
                    'total_tasks': 0,
                    'completed_tasks': 0,
                    'assignee_stats': [],
                    'task_details': []
                }
    
    def get_cache_timestamp(self):
        """Get the timestamp of the current cache"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                return cache_data.get('timestamp', 0)
            return None
        except Exception as e:
            print(f"Error getting cache timestamp: {e}")
            return None 