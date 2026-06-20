XShield — cPanel Git deployment
================================

Before every push:
  ./build.sh

Then commit built files and push:
  git add -A
  git commit -m "Your message"
  git push origin main

On cPanel:
  1. Git Version Control → open the xshield repo
  2. Pull or Update (if needed)
  3. Deploy HEAD Commit

.cpanel.yml runs scripts/cpanel-sync.sh, which copies:
  - index.html, about.html, service.html, contact.html
  - inquiry/*.html (12 pages)
  - mail-config.php, mail-contact.php, mail-newsletter.php
  - robots.txt, sitemap.xml
  - deploy/.htaccess → public_html/.htaccess
  - assets/ (excluding .scss source files)

Live site: https://xshield-services.com
