/**
 * Univerzalna funkcija za preview slike i resetovanje delete checkbox-a
 * @param {string} inputId - ID file input polja
 * @param {string} previewSelector - CSS selektor za <img> tag gde ide preview
 * @param {string} fileNameSelector - CSS selektor za <span> gde piše ime fajla
 * @param {string} checkboxName - Name atribut za "remove" checkbox
 */
function setupImagePreview(inputId, previewSelector, fileNameSelector, checkboxName) {
    const photoInput = document.getElementById(inputId);
    if (!photoInput) return;

    photoInput.addEventListener('change', function() {
        const file = this.files[0];
        const previewImg = document.querySelector(previewSelector);
        const fileNameDisp = document.querySelector(fileNameSelector);
        const removeCheckbox = document.querySelector(`input[name="${checkboxName}"]`);

        if (file) {
            // 1. Ažuriraj ime fajla
            if (fileNameDisp) {
                fileNameDisp.textContent = file.name;
            }

            // 2. Generiši preview
            const reader = new FileReader();
            reader.onload = function(e) {
                if (previewImg) {
                    previewImg.src = e.target.result;

                    // --- DODATO: Otkrivanje X dugmeta ---
                    // Tražimo labelu (X) koja se nalazi u istom thumbnail-wrapperu kao i slika
                    const wrapper = previewImg.closest('.thumbnail-wrapper');
                    if (wrapper) {
                        const deleteBtn = wrapper.querySelector('.delete-trigger-clean');
                        if (deleteBtn) {
                            // Poništavamo Django-ov inline 'display: none'
                            deleteBtn.style.display = 'flex';
                        }
                    }
                }
            }
            reader.readAsDataURL(file);

            // 3. Resetuj "Remove" checkbox ako postoji
            if (removeCheckbox) {
                removeCheckbox.checked = false;
                // Pokrećemo event da bi CSS (checkbox hack) odreagovao i prikazao sliku
                removeCheckbox.dispatchEvent(new Event('change'));
            }
        }
    });

    // Dodaj ovo unutar setupImagePreview ili kao poseban deo koda
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-trigger-clean')) {
            // Pronađi file input (možeš ga tražiti preko ID-a koji koristiš)
            const photoInput = document.getElementById('photo-input');
            if (photoInput) {
                photoInput.value = ""; // Ovo je ključna linija!
            }

            // Opciono: Ako želiš da vratiš text na "Nema slike" odmah
            const fileNameDisp = document.querySelector('.file-name-val');
            if (fileNameDisp) {
                fileNameDisp.textContent = "Nema fotografije";
            }
        }
    });
}