// Function to handle form submission and add a new raw ingredient
document.getElementById('rawIngredientForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent page reload on form submission

    // Get form data
    const name = document.getElementById('raw-name').value;
    const unit = document.getElementById('raw-unit').value;
    const measurement = parseFloat(document.getElementById('raw-measurement').value);
    const price = parseFloat(document.getElementById('raw-price').value);

    // Validate form data
    if (!name || !unit || isNaN(measurement) || isNaN(price)) {
        alert('Please fill in all fields correctly.');
        return;
    }

    // Send POST request to the backend
    const response = await fetch('/add_raw', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            name, 
            unit_of_measure: unit, 
            measurement, 
            purchase_price: price 
        }),
    });

    // Handle response
    if (response.ok) {
        alert('Raw ingredient added successfully!');
        fetchRawIngredients(); // Refresh the table to show the updated data
        document.getElementById('rawIngredientForm').reset(); // Clear form fields
    } else {
        alert('Failed to add raw ingredient.');
    }
});

// Function to fetch raw ingredients and populate the table
async function fetchRawIngredients() {
    const response = await fetch('/get_raw');
    if (response.ok) {
        const raws = await response.json();
        const tableBody = document.getElementById('rawIngredientTableBody');
        tableBody.innerHTML = ''; // Clear existing table rows

        raws.forEach(raw => {
            const row = `
                <tr>
                    <td>${raw.name}</td>
                    <td>${raw.unit_of_measure}</td>
                    <td>${raw.measurement}</td>
                    <td>${raw.purchase_price}</td>
                    <td>${raw.price_per_unit}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    } else {
        console.error('Failed to fetch raw ingredients.');
    }
}

// Initialize the page by fetching raw ingredients
document.addEventListener('DOMContentLoaded', fetchRawIngredients);