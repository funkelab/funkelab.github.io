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
links:
  email: jan.funke@fht.org
  scholar: https://scholar.google.com/citations?user=7rqAapgAAAAJ
  orcid: https://orcid.org/0000-0003-4388-7783
  bluesky: https://bsky.app/profile/janfunkey.bsky.social
  github: https://github.com/funkelab
  website: https://funkelab.github.io/
---

Optional text goes here.
```

`name` and `status` is required (`member` or `alumni`). The optional `links`
mapping is available as `person.links` in the template.

### Blog Articles

Markdown files in `content/blog/<year>/`.

Each post requires an `author` matching a filename in `content/people/`,
without the `.md` extension.

## Publications

Publications are read from the top-level `papers.bib`.

If an entry has the field `selected = {true}` it will be added to the short
list on the home page.

## Deployment

GitHub Actions will build and deploy the static HTML on every upstream push to
`main`.

## Acknowledgements

Icons in `templates/icons/` are from [Font Awesome Free
6.7.2](https://github.com/FortAwesome/Font-Awesome/tree/6.7.2), by Fonticons,
Inc., licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The Google Scholar SVG is from [Academicons by James
Walsh](https://github.com/jpswalsh/academicons/blob/master/svg/google-scholar.svg),
licensed under [SIL OFL 1.1](https://openfontlicense.org/).
