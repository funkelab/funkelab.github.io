# /// script
# requires-python = ">=3.11"
# dependencies = ["Markdown==3.8.2", "Jinja2==3.1.6", "PyYAML==6.0.2", "pybtex==0.25.1", "pylatexenc==2.10"]
# ///
from pathlib import Path
import re
import shutil

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup, escape
from pybtex.database import parse_file
from pylatexenc.latex2text import LatexNodes2Text

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "_site"
TEMPLATES = Environment(
    loader=FileSystemLoader(ROOT / "templates"),
    autoescape=True,
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)
PAPERS_BIB = ROOT / "papers.bib"


def plain(value):
    """Decode BibTeX braces and LaTeX accents."""
    return LatexNodes2Text().latex_to_text(value)


def publications():
    """Parse the BibTeX file."""
    papers = {}
    for key, entry in parse_file(PAPERS_BIB).entries.items():
        fields = entry.fields
        authors = []
        num_authors_shortened = 1
        authors_shortened = []
        for person in entry.persons.get("author", []):
            authors.append(
                plain(
                    " ".join(
                        person.first_names
                        + person.middle_names
                        + person.prelast_names
                        + person.last_names
                        + person.lineage_names
                    )
                )
            )
            authors_shortened.append(plain(" ".join(person.last_names)))
        authors_shortened = authors_shortened[:num_authors_shortened]
        links = []
        if fields.get("doi"):
            links.append(("DOI", "https://doi.org/" + fields["doi"]))
        for field, label in [
            ("url", "Paper"),
            ("pdf", "PDF"),
            ("code", "Code"),
            ("website", "Website"),
            ("blog", "Blog"),
        ]:
            if fields.get(field):
                links.append((label, plain(fields[field])))
        papers[key] = dict(
            key=key,
            title=plain(fields["title"]),
            authors=", ".join(authors),
            authors_shortened=", ".join(authors_shortened) + " et al.",
            year=fields.get("year", "Undated"),
            venue=plain(
                fields.get(
                    "journal", fields.get("booktitle", fields.get("publisher", ""))
                )
            ),
            abstract=plain(fields.get("abstract", "")),
            links=links,
            selected=fields.get("selected", "").lower() == "true",
            preview=fields.get("preview", None),
        )
    return dict(
        sorted(
            papers.items(), key=lambda item: (item[1]["year"], item[0]), reverse=True
        )
    )


def render_citation(index, paper):
    """Render a citation. The index is the base-1 number of the citation in the
    current page."""

    return f"{paper['authors_shortened']}, {paper['year']}"


def render_markdown(body, papers):
    """Convert markdown into HTML, extract citations and link to papers."""
    cited = []

    def citation(match):
        key = match[1]
        if key not in papers:
            raise ValueError(f"Unknown citation: {key}")
        if key not in cited:
            cited.append(key)
        return f'<a href="#{escape(key)}">{render_citation(cited.index(key) + 1, papers[key])}</a>'

    body = re.sub(r"\[@([^\]\s]+)\]", citation, body)
    html = markdown.markdown(body, extensions=["extra", "sane_lists"])
    return Markup(html), [papers[key] for key in cited]


def read_content(path, papers):
    """Parse a markdown file (e.g., for people, projects) that has a YAML front matter."""
    source = path.read_text(encoding="utf-8")
    if not source.startswith("---\n"):
        raise ValueError(f"{path}: expected YAML front matter")
    _, header, body = source.split("---", 2)
    data = yaml.safe_load(header)
    # a title is required for every other markdown file, but for people we call
    # it "name"
    if "name" in data and "title" not in data:
        data["title"] = data["name"]
    if not isinstance(data, dict) or not data.get("title"):
        raise ValueError(f"{path}: title is required")
    data["body"], data["references"] = render_markdown(body, papers)
    return data


def build():
    """Build static HTML pages from templates and markdown files."""
    papers = publications()
    pages = {}

    def page(url, title, body):
        target = url.lstrip("/")
        target = target if target.endswith(".html") else target + "index.html"
        if target in pages:
            raise ValueError(f"Duplicate page: {url}")
        pages[target] = TEMPLATES.get_template("base.html").render(
            title=title, body=body, url=url
        )

    def section(template, **data):
        return Markup(TEMPLATES.get_template(template).render(**data))

    projects = []
    people = []
    posts = []
    for path in sorted((ROOT / "content").rglob("*.md")):
        data = read_content(path, papers)
        relative = path.relative_to(ROOT / "content").with_suffix("").as_posix()
        if relative.startswith("people/"):
            if data.get("status") not in {"member", "alumni"}:
                raise ValueError(f"{path}: status must be member or alumni")
            people.append(data)
            continue
        url = (
            "/"
            if relative == "index"
            else "/404.html"
            if relative == "404"
            else f"/{relative}/"
        )
        data["url"] = url
        if relative.startswith("projects/"):
            projects.append(data)
        if relative.startswith("blog/"):
            posts.append(data)
        body = section("page.html", page=data)
        if relative == "index":
            body += section(
                "publications.html",
                papers=[p for p in papers.values() if p["selected"]],
                heading="Selected publications",
            )
        page(url, data["title"], body)

    projects.sort(key=lambda p: (p.get("order", 100), p["title"]))
    people.sort(
        key=lambda p: (p.get("order", 100), str(p.get("joined", "")), p["title"])
    )
    posts.sort(key=lambda p: str(p.get("date", "")), reverse=True)
    page("/projects/", "Projects", section("projects.html", projects=projects))
    page("/people/", "People", section("people.html", people=people))
    page("/blog/", "Blog", section("blog.html", posts=posts))
    page(
        "/publications/",
        "Publications",
        section("publications.html", papers=list(papers.values()), heading=""),
    )

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for target, html in pages.items():
        dest = OUTPUT / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
    shutil.copytree(ROOT / "assets", OUTPUT / "assets")
    (OUTPUT / ".nojekyll").touch()
    print(f"Built {len(pages)} pages, {len(papers)} publications → {OUTPUT}")


if __name__ == "__main__":
    build()
