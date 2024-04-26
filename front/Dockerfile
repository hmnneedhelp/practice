FROM alpine:3.18
FROM oven/bun:1 as base
FROM base as install

ENV NODE_VERSION 20.12.0

WORKDIR /app

COPY ./front/package*.json ./

COPY ./front/bun.lockb ./

COPY ./front/src ./src

COPY ./front/rsbuild.config.mjs ./

RUN bun install
RUN bun run build 


EXPOSE 3000

ENTRYPOINT [ "bun", "run", "index.ts" ]

