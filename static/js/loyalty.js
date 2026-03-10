async function joinLoyalty() {
    if (!confirm("Postanite član programa lojalnosti i sakupljajte poene uz svaku rezervaciju. Da li želite da se učlanite?")) return;

    // Uzimamo CSRF token iz kolačića (Django standard)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
                      || getCookie('csrftoken');

    try {
        const response = await fetch('/api/loyalty/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}) // Šaljemo prazan body jer DRF uzima user-a iz request-a
        });

        if (response.ok) {
            // Uspešno kreirano! Osvežavamo stranicu da se pojavi Dashboard verzija dugmeta
            window.location.reload();
        } else {
            const data = await response.json();
            alert("Greška: " + (data.detail || "Neuspešno učlanjenje"));
        }
    } catch (error) {
        console.error("Greška pri pozivanju API-ja:", error);
    }
}

// Pomoćna funkcija za uzimanje tokena ako nije u hidden field-u
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
/*--------------------------------------------------------------------------------------------------------------------*/

function toggleLoyaltyDashboard() {
    const dashboard = document.getElementById('loyalty-dashboard-wrapper');

    if (dashboard.style.display === 'none' || dashboard.style.display === '') {
        dashboard.style.display = 'block';
    } else {
        dashboard.style.display = 'none';
    }
}
/*--------------------------------------------------------------------------------------------------------------------*/

async function leaveLoyalty(id) {
    if (!confirm("Napuštanjem programa gubite sve trenutno sakupljene poene i pogodnosti. Da li ste sigurni da želite da nastavite?")) return;

    const response = await fetch(`/api/loyalty/${id}/`, {
        method: 'DELETE',
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
    });

    if (response.ok) {
        window.location.reload();
    }
}

async function claimVoucher(id) {
    const response = await fetch(`/api/loyalty/${id}/claim_voucher/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
        const data = await response.json();
        document.getElementById('display-code').innerText = data.code;
        document.getElementById('voucher-modal').style.display = 'flex';
    } else {
        alert("Greška pri kreiranju vaučera.");
    }
}

function closeVoucher() {
    document.getElementById('voucher-modal').style.display = 'none';
    window.location.reload(); // Osvežavamo da se resetuju poeni na dashboardu
}

/*--------------------------------------------------------------------------------------------------------------------*/
async function useVoucher(voucherId) {
    if (confirm("Da li ste sigurni da želite da iskoristite ovaj vaučer? Akcija se ne može poništiti.")) {

        const csrfToken = getCookie('csrftoken');

        try {
            const response = await fetch(`/api/loyalty/use-voucher/${voucherId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();

            if (data.status === 'success') {
                location.reload();
            } else {
                alert(data.message);
            }
        } catch (e) {
            console.error(e);
        }
    }
}

/*--------------------------------------------------------------------------------------------------------------------*/
