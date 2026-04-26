import json
import re
import struct
from email.utils import parsedate_to_datetime
from functools import lru_cache
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from pybtex.database.input import bibtex

from site_config import get_personal_data

AUTHOR_FILE = Path(__file__).with_name("authors.json")
SUBSTACK_CACHE_FILE = Path(__file__).with_name("substack_posts.json")

JPEG_SOF_MARKERS = {
    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
}

def html_attr(value):
    return escape(str(value), quote=True)

def absolute_url(value, site_url):
    site_url = site_url.rstrip("/")
    if not value:
        return f"{site_url}/"
    parsed = urlparse(value)
    if parsed.scheme and parsed.netloc:
        return value
    return urljoin(f"{site_url}/", value.lstrip("/"))

def secure_target_blank(html):
    return re.sub(
        r'target="_blank"(?![^>]*\brel=)',
        'target="_blank" rel="noopener noreferrer"',
        html,
    )

def get_local_path(src):
    parsed = urlparse(src)
    if parsed.scheme or parsed.netloc:
        return None

    site_root = Path(__file__).resolve().parent
    path = (site_root / unquote(parsed.path)).resolve()
    try:
        path.relative_to(site_root)
    except ValueError:
        return None

    return path if path.exists() else None

def read_png_dimensions(path):
    with path.open("rb") as f:
        header = f.read(24)
    if header.startswith(b"\x89PNG\r\n\x1a\n") and header[12:16] == b"IHDR":
        return struct.unpack(">II", header[16:24])
    return None

def read_jpeg_dimensions(path):
    with path.open("rb") as f:
        if f.read(2) != b"\xff\xd8":
            return None

        while True:
            marker_start = f.read(1)
            if not marker_start:
                return None
            if marker_start != b"\xff":
                continue

            marker_byte = f.read(1)
            while marker_byte == b"\xff":
                marker_byte = f.read(1)
            if not marker_byte:
                return None

            marker = marker_byte[0]
            if marker == 0xD9 or marker == 0xDA:
                return None
            if 0xD0 <= marker <= 0xD8:
                continue

            length_bytes = f.read(2)
            if len(length_bytes) != 2:
                return None
            length = struct.unpack(">H", length_bytes)[0]
            if length < 2:
                return None

            if marker in JPEG_SOF_MARKERS:
                data = f.read(5)
                if len(data) != 5:
                    return None
                height, width = struct.unpack(">HH", data[1:5])
                return width, height

            f.seek(length - 2, 1)

@lru_cache(maxsize=None)
def get_image_dimensions(src):
    path = get_local_path(src)
    if path is None:
        return None

    suffix = path.suffix.lower()
    try:
        if suffix == ".png":
            return read_png_dimensions(path)
        if suffix in {".jpg", ".jpeg"}:
            return read_jpeg_dimensions(path)
    except OSError:
        return None
    return None

def image_tag(src, css_class, alt, lazy=True):
    attrs = [
        f'src="{html_attr(src)}"',
        f'class="{html_attr(css_class)}"',
        f'alt="{html_attr(alt)}"',
    ]

    dimensions = get_image_dimensions(src)
    if dimensions is not None:
        width, height = dimensions
        attrs.extend([f'width="{width}"', f'height="{height}"'])

    if lazy:
        attrs.append('loading="lazy"')
    attrs.append('decoding="async"')
    return f"<img {' '.join(attrs)}>"

def get_json_ld_script(data):
    if data is None:
        return ""

    json_content = json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")
    return f"""
  <script type="application/ld+json">
{json_content}
  </script>"""

def get_author_dict():
    with AUTHOR_FILE.open() as f:
        return json.load(f)

