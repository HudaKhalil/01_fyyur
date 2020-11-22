from flask_wtf import CsrfProtect
# Fix Missing CSRF Token Issues with Flask
# Source: https://nickjanetakis.com/blog/fix-missing-csrf-token-issues-with-flask
csrf = CsrfProtect()
