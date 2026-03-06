function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const csrfToken = getCookie('csrftoken');

/*--------------------------------------------------------------------------------------------------------------------*/
// ─── Fetch i render notifikacija ───────────────────────────────────────────

function fetchNotifications() {
    fetch('/api/notifications/')
        .then(res => res.json())
        .then(data => {
            renderBadge(data.unread_count);
            renderNotificationList(data.notifications);
        })
        .catch(err => console.error('Greška pri učitavanju obaveštenja:', err));
}

function renderBadge(unreadCount) {
    const badge = document.getElementById('unread-badge');
    if (!badge) return;

    if (unreadCount > 0) {
        badge.textContent = unreadCount;
        badge.classList.add('visible');
    } else {
        badge.textContent = '';
        badge.classList.remove('visible');
    }
}

function renderNotificationList(notifications) {
    const list = document.getElementById('notification-list');
    if (!list) return;

    if (notifications.length === 0) {
        list.innerHTML = '<p class="no-notifications">Nema novih obaveštenja.</p>';
        return;
    }

    list.innerHTML = notifications.map(n => `
        <div class="notification-item ${n.is_read ? 'read' : 'unread'}" id="notif-${n.id}">
            <p class="notification-message">${n.message}</p>
            <div class="notification-actions">
                ${!n.is_read
                    ? `<button class="btn-mark-read" onclick="markRead(${n.id})" title="Označi kao pročitano">✓</button>`
                    : ''
                }
                <button class="not-btn-delete" onclick="deleteNotification(${n.id})" title="Obriši">🗑</button>
            </div>
        </div>
    `).join('');
}

/*--------------------------------------------------------------------------------------------------------------------*/
// ─── Toggle dropdown ───────────────────────────────────────────────────────

function toggleNotifications() {
    const dropdown = document.getElementById('notification-dropdown');
    if (!dropdown) return;

    const isHidden = !dropdown.classList.contains('open');

    if (isHidden) {
        dropdown.classList.add('open');
        fetchNotifications();
    } else {
        dropdown.classList.remove('open');
    }
}

// Zatvori dropdown kada korisnik klikne van njega
document.addEventListener('click', function (e) {
    const wrapper = document.getElementById('notification-wrapper');
    if (wrapper && !wrapper.contains(e.target)) {
        const dropdown = document.getElementById('notification-dropdown');
        if (dropdown) dropdown.classList.remove('open');
    }
});

/*--------------------------------------------------------------------------------------------------------------------*/
// ─── API akcije ────────────────────────────────────────────────────────────

function markRead(id) {
    fetch(`/api/notifications/${id}/mark-read/`, {
        method: 'PATCH',
        headers: { 'X-CSRFToken': csrfToken }
    })
        .then(res => {
            if (res.ok) fetchNotifications();
        })
        .catch(err => console.error('Greška pri označavanju:', err));
}

function markAllRead() {
    fetch('/api/notifications/mark-all-read/', {
        method: 'PATCH',
        headers: { 'X-CSRFToken': csrfToken }
    })
        .then(res => {
            if (res.ok) fetchNotifications();
        })
        .catch(err => console.error('Greška pri označavanju svih:', err));
}

function deleteNotification(id) {
    fetch(`/api/notifications/${id}/delete/`, {
        method: 'DELETE',
        headers: { 'X-CSRFToken': csrfToken }
    })
        .then(res => {
            if (res.ok) fetchNotifications();
        })
        .catch(err => console.error('Greška pri brisanju:', err));
}

/*--------------------------------------------------------------------------------------------------------------------*/
// ─── Inicijalizacija ───────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function () {
    const bell = document.getElementById('notification-bell');
    const markAllBtn = document.getElementById('mark-all-btn');

    if (bell) bell.addEventListener('click', toggleNotifications);
    if (markAllBtn) markAllBtn.addEventListener('click', markAllRead);

    // Učitaj badge odmah kada se stranica otvori
    fetchNotifications();
});