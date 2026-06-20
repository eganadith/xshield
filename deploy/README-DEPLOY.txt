XShield Pest Control — GoDaddy cPanel Deployment
================================================

1. Log in to GoDaddy → Hosting → cPanel → File Manager
2. Open public_html
3. Back up any existing site (optional)
4. Upload xshield-cpanel-deploy.zip
5. Right-click the zip → Extract
6. Move all files from the extracted folder into public_html
   (index.html must sit directly in public_html, not in a subfolder)

Files included:
  - index.html, about.html, service.html, contact.html
  - inquiry/ (12 service inquiry pages with WhatsApp prefill)
  - mail-config.php, mail-contact.php, mail-newsletter.php
  - assets/ (images, CSS, JS, fonts, video)
  - .htaccess (caching + clean /inquiry/slug URLs)

Email setup (required for forms to work)
----------------------------------------
1. In cPanel → Email Accounts, create:
   contact@xshield-services.com
2. Upload all PHP mail files to public_html (same folder as index.html).
3. Forms send to contact@xshield-services.com:
   - Contact form on contact.html
   - Newsletter signup in the footer on every live page

After upload, test:
  https://xshield-services.com/
  https://xshield-services.com/contact.html
  Submit the contact form and subscribe via the footer newsletter.
  Check contact@xshield-services.com (and spam/junk).

If email does not arrive:
  - Confirm the mailbox exists in cPanel
  - Confirm PHP mail files are in public_html (not inside a subfolder)
  - Check cPanel → Track Delivery or Email Deliverability
  - Try sending a test from webmail to the same address