def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name=None,
                         add_links=True, equal_contribution=None):
    links = get_author_dict() if add_links else {}
    s = ""

    equal_contributors = -1
    if equal_contribution is not None:
        equal_contributors = equal_contribution
    for idx, p in enumerate(persons):
        person_name = ""
        for name_part_i in p.get_part('first') + p.get_part('last'): 
            if person_name != "":
                person_name += " "
            person_name += name_part_i
        if make_bold and make_bold_name is not None and person_name == make_bold_name:
            string_part_i = f'<span class="author-self">{person_name}</span>'
        elif person_name in links.keys():
            string_part_i = f'<a href="{links[person_name]}" target="_blank">{person_name}</a>'
        else:
            string_part_i = person_name
        if idx < equal_contributors:
            string_part_i += "*"
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_paper_entry(entry_key, entry, show_highlight=True, self_author_name=None):
    if show_highlight and 'highlight' in entry.fields.keys():
        s = """<div class="entry entry-highlight"> <div class="row"><div class="col-sm-3">"""
    else:
        s = """<div class="entry"> <div class="row"><div class="col-sm-3">"""

    s += image_tag(
        entry.fields['img'],
        "img-fluid img-thumbnail",
        f"{entry.fields['title']} thumbnail",
    )
    s += """</div><div class="col-sm-9">"""

    if 'award' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank" class="entry-title">{entry.fields['title']}</a> <span class="award">({entry.fields['award']})</span><br>"""
    else:
        s += f"""<a href="{entry.fields['html']}" target="_blank" class="entry-title">{entry.fields['title']}</a> <br>"""

    if 'equal_contribution' in entry.fields.keys():
        s += f"""{generate_person_html(entry.persons['author'], make_bold_name=self_author_name, equal_contribution=int(entry.fields['equal_contribution']))} <br>"""
    else:
        s += f"""{generate_person_html(entry.persons['author'], make_bold_name=self_author_name)} <br>"""

    s += f"""<span class="venue">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'html': 'Abs', 'pdf': 'Paper', 'supp': 'Supplementary', 'video': 'Video', 'poster': 'Poster', 'code': 'Code'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')

    cite = "<pre><code>@" + entry.type + "{" + f"{entry_key},\n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "},\n"
    for entr in ['title', 'booktitle', 'year']:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "},\n"
    cite += """}</code></pre>"""
    s += f""" / <details class="bibtex"><summary>Bibtex</summary><div class="bibtex-code"><button type="button" class="copy-bibtex" aria-label="Copy BibTeX">Copy</button>{cite}</div></details>"""
    s += """ </div> </div> </div>"""
    return s

def get_talk_entry(entry_key, entry):
    s = """<div class="entry"> <div class="row"><div class="col-sm-3">"""
    s += image_tag(
        entry.fields['img'],
        "img-fluid img-thumbnail",
        f"{entry.fields['title']} talk thumbnail",
    )
    s += """</div><div class="col-sm-9">"""
    if 'video' in entry.fields.keys():
        s += f"""<a href="{entry.fields['video']}" target="_blank" class="entry-title">{entry.fields['title']}</a><br>"""
    else:
        s += f"""<span class="entry-title">{entry.fields['title']}</span><br>"""
    s += f"""<span class="venue">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'slides': 'Slides', 'video': 'Recording'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    s += """ </div> </div> </div>"""
    return s

def get_publications_html(highlighted_only=False, show_highlight=True, self_author_name=None):
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        entry = bib_data.entries[k]
        if highlighted_only:
            if 'highlight' in entry.fields.keys():
                s += get_paper_entry(k, entry, show_highlight=show_highlight, self_author_name=self_author_name)
        else:
            s += get_paper_entry(k, entry, show_highlight=show_highlight, self_author_name=self_author_name)
    return s

def get_talks_html(highlighted_only=False):
    parser = bibtex.Parser()
    bib_data = parser.parse_file('talk_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        entry = bib_data.entries[k]
        if highlighted_only:
            if 'highlight' in entry.fields.keys():
                s += get_talk_entry(k, entry)
        else:
            s += get_talk_entry(k, entry)
    return s

class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metadata = {}
        self.icon = ""

    def handle_starttag(self, tag, attrs):
        attrs = {k.lower(): v for k, v in attrs}

        if tag == "meta":
            key = attrs.get("property") or attrs.get("name")
            content = attrs.get("content")
            if key and content:
                self.metadata[key.lower()] = content
        elif tag == "link":
            rel = (attrs.get("rel") or "").lower()
            href = attrs.get("href") or ""
            if href and ("icon" in rel or "apple-touch-icon" in rel):
                self.icon = href

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

def clean_text(value):
    parser = TextExtractor()
    parser.feed(unescape(value or ""))
    return " ".join(" ".join(parser.parts).split())

def get_substack_url(substack):
    return f"https://{substack}.substack.com"

def fetch_text(url, timeout=10):
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; personal-site-build-script)"
        },
    )
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")

def xml_local_name(tag):
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag

def child_text(element, *names):
    names = set(names)
    for child in element:
        if xml_local_name(child.tag) in names and child.text:
            return child.text.strip()
    return ""

def channel_image_url(channel):
    for child in channel:
        if xml_local_name(child.tag) == "image":
            return child_text(child, "url")
    return ""

