const searchInput = document.getElementById("search-input"); // Get the search input element
const agentRows = document.querySelectorAll(".agent-row"); // Get all agent rows

searchInput.addEventListener("input", function () {
  const searchQuery = this.value.trim().toLowerCase(); // Get the trimmed and lowercase search query

  agentRows.forEach(function (row) {
    const agentNames = row.querySelectorAll(".agent-details h3"); // Get all agent names within the current row
    let isMatchFound = false; // Flag to track if a match is found for the current row

    agentNames.forEach(function (name) {
      const agentName = name.innerText.toLowerCase(); // Get the lowercase text of the agent name

      if (agentName.includes(searchQuery)) { // Check if the agent name contains the search query
        row.style.display = "block"; // Display the row if there is a match
        isMatchFound = true; // Set the flag to true indicating a match is found
      } else {
        row.style.display = "none"; // Hide the row if there is no match
      }
    });

    if (!isMatchFound) {
      row.style.display = "none"; // Hide the row if no match is found within the agent names
    }
  });
});
