<<<<<<< HEAD
# Finanças - Projeto Django (Completo)

Inclui:
- Django 5.2.8
- App controle (Entrada / Saida)
- Bootstrap 5 front-end responsivo
- PWA (manifest + service worker)
- Gunicorn + Dockerfile + docker-compose
- SQLite como banco (db.sqlite3)

## Como usar

1. Construa a imagem e suba o container:
   ```
   docker compose up -d --build
   ```

2. Execute migrações:
   ```
   docker exec -it financas python manage.py migrate
   ```

3. (Opcional) Crie superuser:
   ```
   docker exec -it financas python manage.py createsuperuser
   ```

4. Acesse: http://SEU_IP:8000

5. Para obter HTTPS, use o Nginx Proxy Manager apontando para SEU_IP:8000

=======
# financas_django
app controle de finaças
>>>>>>> 0a9b4a4f37a1ab3c0dd7e16efc3ad592345efe26
