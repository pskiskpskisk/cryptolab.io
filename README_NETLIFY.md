Netlify deployment notes

- Netlify is primarily static-hosting. A full Flask app cannot be hosted as a server on Netlify directly.
- Options:
  1) Deploy this Flask app to a Python-friendly host (Render, Railway, Fly, Heroku) and set Netlify as CDN/static if needed.
  2) Convert Python logic to run client-side (Pyodide) and keep a static frontend on Netlify.
  3) Use Netlify Functions with a custom build to run Python serverless functions (advanced).

Recommended quick path:
1. Push this repo to Git.
2. Create a Render (or Railway) service, choose "Python/Flask" and point to this repo; set `pip install -r requirements.txt` and start command `gunicorn app:app`.
3. Keep Netlify only if you need a separate static frontend; otherwise use Render's URL.
