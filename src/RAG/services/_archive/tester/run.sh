#!/usr/bin/env sh
set -e
echo "Waiting for API..."
until curl -s -X POST -H "Content-Type: application/json"   -d '{"q":"ping"}' http://api:8000/ask > /dev/null; do
  sleep 2
done

echo "Submitting sample query..."
curl -s -X POST -H "Content-Type: application/json"   -d '{"q":"What is discounted cash flow and the key inputs?"}'   http://api:8000/ask > /outputs/answer.json

echo "Saved to /outputs/answer.json"
cat /outputs/answer.json
