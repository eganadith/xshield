XShield — cPanel Git Deployment (from scratch)
==============================================

Live site:  https://xshield-services.com
GitHub:     https://github.com/eganadith/xshield.git
Branch:     main

WHAT GETS DEPLOYED (16 pages + assets)
--------------------------------------
  index.html, about.html, service.html, contact.html
  inquiry/*.html (12 service pages)
  mail-config.php, mail-contact.php, mail-newsletter.php
  robots.txt, sitemap.xml
  deploy/.htaccess  →  public_html/.htaccess
  assets/           →  public_html/assets/  (CSS, JS, images, video)


PART 1 — LOCAL (your Mac, before every deploy)
----------------------------------------------

  cd /path/to/glowz

  1. Build production files:
       chmod +x build.sh scripts/*.sh
       ./build.sh

  2. Verify nothing is missing:
       ./scripts/verify-build.sh

  3. Commit and push to GitHub:
       git add -A
       git commit -m "Deploy update"
       git push origin main

  IMPORTANT: cPanel does NOT run ./build.sh. You must build locally and
  commit the built HTML, CSS, robots.txt, and sitemap.xml before pushing.


PART 2 — cPanel Git Version Control (first-time setup)
------------------------------------------------------

  1. Log in to GoDaddy → cPanel.

  2. Open "Git Version Control".

  3. Click "Create".

  4. Clone the repository:
       Clone URL:     https://github.com/eganadith/xshield.git
       Repository Path:  xshield
         (creates ~/xshield or ~/repositories/xshield — either is fine)
       Branch:        main

  5. Click "Create" / "Clone".

  6. Confirm .cpanel.yml exists in the repo root (cPanel reads this automatically).


PART 3 — Deploy to public_html
------------------------------

  1. In Git Version Control, click "Manage" on the xshield repo.

  2. Click "Pull or Deploy" → "Update from Remote" (pulls latest from GitHub).

  3. Click "Deploy HEAD Commit".

  cPanel runs .cpanel.yml which executes scripts/cpanel-sync.sh and copies
  files to public_html.

  Deploy path (already in .cpanel.yml):
       /home/iq5yfetciw4z/public_html/

  If deploy fails with wrong path, edit .cpanel.yml DEPLOYPATH to match your
  cPanel home directory (File Manager → public_html → path in address bar).


PART 4 — Re-deploy after future changes
---------------------------------------

  On Mac:
    ./build.sh
    ./scripts/verify-build.sh
    git add -A && git commit -m "..." && git push

  On cPanel:
    Git Version Control → Manage → Update from Remote → Deploy HEAD Commit


PART 5 — Verify live site
-------------------------

  https://xshield-services.com/
  https://xshield-services.com/contact.html
  https://xshield-services.com/inquiry/cockroach-control
  https://xshield-services.com/robots.txt
  https://xshield-services.com/sitemap.xml

  Test contact form and newsletter → contact@xshield-services.com


TROUBLESHOOTING
---------------

  Deploy error "Missing deploy/.htaccess"
    → Run ./build.sh locally; ensure deploy/.htaccess is committed and pushed.

  Site shows old content
    → Hard refresh (Cmd+Shift+R). Confirm you pushed AND deployed HEAD on cPanel.

  HTTPS redirect loop
    → In deploy/.htaccess, comment out the HTTPS RewriteRule until SSL is active
      in GoDaddy, then redeploy.

  Video not playing
    → Confirm assets/images/video.mp4 and video.webm exist after deploy.

  Optional manual zip upload (backup method):
    ./build-deploy.sh
    Upload xshield-cpanel-deploy.zip via File Manager → public_html → Extract.
