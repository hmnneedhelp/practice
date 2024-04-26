FROM bun:latest

# Set working directory to /app
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN bun install

# Copy application code
COPY . .

# Expose port 3000 for the React app
EXPOSE 3000

# Run the command to start the React app
CMD ["bun", "dev"]