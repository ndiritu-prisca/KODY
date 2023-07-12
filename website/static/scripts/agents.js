const searchInput = document.getElementById("search-input");
const agentRows = document.querySelectorAll(".agent-row");

searchInput.addEventListener("input", function () {
  const searchQuery = this.value.trim().toLowerCase();
  agentRows.forEach(function (row) {
    const agentNames = row.querySelectorAll(".agent-details h3");
    let isMatchFound = false;
    agentNames.forEach(function (name) {
      const agentName = name.innerText.toLowerCase();
      if (agentName.includes(searchQuery)) {
        row.style.display = "block";
        isMatchFound = true;
      } else {
        row.style.display = "none";
      }
    });
    if (!isMatchFound) {
      row.style.display = "none";
    }
  });
});