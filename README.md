# Funke Lab website

To build and host locally:
```sh
uv run build.py
python3 -m http.server 8000 --directory _site
```

## Content

All content is provided by markdown files.

### Projects

Markdown files in `content/projects/`:

```markdown
---
title: Project Title
description: Longer description
image: /assets/img/teasers/project_teaser.png
order: 1
---

Any other markdown comes here and will be rendered to HTML. Citations are
supported anywhere using their BibTeX key as [@bibtex_key].
```

`description`, `image`, and `order` are optional; lower orders appear first.

### People

Markdown files in `content/people/`:

```markdown
---
name: Jan Funke
role: Group Leader
status: member
image: /assets/img/people/jan.jpg
joined: 2018-06-01
order: 1
---

[Email](mailto:funkej@janelia.hhmi.org)
```

`name` and `status` is required (`member` or `alumni`).
The body can contain a bio and ordinary Markdown links.

### Blog Articles

Markdown files in `content/blog/<year>/`.

## Publications

Publications are read from the top-level `papers.bib`.

If an entry has the field `selected = {true}` it will be added to the short
list on the home page.

## Deployment

GitHub Actions will build and deploy the static HTML whenever on every upstream
push to `main`.
