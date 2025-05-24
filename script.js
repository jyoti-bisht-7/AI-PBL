const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let isDrawing = false;

// Set the initial brush size
let brushSize = 15;

// Setup canvas
canvas.addEventListener('mousedown', (event) => {
    isDrawing = true;
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    ctx.beginPath(); // Start a new path
    ctx.moveTo(x, y); // Move to the starting point
});
canvas.addEventListener('mouseup', () => isDrawing = false);
canvas.addEventListener('mouseout', () => isDrawing = false);
canvas.addEventListener('mousemove', draw);

// Initialize canvas with white background
function clearCanvas() {
    ctx.fillStyle = 'white'; // Set canvas background to white
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// Draw on the canvas with a trail effect
function draw(event) {
    if (!isDrawing) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Draw a line for smooth drawing
    ctx.lineWidth = brushSize; // Set the brush size
    ctx.lineCap = 'round'; // Smooth edges for the trace
    ctx.strokeStyle = 'black'; // Set brush color to black

    ctx.lineTo(x, y); // Draw a line to the current position
    ctx.stroke(); // Render the line
    ctx.beginPath(); // Start a new path
    ctx.moveTo(x, y); // Move to the current position

    // Create a trail effect by drawing small circles
    createTrail(event.pageX, event.pageY);
}

// Function to create a trail effect across the webpage
function createTrail(x, y) {
    const trail = document.createElement('div'); // Create a new div for the trail
    trail.className = 'cursor-trail'; // Assign a class for styling
    trail.style.left = `${x}px`; // Set the X position
    trail.style.top = `${y}px`; // Set the Y position
    document.body.appendChild(trail); // Add the trail to the body

    // Remove the trail after a short delay
    setTimeout(() => {
        trail.remove();
    }, 300); // Adjust the time (in milliseconds) for how long the trail stays
}

// Add a global mousemove event listener for the webpage trail
document.addEventListener('mousemove', (event) => {
    createTrail(event.pageX, event.pageY);
});

// Predict the digit
async function predictDigit() {
    const spinner = document.getElementById('loading-spinner');
    spinner.style.display = 'block'; // Show spinner

    document.getElementById('prediction').textContent = 'Loading...';

    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'digit.png');

        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            if (result.prediction !== undefined) {
                document.getElementById('prediction').textContent = result.prediction;
                updateHistory(result.prediction); // Update prediction history
            } else {
                alert('Error: ' + result.error);
                document.getElementById('prediction').textContent = '?';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to get prediction.');
            document.getElementById('prediction').textContent = '?';
        } finally {
            spinner.style.display = 'none'; // Hide spinner
        }
    }, 'image/png');
}

// Update prediction history
function updateHistory(prediction) {
    const historyTable = document.getElementById('history-table').querySelector('tbody');
    const rowCount = historyTable.rows.length + 1; // Get the current row count for numbering
    const timestamp = new Date().toLocaleString(); // Get the current timestamp

    // Create a new row
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${rowCount}</td>
        <td>${prediction}</td>
        <td>${timestamp}</td>
    `;

    // Append the row to the table
    historyTable.appendChild(row);
}

// Reset the app
function resetApp() {
    clearCanvas();
    document.getElementById('prediction').textContent = '?'; // Reset prediction text
    document.getElementById('history-list').innerHTML = ''; // Clear prediction history
    document.getElementById('brush-size').value = 15; // Reset brush size slider
    brushSize = 15; // Reset brush size variable
}

// Initialize the canvas when the page loads
clearCanvas();