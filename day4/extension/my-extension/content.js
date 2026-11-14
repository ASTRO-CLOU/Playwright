function addNote() {
  const note = document.createElement("div");
  note.id = "extension-note";
  note.textContent = "Changed by my-extension";
  document.body.appendChild(note);
}

if (document.body) {
  addNote();
} else {
  document.addEventListener("DOMContentLoaded", addNote);
}
