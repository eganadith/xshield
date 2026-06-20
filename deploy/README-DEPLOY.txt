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
  - mail-contact.php (contact form)
  - assets/ (images, CSS, JS, fonts, video)
  - .htaccess (caching + clean /inquiry/slug URLs)

After upload, test:
  https://yourdomain.com/
  https://yourdomain.com/contact.html
  Submit the contact form and check contact@xshieldservices.com

If the contact form does not send email, create the mailbox in
cPanel → Email Accounts and check spam folder.
