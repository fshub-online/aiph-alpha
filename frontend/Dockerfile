# Dockerfile for Vue.js + Vuetify Application using PNPM

# ---- Stage 1: Build ----
# Use an official Node.js runtime as a parent image.
# Alpine Linux based images are smaller.
# Replace 'lts-alpine' with a specific version if needed (e.g., '20-alpine').
# Node.js LTS versions (like 18.x, 20.x) come with corepack, which can manage pnpm.
FROM node:lts-alpine AS build-stage

# Set the working directory in the container.
WORKDIR /app

# Enable corepack to use pnpm (recommended way for Node.js >= 16.9.0)
# This ensures you're using the pnpm version defined in your project's package.json if specified.
RUN corepack enable
RUN corepack prepare pnpm@latest --activate
# If the above corepack commands don't work (e.g., older Node version or specific setup),
# you can install pnpm globally using npm:
# RUN npm install -g pnpm

# Copy package.json and the pnpm lockfile.
# This step leverages Docker's cache.
COPY package.json pnpm-lock.yaml ./
# If you only have package.json and expect pnpm to generate the lockfile,
# you might only copy package.json first, then run install, then copy the rest.
# However, it's best practice to commit your lockfile and use it.

# Install project dependencies using pnpm.
# '--frozen-lockfile' is recommended for CI/Docker to ensure reproducible builds.
# If your pnpm version is < 7, use 'pnpm install --frozen-lockfile false' or 'pnpm install --no-frozen-lockfile'
# and then 'pnpm install --frozen-lockfile' after copying all files if you prefer.
# For most modern pnpm versions, '--frozen-lockfile' is the default when a lockfile is present.
# The command 'pnpm install --prod' could be used if you don't need devDependencies for the build.
# However, build tools are often in devDependencies.
RUN pnpm install --frozen-lockfile

# Copy the rest of the application's source code to the working directory.
COPY . .

# Build the application for production using pnpm.
# This command might differ based on your project's scripts in package.json.
RUN pnpm run build

# ---- Stage 2: Production ----
# Use a lightweight Nginx image to serve the static files.
# Alpine Linux based images are smaller.
FROM nginx:stable-alpine AS production-stage

# Set the working directory for Nginx.
WORKDIR /usr/share/nginx/html

# Remove default Nginx static assets.
RUN rm -rf ./*

# Copy the built static files from the 'build-stage' (from the /app/dist directory)
# to the Nginx HTML directory. The 'dist' folder is a common output for Vue CLI builds.
# Adjust '/app/dist' if your build output directory is different.
COPY --from=build-stage /app/dist .

# (Optional) Copy a custom Nginx configuration file.
# This is often needed for Single Page Applications (SPAs) like Vue.js
# to correctly handle client-side routing (e.g., Vue Router in history mode).
# If you don't have a custom nginx.conf, Nginx will use its default configuration.
# Create an 'nginx.conf' file in the same directory as your Dockerfile.
COPY nginx.conf /etc/nginx/conf.d/default.conf
# If you don't have a custom nginx.conf, you can remove the line above.

# Expose port 80 to the outside world.
EXPOSE 80

# Start Nginx when the container launches.
# The 'daemon off;' directive keeps Nginx running in the foreground,
# which is standard practice for Docker containers.
CMD ["nginx", "-g", "daemon off;"]
