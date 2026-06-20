<?php

require_once __DIR__ . '/mail-config.php';

xshield_require_post();

// #region agent log
xshield_debug_log(
    'mail-newsletter.php:entry',
    'newsletter handler invoked',
    [
        'hasEmail' => isset($_POST['email']),
        'termsAccepted' => !empty($_POST['terms']),
    ],
    'C'
);
// #endregion

$email = xshield_sanitize_email($_POST['email'] ?? '');
$page = xshield_sanitize_text($_POST['page'] ?? ($_SERVER['HTTP_REFERER'] ?? ''), 500);
$termsAccepted = !empty($_POST['terms']);

if (!$termsAccepted) {
    xshield_json_response(false, 'Please agree to the terms and policies.', 400);
}

if ($email === '') {
    xshield_json_response(false, 'Please enter a valid email address.', 400);
}

$subject = 'XShield Website — Newsletter Subscription';

$body = "A new newsletter subscription was submitted on " . XSHIELD_SITE_NAME . ".\n\n";
$body .= "Email: {$email}\n";
$body .= "Terms accepted: Yes\n";
$body .= xshield_mail_footer($page);

if (xshield_send_mail($subject, $body, $email)) {
    // #region agent log
    xshield_debug_log('mail-newsletter.php:success', 'newsletter mail sent', [], 'B');
    // #endregion
    xshield_json_response(true, 'Thanks for subscribing. We\'ll keep you updated.');
}

// #region agent log
xshield_debug_log('mail-newsletter.php:failure', 'newsletter mail() returned false', [], 'B');
// #endregion
xshield_json_response(false, 'Something went wrong. Please try again later.', 500);
