XShield Pest Control — Deployment (Git + cPanel)
=================================================

Recommended workflow: GitHub → cPanel Git Version Control

LOCAL (before every push)
-------------------------
1. Run the build:
     ./build.sh

2. Commit built files (especially assets/sass/style.css and inquiry/*.html):
     git add -A
     git commit -m "Your message"
     git push origin main

CPANEL
------
1. cPanel → Git Version Control
2. Clone or connect: https://github.com/eganadith/xshield.git
3. Repository path: e.g. /home/iq5yfetciw4z/repositories/xshield
4. After push, click Pull or Deploy HEAD Commit
5. .cpanel.yml runs scripts/cpanel-sync.sh → copies site files to public_html

What gets deployed to public_html
---------------------------------
  - index.html, about.html, service.html, contact.html
  - inquiry/ (12 service pages)
  - mail-config.php, mail-contact.php, mail-newsletter.php
  - assets/ (compiled CSS, JS, images — no .scss sources)
  - .htaccess (from deploy/.htaccess)

Email (forms)
-------------
Create contact@xshield-services.com in cPanel → Email Accounts.

Test after deploy:
  https://xshield-services.com/
  https://xshield-services.com/contact.html

Optional: manual zip upload
---------------------------
  ./build-deploy.sh
  Upload xshield-cpanel-deploy.zip via File Manager (legacy method).

If DEPLOYPATH changes
---------------------
Edit .cpanel.yml — update DEPLOYPATH to your account's public_html path.
