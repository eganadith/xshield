(function () {
    'use strict';

    var video = document.querySelector('.video-hero__bg');
    if (!video) {
        return;
    }

    var soundToggle = document.querySelector('.video-hero__sound-toggle');

    video.muted = true;
    video.defaultMuted = true;
    video.setAttribute('playsinline', '');
    video.setAttribute('webkit-playsinline', '');

    function playVideo() {
        var promise = video.play();
        if (promise && typeof promise.catch === 'function') {
            promise.catch(function () {});
        }
    }

    function reloadVideo() {
        video.load();
        playVideo();
    }

    function setSoundEnabled(enabled) {
        video.muted = !enabled;
        video.defaultMuted = !enabled;

        if (soundToggle) {
            soundToggle.setAttribute('aria-pressed', enabled ? 'true' : 'false');
            soundToggle.setAttribute('aria-label', enabled ? 'Mute sound' : 'Enable sound');
            soundToggle.setAttribute('title', enabled ? 'Mute sound' : 'Enable sound');
            soundToggle.classList.toggle('is-sound-on', enabled);

            var label = soundToggle.querySelector('.video-hero__sound-label');
            if (label) {
                label.textContent = enabled ? 'Mute sound' : 'Enable sound';
            }
        }
    }

    function toggleSound() {
        setSoundEnabled(video.muted);
        playVideo();
    }

    if (soundToggle) {
        soundToggle.addEventListener('click', toggleSound);
    }

    if (video.readyState >= 2) {
        playVideo();
    } else {
        video.addEventListener('loadeddata', playVideo, { once: true });
        video.addEventListener('canplay', playVideo, { once: true });
    }

    document.addEventListener('visibilitychange', function () {
        if (!document.hidden) {
            playVideo();
        }
    });

    window.addEventListener('pageshow', function (event) {
        if (event.persisted) {
            reloadVideo();
        }
    });
})();
