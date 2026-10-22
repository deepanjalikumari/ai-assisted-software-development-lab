const elements = {
  scenarioSelect: document.querySelector("#scenario-select"),
  floorCount: document.querySelector("#floor-count"),
  liftCount: document.querySelector("#lift-count"),
  building: document.querySelector("#building"),
  liftConsoles: document.querySelector("#lift-consoles"),
  eventTime: document.querySelector("#event-time"),
  eventQueue: document.querySelector("#event-queue"),
  queueCount: document.querySelector("#queue-count"),
  eventLog: document.querySelector("#event-log"),
  logCount: document.querySelector("#log-count"),
  systemStatus: document.querySelector("#system-status"),
  simTime: document.querySelector("#sim-time"),
  bankSummary: document.querySelector("#bank-summary"),
  description: document.querySelector("#scenario-description"),
  speed: document.querySelector("#speed"),
  speedValue: document.querySelector("#speed-value"),
  run: document.querySelector("#run-replay"),
  pause: document.querySelector("#pause-replay"),
  step: document.querySelector("#step-replay"),
};

let scenarios = [];
let queuedEvents = [];
let replayEvents = [];
let replayIndex = 0;
let replayPosition = 0;
let replayStartedAt = 0;
let replayTimer = null;
let lifts = [];
const litCalls = new Set();
const litFloorButtons = new Set();

function currentConfiguration() {
  return {
    floors: Number(elements.floorCount.value),
    elevators: Number(elements.liftCount.value),
  };
}

function resetLiftState() {
  const { elevators } = currentConfiguration();
  lifts = Array.from({ length: elevators }, () => ({ floor: 0, direction: "idle", door: "closed" }));
  litCalls.clear();
  litFloorButtons.clear();
  elements.simTime.textContent = "0.0";
  renderBank();
}

function directionMark(direction) {
  if (direction === "up") return "↑ UP";
  if (direction === "down") return "↓ DOWN";
  return "— IDLE";
}

function callKey(floor, direction) {
  return `call:${floor}:${direction}`;
}

function pressKey(elevator, floor) {
  return `press:${elevator}:${floor}`;
}

function addEvent(event) {
  if (!Number.isFinite(event.t) || event.t < 0) {
    elements.description.textContent = "Enter a valid simulated time of zero or more seconds.";
    return;
  }
  queuedEvents.push(event);
  queuedEvents.sort((first, second) => first.t - second.t);
  elements.description.textContent = "Event added to the scenario queue.";
  renderQueue();
}

function renderBank() {
  const { floors, elevators } = currentConfiguration();
  elements.bankSummary.textContent = `${floors} FLOORS / ${elevators} LIFTS`;
  elements.building.style.setProperty("--lift-count", elevators);

  const headings = ["FL", "CALL"];
  const header = `<div class="building-header"><div>${headings[0]}</div><div>${headings[1]}</div>${lifts.map((_, id) => `<div>LIFT ${String(id + 1).padStart(2, "0")}</div>`).join("")}</div>`;
  const rows = [];
  for (let floor = floors - 1; floor >= 0; floor -= 1) {
    const upAllowed = floor < floors - 1;
    const downAllowed = floor > 0;
    const hallButtons = `<div class="hall-buttons"><button class="hall-button ${litCalls.has(callKey(floor, "up")) ? "lit" : ""}" data-action="call" data-floor="${floor}" data-direction="up" aria-label="Up call at floor ${floor}" title="Call an up lift at floor ${floor}" ${upAllowed ? "" : "disabled"}>↑</button><button class="hall-button ${litCalls.has(callKey(floor, "down")) ? "lit" : ""}" data-action="call" data-floor="${floor}" data-direction="down" aria-label="Down call at floor ${floor}" title="Call a down lift at floor ${floor}" ${downAllowed ? "" : "disabled"}>↓</button></div>`;
    const cars = lifts.map((lift, id) => {
      if (lift.floor !== floor) return "<div class=\"shaft-cell\"></div>";
      return `<div class="shaft-cell"><div class="lift-car ${lift.door === "open" ? "open" : ""}"><span class="lift-car-name">CAR ${String(id + 1).padStart(2, "0")}</span><strong class="lift-car-floor">${floor}</strong><span class="lift-car-direction">${directionMark(lift.direction)}</span><span class="lift-car-door">DOORS ${lift.door.toUpperCase()}</span></div></div>`;
    }).join("");
    rows.push(`<div class="floor-row"><div class="floor-id">${String(floor).padStart(2, "0")}</div>${hallButtons}${cars}</div>`);
  }
  elements.building.innerHTML = header + rows.join("");

  elements.liftConsoles.innerHTML = lifts.map((lift, id) => {
    const floorsHtml = Array.from({ length: floors }, (_, floor) => `<button class="floor-button ${litFloorButtons.has(pressKey(id, floor)) ? "lit" : ""}" data-action="press" data-elevator="${id}" data-floor="${floor}" aria-label="Lift ${id + 1}, floor ${floor}" title="Select floor ${floor}">${floor}</button>`).join("");
    return `<section class="lift-console"><div class="console-heading"><strong>LIFT ${String(id + 1).padStart(2, "0")} / ${lift.floor}</strong><span class="console-status">${directionMark(lift.direction)} · ${lift.door}</span></div><div class="console-door-buttons"><button data-action="open" data-elevator="${id}" type="button">↗ OPEN</button><button data-action="close" data-elevator="${id}" type="button">↘ CLOSE</button></div><div class="floor-buttons">${floorsHtml}</div></section>`;
  }).join("");
}

