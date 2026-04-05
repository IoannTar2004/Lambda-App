FROM node:25-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm install
ARG MODE=example
ENV MODE=$MODE

COPY . .

RUN npm run build -- --mode $MODE

FROM alpine:latest

WORKDIR /usr/share/nginx/html

COPY --from=builder /app/dist .
