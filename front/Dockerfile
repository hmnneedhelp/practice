FROM oven/bun:1 as base

WORKDIR /app

COPY package*.json ./
RUN bun install

COPY . .

EXPOSE 5173

CMD ["bun", "dev"]