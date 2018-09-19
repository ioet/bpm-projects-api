from bpm_projects_api import create_app

app = create_app()
print("Running BPM Projects API")
app.run(host='0.0.0.0', port=8000)
