import docker
import requests
from tabulate import tabulate

client = docker.from_env()

containers = client.containers.list(all=True)

table_data = []
for container in containers:
    container_name = container.name
    container_image = container.attrs['Config']['Image']
    current_version = "N/A"
    docker_hub_version = "N/A"
    github_registry_version = "N/A"

    if container_image:
        # Get the current version of the local container
        current_version = container.image.tags[0].split(":")[-1] if container.image.tags else "N/A"

        # Get the latest tag of the Docker image on Docker Hub
        docker_hub_url = f"https://registry.hub.docker.com/v1/repositories/{container_image}/tags"
        response = requests.get(docker_hub_url)
        if response.status_code == 200:
            data = response.json()
            tags = [tag for tag in data]
            docker_hub_version = max(tags, default="N/A") if tags else "N/A"

        # Get the latest tag of the Docker image on GitHub Registry
        github_registry_url = f"https://api.github.com/repos/{container_image.replace('docker.io/', '').replace('/', '/')}/tags"
        response = requests.get(github_registry_url)
        if response.status_code == 200:
            data = response.json()
            tags = [tag["name"] for tag in data]
            github_registry_version = max(tags, default="N/A") if tags else "N/A"

    # Determine if an update is available
    update_available = (docker_hub_version != current_version and docker_hub_version != "N/A") or \
                       (github_registry_version != current_version and github_registry_version != "N/A")

    table_data.append({
        "Container Name": f"{container_name} ({container_image})",
        "Current Version": current_version,
        "Docker Hub Version": docker_hub_version,
        "GitHub Registry Version": github_registry_version,
        "Update Available": "Yes" if update_available else "No"
    })

print(tabulate(table_data, headers="keys", tablefmt="psql"))
