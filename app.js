// Function to navigate to country details page
function openCountryDetails(country) {
    window.location.href = `country.html?name=${country}`;
}

// If you need to add any interactivity with charts later, you can include that code here.
// Example Chart.js usage for country-specific details:
document.addEventListener('DOMContentLoaded', (event) => {
    const urlParams = new URLSearchParams(window.location.search);
    const country = urlParams.get('name');

    if (country) {
        // Placeholder: You could fetch real data here and display it in charts
        console.log(`Displaying data for: ${country}`);
    }
});
/