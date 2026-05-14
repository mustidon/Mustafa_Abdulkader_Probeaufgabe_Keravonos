# Office Booking App

Eine kleine Webanwendung zur Buchung von Besprechungsräumen und flexiblen Arbeitsplätzen in einem kleinen Büro.

## Ziel der Anwendung

Das Beispielproblem beschreibt ein kleines Unternehmen, das Reservierungen aktuell über Chat-Nachrichten und Tabellen organisiert. Dadurch entstehen Doppelbuchungen und fehlende Übersicht.

Meine Lösung konzentriert sich bewusst auf den wichtigsten Kernprozess:

- freie Räume und Arbeitsplätze anzeigen
- Reservierungen erstellen
- bestehende Reservierungen übersichtlich darstellen
- Doppelbuchungen verhindern

Ich habe bewusst keine große Benutzerverwaltung oder komplexe Kalenderintegration umgesetzt, damit der Kernprozess stabil, verständlich und wartbar bleibt.

## Technologie

### Backend

- Python
- FastAPI
- SQLModel
- SQLite
- pytest

### Frontend

- Vue
- Vite
- JavaScript
- Fetch API

## Projektstruktur

```text
office-booking-app/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── seed.py
│   │   ├── routers/
│   │   │   ├── resources.py
│   │   │   └── reservations.py
│   │   └── services/
│   │       └── availability_service.py
│   ├── tests/
│   │   └── test_availability_service.py
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend/
│   └── src/
│       ├── api/
│       │   └── bookingApi.js
│       └── App.vue
│
└── README.md

## Setup

### Backend starten

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload