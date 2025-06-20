import asana
from datetime import datetime, timedelta
import pandas as pd
from collections import defaultdict
import requests
import urllib3
from config import Config

# Disable SSL warnings and verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AsanaService:
    def __init__(self):
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
    
    def get_all_tasks(self, workspace_gid, project_gid=None):
        """
        Fetch all tasks from a workspace or specific project
        """
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
        """
        Calculate duration for each completed task and group by assignee
        """
        assignee_durations = defaultdict(list)
        task_details = []

        for task in tasks:
            # Skip incomplete tasks
            if not task.get('completed') or not task.get('completed_at'):
                continue

            # Skip tasks without assignee
            if not task.get('assignee'):
                continue

            try:
                # Parse dates
                created_at = datetime.fromisoformat(task['created_at'].replace('Z', '+00:00'))
                completed_at = datetime.fromisoformat(task['completed_at'].replace('Z', '+00:00'))

                # Calculate duration in days
                duration_days = (completed_at - created_at).days

                # Get assignee info
                assignee_name = task['assignee'].get('name', 'Unknown')
                assignee_email = task['assignee'].get('email', '')

                # Store duration by assignee
                assignee_key = f"{assignee_name} ({assignee_email})" if assignee_email else assignee_name
                assignee_durations[assignee_key].append(duration_days)

                # Store task details
                task_details.append({
                    'task_name': task['name'],
                    'assignee': assignee_key,
                    'created_at': created_at.isoformat(),
                    'completed_at': completed_at.isoformat(),
                    'duration_days': duration_days
                })
            except Exception as e:
                print(f"Error processing task {task.get('name', 'Unknown')}: {e}")
                continue

        return assignee_durations, task_details
    
    def calculate_averages(self, assignee_durations):
        """
        Calculate average duration per assignee
        """
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
    
    def get_all_projects(self, workspace_gid):
        """
        Get all projects in a workspace
        """
        projects = []
        opts = {
            'workspace': workspace_gid,
            'opt_fields': 'name,gid'
        }

        try:
            result = self.projects_api.get_projects(opts)
            for project in result:
                projects.append(project)
        except Exception as e:
            print(f"Error fetching projects: {e}")

        return projects
    
    def get_project_data(self):
        """
        Get project data for the configured project
        """
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
            
            return {
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
            
        except Exception as e:
            print(f"Error in get_project_data: {e}")
            raise e
    
    def get_workspace_data(self):
        """
        Get data from all projects in the workspace
        """
        try:
            # Get workspaces
            print("Fetching workspaces...")
            workspaces_list = []
            opts = {'opt_fields': 'name,gid'}

            try:
                result = self.workspaces_api.get_workspaces(opts)
                for workspace in result:
                    workspaces_list.append(workspace)
            except Exception as e:
                print(f"Error fetching workspaces: {e}")
                print("\nTroubleshooting tips:")
                print("1. Make sure you've replaced the access token with your actual token")
                print("2. Ensure your token has the necessary permissions")
                print("3. Check if the token is still valid (not expired)")
                raise e

            if not workspaces_list:
                print("No workspaces found!")
                return None

            # Display available workspaces
            print("\nAvailable workspaces:")
            for i, ws in enumerate(workspaces_list):
                print(f"{i+1}. {ws['name']} (ID: {ws['gid']})")

            # Use first workspace by default
            workspace = workspaces_list[0]
            workspace_gid = workspace['gid']
            print(f"\nUsing workspace: {workspace['name']}")

            # Get all projects in workspace
            print("\nFetching all projects...")
            projects = self.get_all_projects(workspace_gid)
            print(f"Found {len(projects)} projects")

            all_tasks = []

            # Fetch tasks from each project
            for i, project in enumerate(projects, 1):
                print(f"{i}/{len(projects)} Fetching tasks from project: {project['name']}")
                project_tasks = self.get_all_tasks(workspace_gid, project['gid'])
                all_tasks.extend(project_tasks)
                print(f"  Found {len(project_tasks)} tasks")

            print(f"\nTotal tasks found: {len(all_tasks)}")
            
            # Calculate durations
            assignee_durations, task_details = self.calculate_task_durations(all_tasks)
            
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
            
            return {
                'project': {
                    'name': f'All Projects in {workspace["name"]}',
                    'workspace_name': workspace['name'],
                    'gid': workspace['gid']
                },
                'total_tasks': len(all_tasks),
                'completed_tasks': len(task_details),
                'assignee_stats': assignee_stats,
                'task_details': task_details
            }
            
        except Exception as e:
            print(f"Error in get_workspace_data: {e}")
            raise e 