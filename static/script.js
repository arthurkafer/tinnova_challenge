document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/chart_data')
        .then(response => response.json())
        .then(data => {
            renderDecadeChart(data.decades);
            renderBrandChart(data.brands);
        })
        .catch(error => console.error('Error fetching chart data:', error));
});

function renderDecadeChart(decadeData) {
    const ctx = document.getElementById('decadeChart')?.getContext('2d');
    if (!ctx) return;

    const labels = decadeData.map(d => d.name);
    const counts = decadeData.map(d => d.count);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Vehicles by Decade',
                data: counts,
                backgroundColor: 'rgba(54, 162, 235, 0.6)', // Blue
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                borderRadius: 4,
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1 // Ensure y-axis shows whole numbers for counts
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.raw}`;
                        }
                    }
                }
            }
        }
    });
}

function renderBrandChart(brandData) {
    const ctx = document.getElementById('brandChart')?.getContext('2d');
    if (!ctx) return;

    const labels = brandData.map(b => b.name);
    const counts = brandData.map(b => b.count);

    new Chart(ctx, {
        type: 'bar', // Could also be 'pie' or 'doughnut' for brand distribution
        data: {
            labels: labels,
            datasets: [{
                label: 'Vehicles by Brand',
                data: counts,
                backgroundColor: 'rgba(75, 192, 192, 0.6)', // Teal/Green
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                borderRadius: 4,
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            indexAxis: 'y', // Makes it a horizontal bar chart, good for many brands
            scales: {
                x: { // For horizontal bar chart, x-axis is the value axis
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.raw}`;
                        }
                    }
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.action-button.delete').forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const confirmed = confirm("Are you sure you want to delete this vehicle?");
            if (!confirmed) return;

            fetch(`/veiculos/${id}`, {
                method: 'DELETE',
            })
            .then(res => {
                if (!res.ok) throw new Error("Delete failed");
                return res.json();
            })
            .then(() => {
                window.location.reload();
            })
            .catch(err => {
                console.error("Error deleting vehicle", err);
                alert("Failed to delete vehicle.");
            });
        });
    });

    document.querySelectorAll('.status-button').forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const newStatus = this.getAttribute('data-vendido') === 'true';

            fetch(`/veiculos/${id}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ vendido: newStatus })
            })
            .then(res => {
                if (!res.ok) throw new Error("Failed to update status");
                return res.json();
            })
            .then(() => {
                window.location.reload();
            })
            .catch(err => {
                console.error("Update failed", err);
                alert("Failed to update vehicle status.");
            });
        });
    });

    const addForm = document.getElementById('add-vehicle-form');
    if (addForm) {
        addForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(addForm);
            const payload = {
                veiculo: formData.get('veiculo'),
                marca: formData.get('marca'),
                ano: parseInt(formData.get('ano')),
                cor: formData.get('cor'),
                descricao: formData.get('descricao'),
                vendido: formData.get('vendido') === 'on'
            };

            fetch('/veiculos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })
            .then(res => {
                if (!res.ok) throw new Error("Failed to add vehicle");
                return res.json();
            })
            .then(() => {
                alert("Vehicle added successfully!");
                window.location.reload();
            })
            .catch(err => {
                console.error("Add vehicle failed:", err);
                alert("Failed to add vehicle.");
            });
        });
    }

    const editForm = document.getElementById('edit-vehicle-form');
    if (editForm) {
        editForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(editForm);
            const payload = {
                veiculo: formData.get('vehicleName'),
                marca: formData.get('brand'),
                ano: parseInt(formData.get('year')),
                descricao: formData.get('description'),
                vendido: formData.get('sold') === 'on'
            };

            const actionUrl = editForm.getAttribute('action');

            fetch(actionUrl, {
                method: 'PUT', 
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })
            .then(res => {
                if (!res.ok) throw new Error("Failed to update vehicle");
                return res.json();
            })
            .then(() => {
                alert("Vehicle updated successfully!");
                window.location.href = '/'; // Redirect to home or list page
            })
            .catch(err => {
                console.error("Update failed:", err);
                alert("Failed to update vehicle.");
            });
        });
    }
});

// Simple confirmation for delete, already in HTML, but could be enhanced here.
// const deleteForms = document.querySelectorAll('form[action*="/delete_vehicle/"]');
// deleteForms.forEach(form => {
//     form.addEventListener('submit', function(event) {
//         if (!confirm('Are you sure you want to delete this vehicle?')) {
//             event.preventDefault();
//         }
//     });
// });

// Handle setting max year for year input dynamically
const yearInput = document.getElementById('year');
if (yearInput) {
    const currentYear = new Date().getFullYear();
    yearInput.max = currentYear + 1; // Allow next year for upcoming models
    if (!yearInput.value) { // Set default to current year if empty (for add form)
        // yearInput.value = currentYear; // Optional: default to current year
    }
}
