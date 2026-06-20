(function () {
    'use strict';

    var video = document.querySelector('.video-hero__bg');
    if (!video) {
        return;
    }

    var soundToggle = document.querySelector('.video-hero__sound-toggle');
    var CACHE_BUST = '20260620c';
    var WEBM_SRC = 'assets/images/video.webm?v=' + CACHE_BUST;
    var MP4_SRC = 'assets/images/video.mp4?v=' + CACHE_BUST;
    var MOBILE_QUERY = window.matchMedia('(max-width: 767px)');
    var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
        (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    var activeMode = '';

    video.muted = true;
    video.defaultMuted = true;
    video.setAttribute('playsinline', '');
    video.setAttribute('webkit-playsinline', '');
    video.setAttribute('x-webkit-airplay', 'allow');

    function isMobileViewport() {
        return MOBILE_QUERY.matches || isIOS;
    }

    function supportsWebM() {
        var probe = document.createElement('video');
        return probe.canPlayType('video/webm; codecs="vp9"') !== '' ||
            probe.canPlayType('video/webm; codecs="vp8"') !== '' ||
            probe.canPlayType('video/webm') !== '';
    }

    function clearSources() {
        var nodes = video.querySelectorAll('source');
        var i;
        for (i = 0; i < nodes.length; i += 1) {
            nodes[i].remove();
        }
    }

    function addSource(src, type) {
        var source = document.createElement('source');
        source.src = src;
        source.type = type;
        video.appendChild(source);
        return source;
    }

    function currentMode() {
        return isMobileViewport() ? 'mobile' : 'desktop';
    }

    function configureSources() {
        var mode = currentMode();
        clearSources();

        if (mode === 'mobile') {
            addSource(MP4_SRC, 'video/mp4');
        } else if (supportsWebM()) {
            addSource(WEBM_SRC, 'video/webm');
        } else {
            addSource(MP4_SRC, 'video/mp4');
        }

        activeMode = mode;
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

    function onViewportChange() {
        if (currentMode() !== activeMode) {
            reloadVideo();
        }
    }

    configureSources();

    video.addEventListener('error', function () {
        var webm = video.querySelector('source[type="video/webm"]');
        var mp4 = video.querySelector('source[type="video/mp4"]');

        if (webm && !mp4) {
            addSource(MP4_SRC, 'video/mp4');
            video.load();
            playVideo();
            return;
        }

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

    if (typeof MOBILE_QUERY.addEventListener === 'function') {
        MOBILE_QUERY.addEventListener('change', onViewportChange);
    } else if (typeof MOBILE_QUERY.addListener === 'function') {
        MOBILE_QUERY.addListener(onViewportChange);
    }

    window.addEventListener('resize', onViewportChange);
    document.addEventListener('touchstart', playVideo, { once: true, passive: true });
    document.addEventListener('click', playVideo, { once: true });
})();
