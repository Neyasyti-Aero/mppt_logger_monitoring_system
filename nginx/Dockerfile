# nginx/Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY ../frontend/package*.json ./
RUN npm ci --only=production
COPY ../frontend .
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Копируем в /usr/share/nginx/html/mppt_loggers
COPY --from=builder /app/build /usr/share/nginx/html/mppt_loggers