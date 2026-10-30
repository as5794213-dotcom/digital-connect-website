# Digital Connect website

Static site for Digital Connect (Naigaon East). Netlify runs `python3 build.py` and publishes `site/`.

- Pages and services: `data.py`
- Blog posts: `blogs_a.py`, `blogs_b.py` (each post has a `date`; it goes live on that date, India time)
- A GitHub Action (`.github/workflows/publish.yml`) runs daily at 00:05 IST and triggers a Netlify rebuild when a post is due.
