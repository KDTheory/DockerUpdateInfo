import docker
from tabulate import tabulate

client = docker.from_env()

containers = client.containers.list(all=True)

table_data = []
for container in containers:
    container_name = container.name
    container_image = container.image
    container_version = container.image.tags[0].split(":")[1]

    docker_hub_url = f"https://registry.hub.docker.com/v1/repositories/{container_image}/tags"
    response = requests.get(docker_hub_url)
    docker_hub_version = response.json()[0]["name"]

    gist_url = f"https://api.github.com/gists/{container_image}"
    response = requests.get(gist_url)
    gist_version = response.json()["files"][0]["content"] if response.status_code == 200 else "N/A"

    table_data.append({
        "Container Name": container_name,
        "Current Version": container_version,
        "Docker Hub Version": docker_hub_version,
        "GitHub Gist Version": gist_version
    })

print(tabulate(table_data, headers="keys", tablefmt="psql"))
