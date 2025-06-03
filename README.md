# SmallURL

Aplikacja Django do skracania linków (TinyURL) z API REST.

## Wymagania

- Docker
- Docker Compose

## Instalacja

1. Sklonuj repozytorium:
git clone git@github.com:WojciechT93/SmallURL.git
2. Stwórz plik `.env` na podstawie `.env.example` i dostosuj ustawienia bazy danych.
3. Uruchom Docker Compose:
```bash 
docker-compose up -d
```
4. Wykonaj migracje bazy danych:
```bash
docker exec -it smallurl_backend /bin/bash
python manage.py migrate
```
5. Aplikacja będzie dostępna pod adresem `http://localhost:8000`.

## Użycie
Spis dostępnych endpointów API znajduje się w dokumentacji Swaggera, dostępnej pod adresem 
`http://localhost:8000/swagger/`.
