const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchResources() {
  const response = await fetch(`${API_BASE_URL}/resources`);

  if (!response.ok) {
    throw new Error("Ressourcen konnten nicht geladen werden.");
  }

  return response.json();
}

export async function fetchAvailableResources(filters) {
  const params = new URLSearchParams({
    booking_date: filters.bookingDate,
    start_time: filters.startTime,
    end_time: filters.endTime,
  });

  if (filters.resourceType) {
    params.append("resource_type", filters.resourceType);
  }

  const response = await fetch(`${API_BASE_URL}/resources/available?${params}`);

  if (!response.ok) {
    throw new Error("Verfügbare Ressourcen konnten nicht geladen werden.");
  }

  return response.json();
}

export async function fetchReservations(bookingDate) {
  const response = await fetch(
    `${API_BASE_URL}/reservations?booking_date=${bookingDate}`
  );

  if (!response.ok) {
    throw new Error("Reservierungen konnten nicht geladen werden.");
  }

  return response.json();
}

export async function createReservation(payload) {
  const response = await fetch(`${API_BASE_URL}/reservations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (response.status === 409) {
    throw new Error("Diese Ressource ist in diesem Zeitraum bereits gebucht.");
  }

  if (!response.ok) {
    throw new Error("Reservierung konnte nicht erstellt werden.");
  }

  return response.json();
}