def parse_blog_date(date_text):
    if not date_text:
        return "", ""

    try:
        parsed = parsedate_to_datetime(date_text)
    except (TypeError, ValueError):
        return clean_text(date_text), ""

    return parsed.strftime("%B %Y"), parsed.isoformat()

def get_post_metadata(url):
    html = fetch_text(url)
    parser = MetadataParser()
    parser.feed(html)
    metadata = parser.metadata
    image = metadata.get("og:image") or metadata.get("twitter:image") or parser.icon

    return {
        "title": clean_text(metadata.get("og:title") or metadata.get("twitter:title")),
        "subtitle": clean_text(metadata.get("og:description") or metadata.get("description")),
        "image": urljoin(url, image) if image else "",
    }

def parse_substack_feed(feed_xml, base_url):
    root = ET.fromstring(feed_xml)
    channel = root.find("channel")
    if channel is None:
        channel = root

    fallback_image = urljoin(base_url, channel_image_url(channel))
    items = [child for child in channel if xml_local_name(child.tag) in {"item", "entry"}]

    posts = []
    for item in items:
        link = child_text(item, "link")
        if not link:
            for child in item:
                if xml_local_name(child.tag) == "link":
                    link = child.attrib.get("href", "")
                    break
        if not link:
            continue

        title = clean_text(child_text(item, "title"))
        subtitle = clean_text(child_text(item, "description", "summary", "content"))
        date_text = child_text(item, "pubDate", "published", "updated")
        display_date, sort_date = parse_blog_date(date_text)

        posts.append({
            "title": title,
            "subtitle": subtitle,
            "url": urljoin(base_url, link),
            "image": fallback_image,
            "date": display_date,
            "sort_date": sort_date,
        })

    posts.sort(key=lambda post: post["sort_date"], reverse=True)
    return posts

def read_substack_cache(substack):
    if not SUBSTACK_CACHE_FILE.exists():
        return []

    try:
        with SUBSTACK_CACHE_FILE.open() as f:
            cached = json.load(f)
    except json.JSONDecodeError:
        return []

    if cached.get("substack") != substack:
        return []
    return cached.get("posts", [])

def write_substack_cache(substack, posts):
    cache = {
        "substack": substack,
        "posts": posts,
    }
    with SUBSTACK_CACHE_FILE.open("w") as f:
        json.dump(cache, f, indent=2)
        f.write("\n")

def get_substack_posts(substack, limit=2):
    base_url = get_substack_url(substack)
    try:
        feed_xml = fetch_text(f"{base_url}/feed")
        posts = parse_substack_feed(feed_xml, base_url)
        enriched_posts = []

        for post in posts[:limit]:
            try:
                metadata = get_post_metadata(post["url"])
            except (HTTPError, URLError, TimeoutError, OSError) as exc:
                print(f"[Substack] Warning: Could not fetch post metadata for {post['url']}: {exc}")
                metadata = {"title": "", "subtitle": "", "image": ""}
            enriched_posts.append({
                **post,
                "title": metadata["title"] or post["title"],
                "subtitle": metadata["subtitle"] or post["subtitle"],
                "image": metadata["image"] or post["image"],
            })

        if enriched_posts:
            write_substack_cache(substack, enriched_posts)
            return enriched_posts
    except (HTTPError, URLError, TimeoutError, ET.ParseError, OSError) as exc:
        print(f"[Substack] Warning: Could not fetch latest posts: {exc}")

    cached_posts = read_substack_cache(substack)
    if cached_posts:
        print("[Substack] Using cached posts.")
    return cached_posts[:limit]

def get_blog_entry(post):
    raw_title = post["title"]
    raw_image = post.get("image", "")
    title = escape(raw_title)
    url = escape(post["url"], quote=True)
    subtitle = escape(post.get("subtitle", ""))
    date = escape(post.get("date", ""))

    s = """<div class="entry blog-entry"> <div class="row"><div class="col-sm-3">"""
    if raw_image:
        s += image_tag(raw_image, "img-fluid img-thumbnail blog-post-image", raw_title)
    else:
        s += """<div class="img-thumbnail blog-post-placeholder"><i class="fa-solid fa-feather fa-lg"></i></div>"""
    s += """</div><div class="col-sm-9">"""
    s += f"""<a href="{url}" target="_blank" class="entry-title">{title}</a><br>"""
    if date:
        s += f"""{date}<br>"""
    if subtitle:
        s += f"""<a href="{url}" target="_blank" class="blog-post-subtitle">{subtitle}</a>"""
    s += """ </div> </div> </div>"""
    return s

