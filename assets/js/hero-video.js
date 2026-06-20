(function () {
    'use strict';

    var video = document.querySelector('.video-hero__bg');
    if (!video) {
        return;
    }

    var soundToggle = document.querySelector('.video-hero__sound-toggle');
    var CACHE_BUST = '20260620b';
    var MP4_SRC = 'assets/images/video.mp4?v=' + CACHE_BUST;
    var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
        (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    var isMobile = window.matchMedia('(max-width: 767px)').matches;

    video.muted = true;
    video.defaultMuted = true;
    video.setAttribute('playsinline', '');
    video.setAttribute('webkit-playsinline', '');
    video.setAttribute('x-webkit-airplay', 'allow');

    function configureSources() {
        var sources = video.querySelectorAll('source');
        var i;
        var mp4Source = null;

        for (i = 0; i < sources.length; i += 1) {
            if (sources[i].type === 'video/webm' && (isIOS || isMobile)) {
                sources[i].remove();
                continue;
            }

            if (sources[i].type === 'video/mp4') {
                mp4Source = sources[i];
                sources[i].src = MP4_SRC;
            }
        }

        if (!mp4Source) {
            mp4Source = document.createElement('source');
            mp4Source.src = MP4_SRC;
            mp4Source.type = 'video/mp4';
            video.appendChild(mp4Source);
        }

        video.load();
    }

    function playVideo() {
        var promise = video.play();
        if (promise && typeof promise.catch === 'function') {
            promise.catch(function () {});
        }
    }

    function reloadVideo() {
        configureSources();
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

    configureSources();

    video.addEventListener('error', function () {
        var mp4 = video.querySelector('source[type="video/mp4"]');
        if (mp4 && mp4.src.indexOf('video.mp4') === -1) {
            mp4.src = MP4_SRC;
            video.load();
            playVideo();
        }
    });

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

    document.addEventListener('touchstart', playVideo, { once: true, passive: true });
    document.addEventListener('click', playVideo, { once: true });
})();
