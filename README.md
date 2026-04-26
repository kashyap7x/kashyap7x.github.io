# Personal Website

This repository contains the source files for
[kashyap7x.github.io](https://kashyap7x.github.io/), a static personal
academic website generated from BibTeX data.

The site is based on Michael Niemeyer's lightweight homepage generator:
<https://github.com/m-niemeyer/m-niemeyer.github.io>.

## Build

Install the Python dependency:

```bash
pip install -r requirements.txt
```

Generate the static pages:

```bash
python build.py
```

The build script reads `publication_list.bib` and `talk_list.bib`, then writes:

- `index.html`
- `publications.html`
- `talks.html`

The homepage also fetches the two latest Substack posts from the configured
Substack handle and caches their display metadata in `substack_posts.json`.

## Repository Structure

- `build.py` - website generator and shared HTML template
- `requirements.txt` - Python build dependency
- `authors.json` - linked author names and profile URLs
- `assets/site.css` - shared site styling
- `publication_list.bib` - publication data
- `talk_list.bib` - talk data
- `substack_posts.json` - cached Substack post metadata used if the feed is unavailable
- `assets/img/profile.jpg` - profile photo
- `assets/img/publications/` - publication thumbnails
- `assets/img/talks/` - talk thumbnails
- `assets/pdf/` - PDFs, posters, and slides
- `colors.csv` - reference color palette

## Updating Content

To add a publication:

1. Add a BibTeX entry to `publication_list.bib`.
2. Add the thumbnail image to `assets/img/publications/`.
3. Add any linked PDFs, posters, or supplementary files to `assets/pdf/`.
4. Add the author to `authors.json` if they should link to a personal page and
   are not already listed.
5. Add `highlight = {true}` if the publication should appear on the homepage.
6. Run `python build.py`.

To add a talk:

1. Add a BibTeX entry to `talk_list.bib`.
2. Add the thumbnail image to `assets/img/talks/`.
3. Add slides to `assets/pdf/talks/` if available.
4. Add `highlight = {true}` if the talk should appear on the homepage.
5. Run `python build.py`.

To update profile text, links, or footer content, edit `get_personal_data()` in
`build.py` and run `python build.py`.

The Substack homepage section uses the `substack` handle from
`get_personal_data()`. Running `python build.py` refreshes the latest post
titles, subtitles, and preview images from Substack when the feed is reachable.

## Custom Fields

Publication entries can include:

- `img` - thumbnail path
- `html` - project page URL
- `pdf` - paper PDF
- `code` - code repository URL
- `video` - video URL
- `supp` - supplementary material
- `poster` - poster PDF
- `highlight` - show on homepage when set to `{true}`
- `award` - award text displayed after the title
- `equal_contribution` - number of first authors marked with asterisks

Talk entries can include:

- `img` - thumbnail path
- `slides` - slides PDF
- `video` - video URL
- `highlight` - show on homepage when set to `{true}`
