// Define an array of suggestions
let suggestions = [];


// Get HTML elements
const suggestionsList = document.getElementById('suggestions-list');
const searchInput = document.getElementById('search-input');

searchInput.addEventListener('input', function() {
    let input = searchInput.value;
    suggestionsList.innerHTML = ''; // Clear the suggestions list before displaying new suggestions

    // Filter the suggestions array based on the input value
    let suggestionsToDisplay = suggestions.filter(function(suggestion) {
        return suggestion.toLowerCase().startsWith(input.toLowerCase());
    });

    // Iterate over the filtered suggestions and create list elements for each suggestion
    suggestionsToDisplay.forEach(function(suggestion) {
        let suggestionElement = document.createElement('li');
        suggestionElement.innerHTML = suggestion;
        suggestionsList.appendChild(suggestionElement);
    });
});