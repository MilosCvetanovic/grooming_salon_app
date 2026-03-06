document.addEventListener('DOMContentLoaded', function() {

    AOS.init();

    const hamburger = document.getElementById('hamburger');
    const nav = document.getElementById('headerNav');
    const closeNav = document.getElementById('close');
    const overlay = document.getElementById('overlay');
    hamburger.addEventListener('click', () => {
        nav.classList.toggle('show');
        document.body.classList.toggle('freeze');
        overlay.classList.toggle('show');
    });

    closeNav.addEventListener('click', () => {
        closeMenu();
    });

    window.addEventListener('click', (e) => {
        if (e.target !== nav && !nav.contains(e.target) && e.target !== hamburger) {
            closeMenu();
        }
    });


    const headerAnchors = document.querySelectorAll('#headerNav a');
    const footerAnchors = document.querySelectorAll('#footerNav a');

    const allAnchors = [...headerAnchors, ...footerAnchors];
    allAnchors.forEach((anchor) => {
        const target = anchor.getAttribute('href');
        if (target && anchor.getAttribute('target') !== '_blank' && anchor.title !== 'Email') {
            anchor.addEventListener('click', (e) => {
                if (nav.classList.contains('show')) {
                    closeMenu();
                }

                const hash = target.includes('#') ? '#' + target.split('#')[1] : target;
                const targetElement = document.querySelector(hash);

                // Ako element ne postoji na ovoj stranici, dozvoli normalnu navigaciju
                if (!targetElement) return;

                e.preventDefault();
                targetElement.scrollIntoView({behavior: 'smooth'});
            });
        }
    });


    function closeMenu() {
        nav.classList.remove('show');
        document.body.classList.remove('freeze');
        overlay.classList.remove('show');
    }


    if (document.querySelector('.glideOne')) {
        const glide = new Glide('.glideOne', {
            hoverpause: true,
            type: 'carousel',
            perView: 4,
            gap: 25,
            keyboard: true,
            focusAt: 0,
            breakpoints: {
                768: {
                    perView: 2,
                    gap: 10,
                    focusAt: 0
                },
                550: {
                    perView: 2,
                    gap: 10,
                    focusAt: 0
                },
                450: {
                    perView: 1,
                    gap: 10,
                    focusAt: 0
                }
            }
        });
        glide.mount();
    }
})
    /************************************************************/
/* Drop down on click for avatar profile picture and logout button */
document.addEventListener('DOMContentLoaded', function () {
    const avatarContainer = document.querySelector('.avatar-container.has-dropdown');

    if (avatarContainer) {
        const avatarLink = document.getElementById('avatar-link');

        // Klik na avatar otvara/zatvara dropdown
        avatarLink.addEventListener('click', function (e) {
            e.preventDefault();
            avatarContainer.classList.toggle('open');
        });

        // Klik bilo gde van avatara zatvara dropdown
        document.addEventListener('click', function (e) {
            if (!avatarContainer.contains(e.target)) {
                avatarContainer.classList.remove('open');
            }
        });
    }
});
