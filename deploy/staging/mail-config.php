<?php

define('XSHIELD_MAIL_TO', 'contact@xshield-services.com');
define('XSHIELD_MAIL_FROM', 'contact@xshield-services.com');
define('XSHIELD_MAIL_FROM_NAME', 'XShield Website');
define('XSHIELD_SITE_NAME', 'xshield-services.com');

// #region agent log
function xshield_debug_log($location, $message, $data = [], $hypothesisId = 'B')
{
    $entry = [
        'sessionId' => 'ca5b13',
        'runId' => 'mail-handler',
        'hypothesisId' => $hypothesisId,
        'location' => $location,
        'message' => $message,
        'data' => $data,
        'timestamp' => (int) round(microtime(true) * 1000),
    ];

    $paths = [
        __DIR__ . '/.cursor/debug-ca5b13.log',
        sys_get_temp_dir() . '/xshield-debug-ca5b13.log',
    ];

    foreach ($paths as $path) {
        $dir = dirname($path);
        if (!is_dir($dir) && !@mkdir($dir, 0755, true)) {
            continue;
        }

        if (@file_put_contents($path, json_encode($entry) . PHP_EOL, FILE_APPEND | LOCK_EX) !== false) {
            break;
        }
    }
}
// #endregion

function xshield_json_response($success, $message, $status = 200)
{
    http_response_code($status);
    header('Content-Type: application/json; charset=UTF-8');
    echo json_encode([
        'success' => (bool) $success,
        'message' => $message,
    ]);
    exit;
}

function xshield_require_post()
{
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        xshield_json_response(false, 'Method not allowed.', 405);
    }
}

function xshield_sanitize_email($email)
{
    $email = trim((string) $email);
    $email = filter_var($email, FILTER_SANITIZE_EMAIL);

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        return '';
    }

    return $email;
}

function xshield_sanitize_text($value, $maxLength = 5000)
{
    $value = trim((string) $value);
    $value = str_replace(["\r\n", "\r"], "\n", $value);
    $value = preg_replace("/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u", '', $value);

    if (strlen($value) > $maxLength) {
        $value = substr($value, 0, $maxLength);
    }

    return $value;
}

function xshield_send_mail($subject, $body, $replyToEmail = '', $replyToName = '')
{
    $headers = [
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'From: ' . XSHIELD_MAIL_FROM_NAME . ' <' . XSHIELD_MAIL_FROM . '>',
    ];

    if ($replyToEmail !== '') {
        $replyName = $replyToName !== '' ? $replyToName : $replyToEmail;
        $headers[] = 'Reply-To: ' . $replyName . ' <' . $replyToEmail . '>';
    }

    $headers[] = 'X-Mailer: PHP/' . phpversion();

    $sent = @mail(XSHIELD_MAIL_TO, $subject, $body, implode("\r\n", $headers));

    // #region agent log
    xshield_debug_log(
        'mail-config.php:xshield_send_mail',
        'mail() result',
        [
            'sent' => (bool) $sent,
            'to' => XSHIELD_MAIL_TO,
            'subject' => $subject,
        ],
        'B'
    );
    // #endregion

    return $sent;
}

function xshield_mail_footer($page = '')
{
    $lines = [
        '',
        '---',
        'Site: ' . XSHIELD_SITE_NAME,
        'Submitted: ' . date('Y-m-d H:i:s T'),
        'IP: ' . ($_SERVER['REMOTE_ADDR'] ?? 'unknown'),
    ];

    if ($page !== '') {
        $lines[] = 'Page: ' . $page;
    }

    return implode("\n", $lines);
}
