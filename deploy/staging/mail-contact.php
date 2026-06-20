<?php

require_once __DIR__ . '/mail-config.php';

xshield_require_post();

// #region agent log
xshield_debug_log(
    'mail-contact.php:entry',
    'contact handler invoked',
    [
        'method' => $_SERVER['REQUEST_METHOD'] ?? '',
        'hasName' => isset($_POST['name']),
        'hasEmail' => isset($_POST['email']),
        'hasMessage' => isset($_POST['message']),
    ],
    'C'
);
// #endregion

$name = xshield_sanitize_text($_POST['name'] ?? '', 120);
$email = xshield_sanitize_email($_POST['email'] ?? '');
$message = xshield_sanitize_text($_POST['message'] ?? '', 5000);
$page = xshield_sanitize_text($_POST['page'] ?? ($_SERVER['HTTP_REFERER'] ?? ''), 500);

if ($name === '' || $email === '' || $message === '') {
    // #region agent log
    xshield_debug_log(
        'mail-contact.php:validation',
        'contact validation failed',
        ['nameEmpty' => $name === '', 'emailEmpty' => $email === '', 'messageEmpty' => $message === ''],
        'E'
    );
    // #endregion
    xshield_json_response(false, 'Please fill in all required fields.', 400);
}

$subject = 'XShield Website — Contact Form Message';

$body = "A new contact form message was submitted on " . XSHIELD_SITE_NAME . ".\n\n";
$body .= "Name: {$name}\n";
$body .= "Email: {$email}\n\n";
$body .= "Message:\n{$message}\n";
$body .= xshield_mail_footer($page);

if (xshield_send_mail($subject, $body, $email, $name)) {
    // #region agent log
    xshield_debug_log('mail-contact.php:success', 'contact mail sent', [], 'B');
    // #endregion
    xshield_json_response(true, 'Thank you. We\'ll be in touch shortly.');
}

// #region agent log
xshield_debug_log('mail-contact.php:failure', 'contact mail() returned false', [], 'B');
// #endregion
xshield_json_response(false, 'Something went wrong. Please call +971 4 410 6502 or WhatsApp us.', 500);
