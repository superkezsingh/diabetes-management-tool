document.addEventListener('DOMContentLoaded', function () {
    // Select the form and the response output area
    const form = document.getElementById('patient-form');
    const responseOutput = document.getElementById('response-output');

    // Handle form submission
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent page refresh

        // Capture form data
        const hba1c = document.getElementById('hba1c').value;
        const medications = document.getElementById('medications').value;

        // Send data to Flask backend
        fetch("http://127.0.0.1:5000/get-management-plan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ hba1c, medications })
        })
        .then(response => response.json())
        .then(data => {
            // Display the management plan from the response
            responseOutput.innerHTML = `
                <h3>Management Plan</h3>
                <p>${data.management_plan}</p>
            `;
        })
        .catch(error => {
            console.error("Error:", error);
            responseOutput.innerHTML = `<p>There was an error processing your request.</p>`;
        });
    });
});
