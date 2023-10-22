function validateForm() {
    var loadWeight = parseFloat(document.getElementById('LoadWeight').value);
    var weightToDestroy = parseFloat(document.getElementById('WeightToDestroy').value);

    if (isNaN(loadWeight) || isNaN(weightToDestroy)) {
        // Handle invalid input (non-numeric values)
        alert("Please enter valid numeric values for Load Weight and Weight to Destroy.");
        return false; // Prevent the form from submitting
    }

    if (weightToDestroy >= loadWeight) {
        // Display an error message
        alert("Weight to Destroy must be less than Load Weight.");
        return false; // Prevent the form from submitting
    }

    // Form data is valid, allow the form to submit
    return true;
}