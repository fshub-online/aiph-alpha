#!/bin/sh
# ./frontend/entrypoint.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Define a default server name if NGINX_SERVER_NAME is not set (e.g., for local development)
# If NGINX_SERVER_NAME is set (e.g., in docker-compose.prod.yml via .env), that value will be used.
export NGINX_SERVER_NAME_OR_DEFAULT=${NGINX_SERVER_NAME:-localhost}

# Substitute environment variables in the Nginx config template
# and output to the actual Nginx config file path.
# Only substitute NGINX_SERVER_NAME_OR_DEFAULT to avoid accidentally substituting other $vars in nginx.conf
envsubst '$NGINX_SERVER_NAME_OR_DEFAULT' < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Optional: Output the generated config for debugging
echo "--- Generated Nginx Configuration (/etc/nginx/conf.d/default.conf) ---"
cat /etc/nginx/conf.d/default.conf
echo "----------------------------------------------------------------------"

# Execute the CMD from the Dockerfile (which will be nginx -g 'daemon off;')
exec "$@"