<?php

require_once __DIR__ . '/mail-config.php';

xshield_require_post();

$name = xshield_sanitize_text($_POST['name'] ?? '', 120);
$email = xshield_sanitize_email($_POST['email'] ?? '');
$message = xshield_sanitize_text($_POST['message'] ?? '', 5000);
$page = xshield_sanitize_text($_POST['page'] ?? ($_SERVER['HTTP_REFERER'] ?? ''), 500);

if ($name === '' || $email === '' || $message === '') {
    xshield_json_response(false, 'Please fill in all required fields.', 400);
}

$subject = 'XShield Website — Contact Form Message';

$body = "A new contact form message was submitted on " . XSHIELD_SITE_NAME . ".\n\n";
$body .= "Name: {$name}\n";
$body .= "Email: {$email}\n\n";
$body .= "Message:\n{$message}\n";
$body .= xshield_mail_footer($page);

if (xshield_send_mail($subject, $body, $email, $name)) {
    xshield_json_response(true, 'Thank you. We\'ll be in touch shortly.');
}

xshield_json_response(false, 'Something went wrong. Please call +971 4 410 6502 or WhatsApp us.', 500);