function describeQueuedEvent(event) {
  if (event.type === "call") return `Floor ${event.floor} · ${event.dir.toUpperCase()} call`;
  if (event.type === "press") return `Lift ${event.elevator + 1} · select floor ${event.floor}`;
  return `Lift ${event.elevator + 1} · ${event.type} doors`;
}

function renderQueue() {
  elements.queueCount.textContent = String(queuedEvents.length);
  if (queuedEvents.length === 0) {
    elements.eventQueue.innerHTML = '<li class="empty-queue">No button presses queued.</li>';
    return;
  }
  elements.eventQueue.innerHTML = queuedEvents.map((event, index) => `<li class="queue-item"><span class="queue-time">T+${event.t}s</span><span class="queue-event">${describeQueuedEvent(event)}</span><button class="queue-remove" data-remove-event="${index}" type="button" aria-label="Remove event">×</button></li>`).join("");
}

function eventDescription(event) {
  if (event.event === "arrive") return `Lift ${event.elevator + 1} / floor ${event.floor}`;
  if (event.event === "door_open" || event.event === "door_close") return `Lift ${event.elevator + 1} / ${event.event.replace("_", " ")}`;
  if (event.event.startsWith("light_")) {
    const state = event.event === "light_on" ? "light on" : "light off";
    if (event.button === "call") return `Floor ${event.floor} / ${event.dir} call ${state}`;
    return `Lift ${event.elevator + 1} / floor ${event.floor} ${state}`;
  }
  return event.event;
}

function renderLog(currentLine = -1) {
  if (replayEvents.length === 0) {
    elements.eventLog.innerHTML = '<p class="empty-log">Run a scenario to inspect arrivals, doors, and button lights.</p>';
    elements.logCount.textContent = "WAITING FOR REPLAY";
    return;
  }
  elements.logCount.textContent = `${replayIndex} / ${replayEvents.length} EVENTS`;
  elements.eventLog.innerHTML = replayEvents.map((event, index) => `<div class="log-row ${index === currentLine ? "current" : ""}"><span class="log-time">${Number(event.t).toFixed(1)}s</span><span class="log-event">${eventDescription(event)}</span><span class="log-detail">${event.dir ? directionMark(event.dir) : event.button?.toUpperCase() ?? ""}</span></div>`).join("");
  const current = elements.eventLog.querySelector(".current");
  current?.scrollIntoView({ block: "nearest" });
}

function applyLogEvent(event) {
  if (event.event === "arrive") {
    lifts[event.elevator].floor = event.floor;
    lifts[event.elevator].direction = event.dir;
  } else if (event.event === "door_open") {
    lifts[event.elevator].floor = event.floor;
    lifts[event.elevator].door = "open";
    lifts[event.elevator].direction = event.dir;
  } else if (event.event === "door_close") {
    lifts[event.elevator].floor = event.floor;
    lifts[event.elevator].door = "closed";
    lifts[event.elevator].direction = event.dir;
  } else if (event.button === "call") {
    const key = callKey(event.floor, event.dir);
    if (event.event === "light_on") litCalls.add(key);
    else litCalls.delete(key);
  } else if (event.button === "press") {
    const key = pressKey(event.elevator, event.floor);
    if (event.event === "light_on") litFloorButtons.add(key);
    else litFloorButtons.delete(key);
  }
  elements.simTime.textContent = Number(event.t).toFixed(1);
  renderBank();
}

function stopPlayback() {
  if (replayTimer !== null) window.clearInterval(replayTimer);
  replayTimer = null;
}

function playFrom(position = replayPosition) {
  stopPlayback();
  replayPosition = position;
  replayStartedAt = performance.now();
  elements.pause.disabled = false;
  elements.pause.innerHTML = '<span aria-hidden="true">Ⅱ</span>';
  elements.pause.setAttribute("aria-label", "Pause replay");
  replayTimer = window.setInterval(() => {
    replayPosition = position + (performance.now() - replayStartedAt) * Number(elements.speed.value) / 1000;
    while (replayIndex < replayEvents.length && replayEvents[replayIndex].t <= replayPosition) {
      applyLogEvent(replayEvents[replayIndex]);
      replayIndex += 1;
      renderLog(replayIndex - 1);
    }
    if (replayIndex >= replayEvents.length) {
      stopPlayback();
      elements.pause.innerHTML = '<span aria-hidden="true">↻</span>';
      elements.pause.setAttribute("aria-label", "Replay from beginning");
      elements.systemStatus.textContent = "Replay complete";
    }
  }, 35);
}

function resetReplay() {
  stopPlayback();
  replayEvents = [];
  replayIndex = 0;
  replayPosition = 0;
  elements.pause.disabled = true;
  elements.step.disabled = true;
  resetLiftState();
  renderLog();
}

