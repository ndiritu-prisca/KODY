document.addEventListener("DOMContentLoaded", function() {
    // Get references to the filter controls
    const locationSelect = document.getElementById("location");
    const priceSelect = document.getElementById("price");
    const agencySelect = document.getElementById("agency");
    const bedroomsSelect = document.getElementById("bedrooms");
  
    // Get references to all property containers
    const propertyContainers = document.querySelectorAll(".properties .carousel_container");
  
    // Collect unique values for locations, prices, and agencies
    const uniqueLocations = new Set();
    const uniquePrices = new Set();
    const uniqueAgencies = new Set();
    const uniqueBedrooms = new Set()

    // Add "All" option to each filter
    uniqueLocations.add("All");
    uniquePrices.add("All");
    uniqueAgencies.add("All");
    uniqueBedrooms.add("All");
  
    propertyContainers.forEach(function(container) {
      uniqueLocations.add(container.dataset.location);
      uniquePrices.add(container.dataset.price);
      uniqueAgencies.add(container.dataset.agency);
      uniqueBedrooms.add(container.dataset.bedrooms);
    });
  
    // Populate the filter options
    populateFilterOptions(locationSelect, uniqueLocations);
    populateFilterOptions(priceSelect, uniquePrices);
    populateFilterOptions(agencySelect, uniqueAgencies);
    populateFilterOptions(bedroomsSelect, uniqueBedrooms);
  
    // Function to populate filter options
    function populateFilterOptions(select, options) {
      options.forEach(function(option) {
        const optionElement = document.createElement("option");
        optionElement.value = option;
        optionElement.textContent = option;
        select.appendChild(optionElement);
      });
    }
  
    // Function to filter properties based on selected filters
    function filterProperties() {
      const selectedLocation = locationSelect.value;
      const selectedPrice = priceSelect.value;
      const selectedAgency = agencySelect.value;
      const selectedBedrooms = bedroomsSelect.value;

  // Loop through each property container and check if it matches the selected filters
  propertyContainers.forEach(function(container) {
    const propertyLocation = container.dataset.location;
    const propertyPrice = container.dataset.price;
    const propertyAgency = container.dataset.agency;
    const propertyBedrooms = container.dataset.bedrooms;

    // Hide or show the property based on the selected filters
    if (
      (selectedLocation === "All" || selectedLocation === propertyLocation) &&
      (selectedPrice === "All" || selectedPrice === propertyPrice) &&
      (selectedAgency === "All" || selectedAgency === propertyAgency) &&
      (selectedBedrooms === "All" || selectedBedrooms === propertyBedrooms)
    ) {
      container.style.display = "block";
    } else {
      container.style.display = "none";
    }
  });
}

// Add event listeners to the filter controls
locationSelect.addEventListener("change", filterProperties);
priceSelect.addEventListener("change", filterProperties);
agencySelect.addEventListener("change", filterProperties);
bedroomsSelect.addEventListener("change", filterProperties);

});