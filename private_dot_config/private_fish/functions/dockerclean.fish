function dockerclean --description "Safely prune stopped containers, unused networks, and dangling images"
    if not type -q docker
        echo "dockerclean: docker is not installed or not in PATH"
        return 1
    end

    echo "==> Cleaning stopped containers..."
    docker container prune -f
    echo "==> Cleaning unused networks..."
    docker network prune -f
    echo "==> Cleaning dangling images..."
    docker image prune -f
    echo "✓ Docker cleanup complete."
end
