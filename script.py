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
        # Récupérer la version actuelle du conteneur local
        current_version = container.image.tags[0].split(":")[-1] if container.image.tags else "N/A"

        # Récupérer les tags de l'image Docker sur Docker Hub
        docker_hub_url = f"https://hub.docker.com/v2/repositories/{container_image}/tags"
        response = requests.get(docker_hub_url)
        if response.status_code == 200:
            data = response.json()
            tags = [tag["name"] for tag in data.get("results", [])]
            docker_hub_version = tags[0] if tags else "N/A"

        # Récupérer les tags de l'image Docker sur GitHub Registry
        github_registry_url = f"https://api.github.com/repos/{container_image}/tags"
        response = requests.get(github_registry_url)
        if response.status_code == 200:
            tags = [tag["name"] for tag in response.json()]
            github_registry_version = tags[0] if tags else "N/A"

    # Comparer les versions pour déterminer s'il y a une mise à jour disponible
    update_available = docker_hub_version != current_version or github_registry_version != current_version

    table_data.append({
        "Container Name": f"{container_name} ({container_image})",
        "Current Version": current_version,
        "Docker Hub Version": docker_hub_version,
        "GitHub Registry Version": github_registry_version,
        "Update Available": "Yes" if update_available else "No"
    })

print(tabulate(table_data, headers="keys", tablefmt="psql"))
