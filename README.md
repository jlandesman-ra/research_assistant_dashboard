# Asana Task Analytics Dashboard

A Flask-based dashboard that displays task completion analytics from Asana projects. The dashboard shows task duration statistics by assignee, including averages, totals, and detailed task information.

## Features

- **Live Asana Integration**: Pulls real data from your Asana projects
- **Cached Data System**: Pulls data once per day and caches it locally for fast loading
- **Interactive Charts**: Bar charts and doughnut charts showing task completion analytics
- **Detailed Statistics**: Average completion times, total tasks, and performance metrics by assignee
- **Responsive Design**: Modern, mobile-friendly interface
- **Fallback System**: Uses mock data if live data is unavailable

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test Asana Connection

Test that your Asana integration is working:

```bash
python test_asana_connection.py
```

This will verify the connection and show sample data from your project.

### 3. Run the Application

```bash
python run.py
```

The dashboard will be available at `http://localhost:5000`

## Caching System

The application uses a smart caching system to improve performance:

- **Automatic Caching**: Data is fetched once per day and stored locally
- **Fast Loading**: Dashboard loads instantly from cache
- **Manual Refresh**: Use `python refresh_cache.py` to force a data refresh
- **Fallback**: Uses mock data if both live data and cache fail

### Manual Cache Refresh

To manually refresh the data cache:

```bash
python refresh_cache.py
```

This will:
- Fetch fresh data from Asana
- Save it to the local cache
- Show statistics about the fetched data

### Creating Mock Data

To create sample data for testing:

```bash
python create_mock_cache.py
```

This creates a cache file with realistic sample data that the dashboard can use immediately.

## API Endpoints

- `GET /` - Main dashboard page
- `GET /api/project-data` - Project analytics data
- `GET /api/health` - Health check endpoint

## Data Structure

The API returns data in the following format:

```json
{
  "success": true,
  "data": {
    "project": {
      "name": "Project Name",
      "workspace_name": "Workspace Name",
      "gid": "project_gid"
    },
    "total_tasks": 100,
    "completed_tasks": 75,
    "assignee_stats": [
      {
        "assignee": "John Doe (john@example.com)",
        "average_days": 5.2,
        "total_tasks": 15,
        "min_days": 1,
        "max_days": 12,
        "total_days": 78
      }
    ],
    "task_details": [
      {
        "task_name": "Task Name",
        "assignee": "John Doe (john@example.com)",
        "created_at": "2024-01-01T00:00:00",
        "completed_at": "2024-01-05T00:00:00",
        "duration_days": 4
      }
    ]
  }
}
```

## Current Project Data

The dashboard is currently configured to pull data from:
- **Project**: Research Ad-Hoc Tracker
- **Workspace**: RA Capital
- **Total Tasks**: 215
- **Completed Tasks**: 184
- **Team Members**: 12

## Troubleshooting

### Testing Connection

If you encounter issues, test the Asana connection:

```bash
python test_asana_connection.py
```

This will show detailed information about the connection and data retrieval.

### Missing Dependencies

If you get module import errors, install the required packages:

```bash
pip install flask flask-cors asana pandas python-dotenv requests
```

### Cache Issues

If the cache becomes corrupted or outdated:
1. Delete the `asana_cache.json` file
2. Run `python refresh_cache.py` to create a fresh cache
3. Or run `python create_mock_cache.py` for sample data
4. Restart the application

## Development

### Project Structure

```
research_assistant_dashboard/
├── app.py                 # Flask application
├── asana_service.py       # Direct Asana API service
├── cached_asana_service.py # Cached Asana API service
├── mock_asana_service.py  # Mock data service
├── config.py             # Configuration management
├── refresh_cache.py      # Cache refresh script
├── create_mock_cache.py  # Mock cache creation script
├── test_asana_connection.py # Connection test script
├── run.py               # Application entry point
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html      # Dashboard template
└── README.md           # This file
```

### Adding New Features

1. **New Charts**: Add Chart.js configurations in `templates/index.html`
2. **New Metrics**: Extend the data processing in `asana_service.py`
3. **New API Endpoints**: Add routes in `app.py`

## License

This project is for internal use only. 