from django.shortcuts import render
from.models import Container
import docker
import requests

def container_list(request):
    containers = []
    client = docker.from_env()
    for container in client.containers.list(all=True):
        container_name = container.name
        container_image = container.image
        container_version = container.image.tags[0].split(":")[1]

        docker_hub_url = f"https://registry.hub.docker.com/v1/repositories/{container_image}/tags"
        response = requests.get(docker_hub_url)
        docker_hub_version = response.json()[0]["name"]

        gist_url = f"https://api.github.com/gists/{container_image}"
        response = requests.get(gist_url)
        gist_version = response.json()["files"][0]["content"] if response.status_code == 200 else "N/A"

        containers.append({
            "name": container_name,
            "image": container_image,
            "current_version": container_version,
            "docker_hub_version": docker_hub_version,
            "gist_version": gist_version
        })

    return render(request, "container_list.html", {"containers": containers})
