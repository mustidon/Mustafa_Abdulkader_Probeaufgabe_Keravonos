<script setup>
import { onMounted, ref } from "vue";
import {
  createReservation,
  fetchAvailableResources,
  fetchReservations,
  fetchResources,
} from "./api/bookingApi";

const today = new Date().toISOString().slice(0, 10);

const bookingDate = ref(today);
const startTime = ref("09:00");
const endTime = ref("10:00");
const resourceType = ref("room");

const allResources = ref([]);
const availableResources = ref([]);
const reservations = ref([]);

const selectedResource = ref(null);
const bookedBy = ref("");
const title = ref("");
const note = ref("");

const message = ref("");
const error = ref("");

function clearMessages() {
  message.value = "";
  error.value = "";
}

function getResourceName(resourceId) {
  const resource = allResources.value.find((item) => item.id === resourceId);
  return resource ? resource.name : `Ressource ${resourceId}`;
}

async function loadAvailableResources() {
  clearMessages();

  try {
    availableResources.value = await fetchAvailableResources({
      bookingDate: bookingDate.value,
      startTime: startTime.value,
      endTime: endTime.value,
      resourceType: resourceType.value,
    });

    selectedResource.value = null;
  } catch (err) {
    error.value = err.message;
  }
}

async function loadReservations() {
  try {
    reservations.value = await fetchReservations(bookingDate.value);
  } catch (err) {
    error.value = err.message;
  }
}

function selectResource(resource) {
  selectedResource.value = resource;
  clearMessages();
}

async function submitReservation() {
  clearMessages();

  if (!selectedResource.value) {
    error.value = "Bitte zuerst eine Ressource auswählen.";
    return;
  }

  if (!bookedBy.value.trim() || !title.value.trim()) {
    error.value = "Bitte Name und Titel ausfüllen.";
    return;
  }

  try {
    await createReservation({
      resource_id: selectedResource.value.id,
      booked_by: bookedBy.value,
      title: title.value,
      booking_date: bookingDate.value,
      start_time: startTime.value,
      end_time: endTime.value,
      note: note.value,
    });

    message.value = "Reservierung wurde erfolgreich erstellt.";

    bookedBy.value = "";
    title.value = "";
    note.value = "";
    selectedResource.value = null;

    await loadAvailableResources();
    await loadReservations();
  } catch (err) {
    error.value = err.message;
  }
}

async function refreshData() {
  allResources.value = await fetchResources();
  await loadAvailableResources();
  await loadReservations();
}

onMounted(refreshData);
</script>

