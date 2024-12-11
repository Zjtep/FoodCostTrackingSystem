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

async function fetchRawIngredientOptions() {
    const response = await fetch('/get_raw');
    const raws = await response.json();
    const dropdown = document.getElementById('in-house-raw');
    dropdown.innerHTML = '<option value="">Select Raw Ingredient</option>';

    raws.forEach(raw => {
        const option = document.createElement('option');
        option.value = JSON.stringify(raw); // Pass raw ingredient data as JSON string
        option.textContent = `${raw.name} (${raw.unit_of_measure})`;
        dropdown.appendChild(option);
    });
}

document.getElementById('addComponentButton').addEventListener('click', () => {
    const rawIngredientDropdown = document.getElementById('in-house-raw');
    const rawIngredient = JSON.parse(rawIngredientDropdown.value);
    const measurement = parseFloat(document.getElementById('in-house-measurement').value);

    if (!rawIngredient || isNaN(measurement) || measurement <= 0) {
        alert('Please select a raw ingredient and enter a valid measurement.');
        return;
    }

    const tableBody = document.getElementById('inHouseComponentTableBody');
    const row = `
        <tr>
            <td>${rawIngredient.name}</td>
            <td>${measurement}</td>
            <td>${rawIngredient.unit_of_measure}</td>
            <td>${rawIngredient.price_per_unit}</td>
        </tr>
    `;
    tableBody.innerHTML += row;

    // Clear the measurement input for next entry
    document.getElementById('in-house-measurement').value = '';
});

document.getElementById('saveInHouseButton').addEventListener('click', async () => {
    const name = document.getElementById('in-house-name').value;
    const tableRows = document.querySelectorAll('#inHouseComponentTableBody tr');

    if (!name || tableRows.length === 0) {
        alert('Please provide a name and at least one component.');
        return;
    }

    const components = Array.from(tableRows).map(row => {
        const cells = row.children;
        return {
            raw_name: cells[0].textContent,
            measurement: parseFloat(cells[1].textContent),
        };
    });

    const response = await fetch('/add_in_house', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, components }),
    });

    if (response.ok) {
        alert('In-House Ingredient saved successfully!');
        document.getElementById('inHouseIngredientForm').reset();
        document.getElementById('inHouseComponentTableBody').innerHTML = '';
        fetchInHouseIngredients(); // Refresh the saved list
    } else {
        alert('Failed to save In-House Ingredient.');
    }
});


async function fetchInHouseIngredients() {
    const response = await fetch('/get_in_house');
    if (response.ok) {
        const inHouseIngredients = await response.json();
        const tableBody = document.getElementById('inHouseIngredientTableBody');
        tableBody.innerHTML = ''; // Clear existing rows

        inHouseIngredients.forEach(ingredient => {
            const components = ingredient.components.map(component => 
                `${component.raw_name} (${component.quantity_used} ${component.unit_of_measure})`
            ).join(', ');

            const row = `
                <tr>
                    <td>${ingredient.name}</td>
                    <td>${components}</td>
                    <td>${ingredient.total_measurement}</td>
                    <td>${ingredient.total_cost}</td>
                    <td>${ingredient.price_per_unit}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    } else {
        console.error('Failed to fetch in-house ingredients.');
    }
}

// Call this function on page load or when data changes
document.addEventListener('DOMContentLoaded', () => {
    fetchInHouseIngredients();
});



document.addEventListener('DOMContentLoaded', () => {
    fetchRawIngredientOptions();
});

// Initialize the page by fetching raw ingredients
document.addEventListener('DOMContentLoaded', fetchRawIngredients);
