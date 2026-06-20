(function () {
    'use strict';

    function updateNavState(root) {
        var track = root.querySelector('.xshield-apple-carousel__track');
        var prev = root.querySelector('[data-apple-carousel-prev]');
        var next = root.querySelector('[data-apple-carousel-next]');
        if (!track || !prev || !next) return;

        var maxScroll = track.scrollWidth - track.clientWidth;
        prev.disabled = track.scrollLeft <= 4;
        next.disabled = track.scrollLeft >= maxScroll - 4;
    }

    function scrollTrack(root, direction) {
        var track = root.querySelector('.xshield-apple-carousel__track');
        if (!track) return;

        var card = track.querySelector('.xshield-apple-card');
        var gap = 20;
        var amount = card ? card.offsetWidth + gap : 392;

        track.scrollBy({
            left: direction * amount,
            behavior: 'smooth'
        });
    }

    document.querySelectorAll('[data-apple-carousel]').forEach(function (root) {
        var track = root.querySelector('.xshield-apple-carousel__track');
        var prev = root.querySelector('[data-apple-carousel-prev]');
        var next = root.querySelector('[data-apple-carousel-next]');

        if (!track) return;

        if (prev) {
            prev.addEventListener('click', function () {
                scrollTrack(root, -1);
            });
        }

        if (next) {
            next.addEventListener('click', function () {
                scrollTrack(root, 1);
            });
        }

        track.addEventListener('scroll', function () {
            updateNavState(root);
        }, { passive: true });

        window.addEventListener('resize', function () {
            updateNavState(root);
        });

        updateNavState(root);
    });
})();