def get_blog_posts_html(substack, limit=2):
    posts = get_substack_posts(substack, limit=limit)
    return "".join(get_blog_entry(post) for post in posts)

def get_person_structured_data(personal_data):
    name = personal_data["name"]
    organization = personal_data["organization"]
    profiles = personal_data["profiles"]
    site_url = personal_data["site_url"].rstrip("/")

    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": f"{site_url}/#person",
        "name": personal_data["full_name"],
        "givenName": name[0],
        "familyName": name[1],
        "url": f"{site_url}/",
        "image": absolute_url(personal_data["profile_image"], site_url),
        "email": f"mailto:{personal_data['email']}",
        "jobTitle": personal_data["job_title"],
        "description": personal_data["description"],
        "worksFor": {
            "@type": "Organization",
            "name": organization["name"],
            "url": organization["url"],
        },
        "sameAs": [
            profiles["scholar"],
            profiles["substack"],
            profiles["linkedin"],
            profiles["github"],
            profiles["youtube"],
        ],
    }

def get_html_header(
    title,
    description,
    site_url,
    site_name,
    canonical_path="",
    social_image="",
    structured_data=None,
):
    canonical_url = absolute_url(canonical_path, site_url)
    image_url = absolute_url(social_image, site_url)
    escaped_title = html_attr(title)
    escaped_description = html_attr(description)
    escaped_site_name = html_attr(site_name)
    escaped_canonical_url = html_attr(canonical_url)
    escaped_image_url = html_attr(image_url)
    social_image_dimensions = get_image_dimensions(social_image)
    social_image_size_tags = ""
    if social_image_dimensions is not None:
        width, height = social_image_dimensions
        social_image_size_tags = f"""
  <meta property="og:image:width" content="{width}">
  <meta property="og:image:height" content="{height}">"""
    structured_data_script = get_json_ld_script(structured_data)

    return f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"
    integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A=="
    crossorigin="anonymous" referrerpolicy="no-referrer">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <title>{escaped_title}</title>
  <meta name="description" content="{escaped_description}">
  <meta name="author" content="{escaped_site_name}">
  <link rel="canonical" href="{escaped_canonical_url}">
  <meta property="og:site_name" content="{escaped_site_name}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escaped_title}">
  <meta property="og:description" content="{escaped_description}">
  <meta property="og:url" content="{escaped_canonical_url}">
  <meta property="og:image" content="{escaped_image_url}">{social_image_size_tags}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escaped_title}">
  <meta name="twitter:description" content="{escaped_description}">
  <meta name="twitter:image" content="{escaped_image_url}">
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
  <link rel="stylesheet" href="assets/site.css">{structured_data_script}
</head>
"""

def get_html_footer():
    return """
    <script>
      function copyText(text) {
        if (navigator.clipboard && window.isSecureContext) {
          return navigator.clipboard.writeText(text);
        }

        return new Promise(function(resolve, reject) {
          var textarea = document.createElement('textarea');
          textarea.value = text;
          textarea.style.position = 'fixed';
          textarea.style.opacity = '0';
          document.body.appendChild(textarea);
          textarea.focus();
          textarea.select();

          try {
            document.execCommand('copy') ? resolve() : reject();
          } catch (err) {
            reject(err);
          } finally {
            document.body.removeChild(textarea);
          }
        });
      }

      document.addEventListener('click', function(event) {
        var button = event.target.closest('.copy-bibtex');
        if (!button) {
          return;
        }

        var details = button.closest('details.bibtex');
        var code = details ? details.querySelector('code') : null;
        if (!code) {
          return;
        }

        copyText(code.textContent).then(function() {
          button.textContent = 'Copied';
          button.classList.add('copied');
          window.setTimeout(function() {
            button.textContent = 'Copy';
            button.classList.remove('copied');
          }, 1200);
        });
      });
    </script>
    <!-- Cloudflare Web Analytics -->
    <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "556cab14f28a44af930eb08b42be4126"}'></script>
    <!-- End Cloudflare Web Analytics -->
</body>

</html>
"""

def get_page_html(
    title,
    body,
    footer,
    description,
    site_url,
    site_name,
    canonical_path="",
    social_image="",
    structured_data=None,
):
    html = get_html_header(
        title,
        description=description,
        site_url=site_url,
        site_name=site_name,
        canonical_path=canonical_path,
        social_image=social_image,
        structured_data=structured_data,
    ) + f"""
