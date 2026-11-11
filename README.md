# monopaints.com

Website for Altanzul “Mono” Munkhjargal, oil painter. Plain HTML and CSS, served by GitHub Pages. There is no build step.

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| Portfolio | `portfolio/index.html` |
| Statement | `statement/index.html` |
| About (bio and résumé) | `about/index.html` |
| Contact | `contact/index.html` |

Styles are in `assets/site.css`; the portfolio viewer and copy-email button are in `assets/site.js`.

## Preview locally

```bash
python3 -m http.server 8765
```

Then open http://localhost:8765.

## Add or replace a painting

1. Add the photo's path to `WORKS` in `tools/build_images.py` (needs Pillow: `pip install pillow`).
2. Run `python3 tools/build_images.py`. It writes 800px and 1600px copies to `assets/works/` and strips camera metadata such as GPS location.
3. In `portfolio/index.html`, copy an existing `<li>` block and change the file names, `width`/`height`, alt text and caption.

## Domain setup (Squarespace DNS)

GitHub: repository **Settings → Pages**, deploy from the `main` branch, root folder. The `CNAME` file already sets the custom domain to `monopaints.com`. Turn on **Enforce HTTPS** once GitHub has issued the certificate.

Squarespace: **Domains → monopaints.com → DNS settings**.

- Remove the Squarespace default records for `@` and `www`. Keep any MX and TXT records, since they handle email for mono@monopaints.com.
- Add four `A` records for host `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
- Add a `CNAME` record for host `www` pointing to `vermi.github.io`.

DNS changes can take up to a day to spread.
