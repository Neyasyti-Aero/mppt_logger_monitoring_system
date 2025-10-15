#!/bin/bash
set -e

echo "Сборка и запуск в production..."

# Собираем фронтенд для production
cd frontend
npm run build
cd ..

# Копируем build в nginx
docker-compose -f docker-compose.prod.yml up -d --build

echo "✅ Готово! Откройте http://ваш_сервер"