<body>
    <div class="container">
        {body}
        <div class="row page-footer">
            {footer}
        </div>
    </div>
""" + get_html_footer()
    return secure_target_blank(html)

def get_display_name_html(name, highlight_last=False):
    last_name = name[1].upper()
    if highlight_last:
        last_name = f"""<span class="name-last">{last_name}</span>"""
    return f"""<span class="text-bold">{name[0].upper()}</span> {last_name}"""

def get_name_row(name, linked=False):
    title = get_display_name_html(name)
    if linked:
        title = f"""<a href="index.html" class="page-title-link">{title}</a>"""

    return f"""
        <div class="row page-title-row">
            <div class="col-sm-12 page-title-wrap">
            <h1 class="display-4 page-title">{title}</h1>
            </div>
        </div>
"""

def get_section_row(title, content, margin_top="1em", view_all_href=None, view_all_text=None):
    section_class = "content-section-spacious" if margin_top == "3em" else "content-section"
    view_all = ""
    if view_all_href is not None:
        target = ' target="_blank"' if view_all_href.startswith(("http://", "https://")) else ""
        view_all = f"""
                <p><a href="{view_all_href}"{target}>{view_all_text}</a></p>"""

    return f"""
        <div class="row {section_class}">
            <div class="col-sm-12">
                <h2 class="h4">{title}</h2>{view_all}
                <hr>
                {content}
            </div>
        </div>
"""

def get_index_intro_row(personal_data):
    title = get_display_name_html(personal_data["name"], highlight_last=True)
    return f"""
        <div class="row intro-row">
            <div class="col-sm-12 page-title-wrap">
            <h1 class="display-4 page-title">{title}</h1>
            </div>
            <br>
            <div class="col-md-8">
                {personal_data["bio_text"]}
            </div>
            <div class="col-md-4">
                {image_tag(personal_data["profile_image"], "img-thumbnail", personal_data["profile_image_alt"], lazy=False)}
            </div>
        </div>
"""

def get_index_html():
    personal_data = get_personal_data()
    pub = get_publications_html(
        highlighted_only=True,
        show_highlight=False,
        self_author_name=personal_data["self_author_name"],
    )
    talks = get_talks_html(highlighted_only=True)
    blog_posts = get_blog_posts_html(personal_data["substack"])
    body = get_index_intro_row(personal_data)
    body += get_section_row("Selected Publications", pub, view_all_href="publications.html", view_all_text="View all publications")
    body += get_section_row("Selected Talks", talks, margin_top="3em", view_all_href="talks.html", view_all_text="View all talks")
    if blog_posts:
        body += get_section_row(
            "Recent Blog Posts",
            blog_posts,
            margin_top="3em",
            view_all_href=get_substack_url(personal_data["substack"]),
            view_all_text="View all posts",
        )
    return get_page_html(
        f"{personal_data['full_name']} | {personal_data['site_title_suffix']}",
        body,
        personal_data["footer"],
        description=personal_data["description"],
        site_url=personal_data["site_url"],
        site_name=personal_data["full_name"],
        canonical_path="",
        social_image=personal_data["profile_image"],
        structured_data=get_person_structured_data(personal_data),
    )

def get_publications_page_html():
    personal_data = get_personal_data()
    pub = get_publications_html(
        highlighted_only=False,
        show_highlight=True,
        self_author_name=personal_data["self_author_name"],
    )
    body = get_name_row(personal_data["name"], linked=True)
    body += get_section_row("Publications", pub)
    return get_page_html(
        f"Publications | {personal_data['full_name']}",
        body,
        personal_data["footer"],
        description=personal_data["publications_description"],
        site_url=personal_data["site_url"],
        site_name=personal_data["full_name"],
        canonical_path="publications.html",
        social_image=personal_data["profile_image"],
    )

def get_talks_page_html():
    personal_data = get_personal_data()
    talks = get_talks_html()
    body = get_name_row(personal_data["name"], linked=True)
    body += get_section_row("Talks", talks)
    return get_page_html(
        f"Talks | {personal_data['full_name']}",
        body,
        personal_data["footer"],
        description=personal_data["talks_description"],
        site_url=personal_data["site_url"],
        site_name=personal_data["full_name"],
        canonical_path="talks.html",
        social_image=personal_data["profile_image"],
    )

def write_html(content, filename):
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Written content to {filename}.')

if __name__ == '__main__':
    write_html(get_index_html(), 'index.html')
    write_html(get_publications_page_html(), 'publications.html')
    write_html(get_talks_page_html(), 'talks.html')
