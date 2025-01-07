## Backend - Asset Manager Backend

Il backend del sistema è progettato con le seguenti tecnologie e funzionalità:

### Tecnologie Utilizzate

- **Python**
- **Django**
- **Django Rest Framework (DRF)**
- **Docker**
- **PostgreSQL**
- **Caddy** (opzionale come reverse proxy)

### Ambiente

Questo backend è progettato per funzionare in ambiente Docker, e non si raccomanda l'utilizzo senza Docker.

### Come Usare Docker

1. Crea un file `.env` con le variabili d'ambiente richieste.
2. Avvia il progetto con:
   ```bash
   docker compose up --build
   ```
   Per l'ambiente di produzione, usa:
   ```bash
   docker compose -f docker-compose.prod.yml up --build
   ```

3. Esegui comandi all'interno del container. Ad esempio:
   ```bash
   docker exec -it asset-manager-backend-app-1 python manage.py makemigrations
   ```

### Funzionalità Principali del Backend

- **Gestione CRUD** per risorse IT, utenti e licenze.
- **Autenticazione Sicura** tramite Bearer Token.
- **Integrazione con Database PostgreSQL**.
- **Supporto API RESTful** con DRF.
- **Gestione CORS e Sicurezza**.
- **Documentazione API** con `drf-spectacular`.

### Generazione della Documentazione API

Per generare il file `schema.yml`:

- All'interno del container:
  ```bash
  python manage.py spectacular --color --file schema.yml
  ```

- Al di fuori del container:
  ```bash
  docker exec -it asset-manager-backend-app-1 python manage.py spectacular --color --file schema.yml
  ```

### Variabili d'Ambiente Necessarie

- **Obbligatorie:**
  - `DJANGO_SETTINGS_MODULE`
  - `DB_NAME`
  - `DB_USERNAME`
  - `DB_PASSWORD`
  - `DB_HOSTNAME`
  - `DB_PORT`
  - `DJANGO_ALLOWED_HOSTS`
  - `DJANGO_CORS_ALLOWED_ORIGINS`
  - `DJANGO_CSRF_TRUSTED_ORIGINS`
  - `CADDY_PORT`
  - `CADDY_EMAIL`
  - `DOMAIN`

- **Opzionali:**
  - `SECRET_KEY`
  - `EMAIL_HOST`, `EMAIL_HOST_PASSWORD`, `EMAIL_HOST_USER`, `EMAIL_PORT`
  - `DEBUG`

### Esempio di `.env`

```env
DJANGO_SETTINGS_MODULE=core.config.settings.development
SECRET_KEY=supersecretkey
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_PASSWORD=gmailpassword
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_PORT=587
DB_NAME=assetdb
DB_USERNAME=dbuser
DB_PASSWORD=dbpassword
DB_HOSTNAME=database
DB_PORT=5432
DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:3000
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:3000
CADDY_PORT=80
CADDY_EMAIL=admin@example.com
DOMAIN=example.com
```

## Contributi

Contribuzioni sono benvenute! Segui questi passaggi per proporre miglioramenti:

1. Fai un fork del repository.
2. Crea un branch per la tua feature:
   ```bash
   git checkout -b feature/<nome-feature>
   ```
3. Invia una pull request con una descrizione dettagliata delle modifiche.

## Licenza

Questo progetto è rilasciato sotto la licenza MIT. Consulta il file [LICENSE](LICENSE) per ulteriori dettagli.

---

**Autore:**
- Raffaele Grieco
