Tentative container build for the searchdv demo


# Build the container
docker build -t searchdv .

# Test it
docker run -d -p 8000:8000 searchdv

# Call the API
curl -X 'POST' 'http://127.0.0.1:8000/search' \
     -H 'Content-Type: application/json' \
     -d '{"query": "Colorado Adoption Project"}'

# Push to hub after tagging
docker tag searchdv smiacus/searchdv

docker push smiacus/searchdv

# Running as a service

docker compose up -d