<template>
  <main class="page">
    <section class="hero">
      <p class="eyebrow">Office Booking</p>
      <h1>Räume und Arbeitsplätze einfach reservieren</h1>
      <p class="subtitle">
        Prüfe freie Ressourcen, erstelle Buchungen und vermeide Doppelbuchungen.
      </p>
    </section>

    <section class="panel">
      <h2>Verfügbarkeit prüfen</h2>

      <div class="filters">
        <label>
          Datum
          <input v-model="bookingDate" type="date" @change="refreshData" />
        </label>

        <label>
          Start
          <input v-model="startTime" type="time" />
        </label>

        <label>
          Ende
          <input v-model="endTime" type="time" />
        </label>

        <label>
          Typ
          <select v-model="resourceType">
            <option value="room">Raum</option>
            <option value="desk">Arbeitsplatz</option>
          </select>
        </label>

        <button @click="loadAvailableResources">
          Verfügbarkeit prüfen
        </button>
      </div>
    </section>

    <section class="layout">
      <div class="panel">
        <h2>Freie Ressourcen</h2>

        <div v-if="availableResources.length === 0" class="empty">
          Keine freie Ressource gefunden.
        </div>

        <div class="resource-grid">
          <article
            v-for="resource in availableResources"
            :key="resource.id"
            class="resource-card"
            :class="{ selected: selectedResource?.id === resource.id }"
            @click="selectResource(resource)"
          >
            <h3>{{ resource.name }}</h3>
            <p>{{ resource.location }}</p>
            <span>
              {{ resource.resource_type === "room" ? "Raum" : "Arbeitsplatz" }}
              · Kapazität: {{ resource.capacity }}
            </span>
          </article>
        </div>
      </div>

      <div class="panel">
        <h2>Reservierung erstellen</h2>

        <div v-if="selectedResource" class="selected-info">
          Ausgewählt: <strong>{{ selectedResource.name }}</strong>
        </div>

        <div class="form">
          <label>
            Name
            <input
              v-model="bookedBy"
              type="text"
              placeholder="z. B. Mustafa Abdulkader"
            />
          </label>

          <label>
            Titel
            <input
              v-model="title"
              type="text"
              placeholder="z. B. Team Meeting"
            />
          </label>

          <label>
            Notiz optional
            <textarea
              v-model="note"
              placeholder="Weitere Informationen"
            ></textarea>
          </label>

          <button @click="submitReservation">
            Reservieren
          </button>
        </div>

        <p v-if="message" class="success">{{ message }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </div>
    </section>

    <section class="panel">
      <h2>Reservierungen am {{ bookingDate }}</h2>

      <div v-if="reservations.length === 0" class="empty">
        Für dieses Datum gibt es noch keine Reservierungen.
      </div>

      <div class="reservation-list">
        <article
          v-for="reservation in reservations"
          :key="reservation.id"
          class="reservation-item"
        >
          <div>
            <strong>{{ reservation.title }}</strong>
            <p> {{ reservation.booked_by }} · {{ getResourceName(reservation.resource_id) }}</p>
          </div>

          <span>
            {{ reservation.start_time.slice(0, 5) }}–{{ reservation.end_time.slice(0, 5) }}
          </span>
        </article>
      </div>
    </section>
  </main>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.page {
  min-height: 100vh;
  background: #f4f6f8;
  color: #1f2937;
  font-family: Arial, sans-serif;
  padding: 32px;
}

.hero {
  max-width: 1100px;
  margin: 0 auto 24px;
  background: linear-gradient(135deg, #1f2937, #374151);
  color: white;
  padding: 32px;
  border-radius: 24px;
}

.eyebrow {
  margin: 0 0 8px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 13px;
  color: #cbd5e1;
}

h1 {
  margin: 0 0 12px;
  font-size: 34px;
}

.subtitle {
  margin: 0;
  color: #e5e7eb;
}

.panel {
  max-width: 1100px;
  margin: 0 auto 24px;
  background: white;
  padding: 24px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
}

h2 {
  margin-top: 0;
}

.filters,
.form {
  display: grid;
  gap: 16px;
}

.filters {
  grid-template-columns: repeat(5, minmax(0, 1fr));
  align-items: end;
}

label {
  display: grid;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
}

input,
select,
textarea {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 11px 12px;
  font: inherit;
}

textarea {
  min-height: 90px;
  resize: vertical;
}

button {
  border: none;
  border-radius: 12px;
  padding: 12px 16px;
  background: #1f2937;
  color: white;
  font-weight: 700;
  cursor: pointer;
}

button:hover {
  background: #111827;
}

.layout {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 24px;
}

.resource-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.resource-card {
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 18px;
  cursor: pointer;
  transition: 0.2s;
}

.resource-card:hover,
.resource-card.selected {
  border-color: #1f2937;
  transform: translateY(-2px);
}

.resource-card h3 {
  margin: 0 0 6px;
}

.resource-card p {
  margin: 0 0 10px;
  color: #6b7280;
}

.resource-card span {
  color: #4b5563;
  font-size: 14px;
}

.selected-info {
  background: #eef2ff;
  padding: 12px;
  border-radius: 12px;
  margin-bottom: 16px;
}

.success {
  color: #047857;
  font-weight: 700;
}

.error {
  color: #b91c1c;
  font-weight: 700;
}

.empty {
  color: #6b7280;
  background: #f9fafb;
  padding: 16px;
  border-radius: 12px;
}

.reservation-list {
  display: grid;
  gap: 12px;
}

.reservation-item {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 16px;
}

.reservation-item p {
  margin: 4px 0 0;
  color: #6b7280;
}

.reservation-item span {
  font-weight: 700;
}

@media (max-width: 850px) {
  .filters,
  .layout {
    grid-template-columns: 1fr;
  }

  .resource-grid {
    grid-template-columns: 1fr;
  }
}
</style>