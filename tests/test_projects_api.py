

def test_list_all_projects_should_return_nothing(client, auth):
    """Check if all projects are listed"""
    client.get("/projects")