async function loadScenarios() {
  const response = await fetch("/api/scenarios");
  if (!response.ok) throw new Error("Scenario list could not be loaded.");
  const data = await response.json();
  scenarios = data.scenarios;
  elements.scenarioSelect.innerHTML = scenarios.map((item, index) => `<option value="${index}">${item.file}</option>`).join("");
  elements.systemStatus.textContent = "System ready";
  if (scenarios.length) loadSelectedScenario();
}

function loadSelectedScenario() {
  const selected = scenarios[Number(elements.scenarioSelect.value)];
  if (!selected) return;
  const scenario = selected.scenario;
  elements.floorCount.value = scenario.floors;
  elements.liftCount.value = scenario.elevators;
  queuedEvents = scenario.events.map((event) => ({ ...event }));
  elements.description.textContent = selected.description;
  resetReplay();
  renderQueue();
}

async function runReplay() {
  const { floors, elevators } = currentConfiguration();
  if (!Number.isInteger(floors) || floors < 2 || floors > 20 || !Number.isInteger(elevators) || elevators < 1 || elevators > 4) {
    elements.description.textContent = "Choose 2–20 floors and 1–4 lifts.";
    return;
  }
  stopPlayback();
  elements.run.disabled = true;
  elements.systemStatus.textContent = "Running simulated time";
  try {
    const response = await fetch("/api/replay", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ floors, elevators, events: queuedEvents }),
    });
    if (!response.ok) throw new Error(await response.text());
    const data = await response.json();
    replayEvents = data.events;
    replayIndex = 0;
    replayPosition = 0;
    resetLiftState();
    elements.step.disabled = replayEvents.length === 0;
    elements.systemStatus.textContent = "Replay ready";
    renderLog();
    if (replayEvents.length) playFrom(0);
  } catch (error) {
    elements.systemStatus.textContent = "Replay failed";
    elements.description.textContent = error.message;
  } finally {
    elements.run.disabled = false;
  }
}

document.querySelector("#load-scenario").addEventListener("click", loadSelectedScenario);
document.querySelector("#apply-config").addEventListener("click", () => {
  const { floors, elevators } = currentConfiguration();
  if (floors < 2 || floors > 20 || elevators < 1 || elevators > 4) {
    elements.description.textContent = "Choose 2–20 floors and 1–4 lifts.";
    return;
  }
  queuedEvents = [];
  elements.description.textContent = "New bank ready. Add button presses, then run the replay.";
  resetReplay();
  renderQueue();
});
elements.scenarioSelect.addEventListener("change", loadSelectedScenario);
elements.run.addEventListener("click", runReplay);
elements.pause.addEventListener("click", () => {
  if (replayTimer !== null) {
    replayPosition += (performance.now() - replayStartedAt) * Number(elements.speed.value) / 1000;
    stopPlayback();
    elements.pause.innerHTML = '<span aria-hidden="true">▶</span>';
    elements.pause.setAttribute("aria-label", "Resume replay");
    elements.systemStatus.textContent = "Replay paused";
  } else if (replayIndex < replayEvents.length) {
    playFrom(replayPosition);
  } else if (replayEvents.length) {
    replayIndex = 0;
    replayPosition = 0;
    resetLiftState();
    renderLog();
    playFrom(0);
  }
});
elements.step.addEventListener("click", () => {
  stopPlayback();
  if (replayIndex >= replayEvents.length) return;
  const eventTime = replayEvents[replayIndex].t;
  while (replayIndex < replayEvents.length && replayEvents[replayIndex].t === eventTime) {
    applyLogEvent(replayEvents[replayIndex]);
    replayIndex += 1;
  }
  replayPosition = eventTime;
  renderLog(replayIndex - 1);
  elements.systemStatus.textContent = "Stepped replay";
});
elements.speed.addEventListener("input", () => {
  elements.speedValue.textContent = elements.speed.value;
});
document.querySelector("#clear-events").addEventListener("click", () => {
  queuedEvents = [];
  renderQueue();
});

document.addEventListener("click", (event) => {
  const actionButton = event.target.closest("[data-action]");
  if (actionButton) {
    const t = Number(elements.eventTime.value);
    const floor = Number(actionButton.dataset.floor);
    const elevator = Number(actionButton.dataset.elevator);
    if (actionButton.dataset.action === "call") {
      addEvent({ t, type: "call", floor, dir: actionButton.dataset.direction });
    } else if (actionButton.dataset.action === "press") {
      addEvent({ t, type: "press", elevator, floor });
    } else {
      addEvent({ t, type: actionButton.dataset.action, elevator });
    }
  }

  const removeButton = event.target.closest("[data-remove-event]");
  if (removeButton) {
    queuedEvents.splice(Number(removeButton.dataset.removeEvent), 1);
    renderQueue();
  }
});

elements.speedValue.textContent = elements.speed.value;
resetLiftState();
renderQueue();
loadScenarios().catch((error) => {
  elements.systemStatus.textContent = "Server unavailable";
  elements.description.textContent = error.message;
});