param(
    [string]$ImageName = "colegio_ninito_jesus:local",
    [string]$ContainerName = "colegio_local"
)

Write-Host "Building Docker image $ImageName..."
docker build -t $ImageName .

if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker build failed. Check output above."
    exit 1
}

# Stop any existing container with the same name
$existing = docker ps -a --filter "name=$ContainerName" --format "{{.ID}}"
if ($existing) {
    Write-Host "Stopping and removing existing container..."
    docker rm -f $ContainerName | Out-Null
}

Write-Host "Starting container $ContainerName (ports 8000:8000)..."
docker run -d --name $ContainerName -p 8000:8000 --env DJANGO_DEBUG=1 --env DJANGO_SECRET_KEY=dev-secret-key $ImageName

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to start container."
    exit 1
}

Write-Host "Running migrations inside container..."
docker exec -u root $ContainerName python manage.py migrate --noinput

Write-Host "Collecting static files inside container..."
docker exec -u root $ContainerName python manage.py collectstatic --noinput

Write-Host "Tailing container logs (press Ctrl+C to stop)..."
docker logs -f $ContainerName
