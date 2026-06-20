(function () {
    'use strict';

    // #region agent log
    function debugLog(location, message, data, hypothesisId) {
        fetch('http://127.0.0.1:7839/ingest/e2e76956-23e9-481b-9ce0-4635f4cf51a6', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Debug-Session-Id': 'ca5b13',
            },
            body: JSON.stringify({
                sessionId: 'ca5b13',
                runId: 'form-client',
                hypothesisId: hypothesisId || 'A',
                location: location,
                message: message,
                data: data || {},
                timestamp: Date.now(),
            }),
        }).catch(function () {});
    }
    // #endregion

    function hideNotice(notice) {
        if (!notice) {
            return;
        }

        notice.textContent = '';
        notice.classList.remove('is-visible', 'is-success', 'is-error');
    }

    function showNotice(notice, message, isSuccess) {
        if (!notice) {
            return;
        }

        notice.textContent = message;
        notice.classList.add('is-visible');
        notice.classList.toggle('is-success', isSuccess);
        notice.classList.toggle('is-error', !isSuccess);
    }

    function postForm(form) {
        var action = form.getAttribute('action');

        if (!action) {
            return Promise.reject(new Error('Missing form action.'));
        }

        var formData = new FormData(form);

        if (!formData.get('page')) {
            formData.set('page', window.location.href);
        }

        return fetch(action, {
            method: 'POST',
            body: formData,
            headers: {
                Accept: 'application/json',
            },
        }).then(function (response) {
            return response.text().then(function (text) {
                var data = null;

                try {
                    data = text ? JSON.parse(text) : null;
                } catch (parseError) {
                    // #region agent log
                    debugLog(
                        'xshield-forms.js:postForm',
                        'non-json response',
                        {
                            action: action,
                            status: response.status,
                            bodyPreview: text.slice(0, 120),
                        },
                        'C'
                    );
                    // #endregion
                    throw parseError;
                }

                // #region agent log
                debugLog(
                    'xshield-forms.js:postForm',
                    'form response',
                    {
                        action: action,
                        status: response.status,
                        success: !!(data && data.success),
                    },
                    'A'
                );
                // #endregion

                return {
                    ok: response.ok,
                    data: data,
                };
            });
        });
    }

    function bindSubmit(form, onSuccess, onError) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            if (!form.checkValidity()) {
                // #region agent log
                debugLog(
                    'xshield-forms.js:bindSubmit',
                    'html validation blocked submit',
                    { action: form.getAttribute('action') || '' },
                    'E'
                );
                // #endregion
                form.reportValidity();
                return;
            }

            var submitButton = form.querySelector('button[type="submit"]');
            var notice = form.querySelector('.xshield-form-notice');

            hideNotice(notice);

            if (submitButton) {
                submitButton.disabled = true;
            }

            postForm(form)
                .then(function (result) {
                    if (result.ok && result.data && result.data.success) {
                        onSuccess(result.data.message || 'Submitted successfully.');
                        form.reset();
                        return;
                    }

                    var errorMessage =
                        (result.data && result.data.message) ||
                        'Something went wrong. Please try again.';

                    onError(errorMessage, notice);
                })
                .catch(function (error) {
                    // #region agent log
                    debugLog(
                        'xshield-forms.js:bindSubmit',
                        'form submit failed',
                        {
                            action: form.getAttribute('action') || '',
                            error: error && error.message ? error.message : 'unknown',
                        },
                        'A'
                    );
                    // #endregion
                    onError('Something went wrong. Please try again.', notice);
                })
                .finally(function () {
                    if (submitButton) {
                        submitButton.disabled = false;
                    }
                });
        });
    }

    var contactForm = document.getElementById('contact-form');

    // #region agent log
    debugLog(
        'xshield-forms.js:init',
        'form handlers initialized',
        {
            hasContactForm: !!contactForm,
            newsletterForms: document.querySelectorAll('.xshield-newsletter-form').length,
            page: window.location.pathname,
        },
        'A'
    );
    // #endregion

    if (contactForm) {
        bindSubmit(
            contactForm,
            function (message) {
                var success = document.getElementById('success');
                var error = document.getElementById('error');

                if (error) {
                    error.style.display = 'none';
                }

                if (success) {
                    success.textContent = message;
                    success.style.display = 'block';
                }
            },
            function (message) {
                var success = document.getElementById('success');
                var error = document.getElementById('error');

                if (success) {
                    success.style.display = 'none';
                }

                if (error) {
                    error.textContent = message;
                    error.style.display = 'block';
                }
            }
        );
    }

    document.querySelectorAll('.xshield-newsletter-form').forEach(function (form) {
        bindSubmit(
            form,
            function (message) {
                showNotice(form.querySelector('.xshield-form-notice'), message, true);
            },
            function (message, notice) {
                showNotice(notice, message, false);
            }
        );
    });
})();
