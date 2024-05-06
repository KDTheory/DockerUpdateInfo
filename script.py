import docker
import requests
from tabulate import tabulate

client = docker.from_env()

containers = client.containers.list(all=True)

table_data = []
for container in containers:
    container_name = container.name
    container_image = container.attrs['Config']['Image']

    docker_hub_version = "N/A"
    github_registry_version = "N/A"

    if container_image:
        docker_hub_url = f"https://hub.docker.com/v2/repositories/{container_image}/tags"
        response = requests.get(docker_hub_url)
        if response.status_code == 200:
            docker_hub_version = response.json()[0]["name"] if response.json()["results"] else "N/A"

        github_registry_url = f"https://api.github.com/repos/{container_image}/tags"
        response = requests.get(github_registry_url)
        if response.status_code == 200:
            github_registry_version = response.json()[0]["name"] if response.json() else "N/A"

    table_data.append({
        "Container Name": f"{container_name} ({container_image})",
        "Current Version": container.image.tags[0].split(":")[1] if container.image.tags else "N/A",
        "Docker Hub Version": docker_hub_version,
        "GitHub Registry Version": github_registry_version
    })

print(tabulate(table_data, headers="keys", tablefmt="psql"))
