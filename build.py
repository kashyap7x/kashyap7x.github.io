import json
from pathlib import Path

from pybtex.database.input import bibtex

AUTHOR_FILE = Path(__file__).with_name("authors.json")

def get_personal_data():
    name = ["Kashyap", "Chitta"]
    email = "kchitta@nvidia.com"
    scholar = "vX5i2CcAAAAJ"
    substack = "kashyap7x"
    linkedin = "kchitta"
    github = "kashyap7x"
    youtube = "UC_rpEkxE-pUAV8v0wjdtg5w"

    bio_text = f"""
                <p>
                    I am a Postdoctoral Researcher at the <a href="https://research.nvidia.com/labs/avg/" target="_blank">NVIDIA Autonomous Vehicle Research Group</a> working from Tübingen, Germany. My research focuses on simulation-based training and evaluation of Physical AI systems.
                </p>
                <p>
                    <span class="text-bold">Bio:</span>
                    Kashyap did a bachelor's degree in electronics at the <a href="https://www.rvce.edu.in/" target="_blank">RV College of Engineering</a>, India. He then moved to the US in 2017 to obtain his Master's degree in computer vision from <a href="https://www.ri.cmu.edu/" target="_blank">Carnegie Mellon University</a>, where he was advised by <a href = "http://www.cs.cmu.edu/~hebert/" target="_blank">Prof. Martial Hebert</a>. During this time, he was also an intern at the <a href = "https://research.nvidia.com/labs/av-applied-research/" target="_blank">NVIDIA Autonomous Vehicles Applied Research Group</a> working with <a href = "https://alvarezlopezjosem.github.io/" target="_blank">Dr. Jose M. Alvarez</a>. From 2019, he was a PhD student in the <a href="https://uni-tuebingen.de/en/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/autonomous-vision/home/" target="_blank">Autonomous Vision Group</a> at the University of Tübingen, Germany, supervised by <a href="http://cvlibs.net/" target="_blank">Prof. Andreas Geiger</a>. He was selected for the <a href="https://iccv2023.thecvf.com/doctoral.consortium-353000-2-30.php" target="_blank">doctoral consortium</a> at ICCV 2023, as a 2023 <a href="https://sites.google.com/view/rsspioneers2023/participants" target="_blank">RSS pioneer</a>, and an outstanding reviewer for <a href="https://cvpr2023.thecvf.com/Conferences/2023/OutstandingReviewers" target="_blank">CVPR</a>, <a href="https://twitter.com/kashyap7x/status/1712169445349560517" target="_blank">ICCV</a>, <a href="https://eccv.ecva.net/Conferences/2024/Reviewers" target="_blank">ECCV</a>, and <a href="https://neurips.cc/Conferences/2023/ProgramCommittee#top-reivewers" target="_blank">NeurIPS</a>. He has also won multiple autonomous driving challenge awards <a href="https://opendrivelab.com/challenge2023/#nuplan_planning" target="_blank">[nuPlan 2023]</a> <a href="https://leaderboard.carla.org/challenge/#previous-carla-ad-challenges" target="_blank">[CARLA 2020, 2021, 2022, 2023, 2024]</a> <a href="https://waymo.com/open/challenges/" target="_blank">[Waymo 2025]</a> <a href="https://realadsim.github.io/2025/#challenge" target="_blank">[HUGSIM 2025]</a>.
                </p>
                <p>
                    <a href="https://kashyap7x.github.io/assets/pdf/kchitta_cv.pdf" target="_blank" class="social-link"><i class="fa fa-address-card fa-lg"></i> CV</a>
                    <a href="mailto:{email}" class="social-link"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a href="https://scholar.google.com/citations?user={scholar}&hl=en" target="_blank" class="social-link"><i class="fa-solid fa-graduation-cap"></i> Scholar</a>
                    <a href="https://{substack}.substack.com" target="_blank" class="social-link"><i class="fa-solid fa-feather fa-lg"></i> Substack</a>
                    <a href="https://www.linkedin.com/in/{linkedin}" target="_blank" class="social-link"><i class="fab fa-linkedin fa-lg"></i> Linkedin</a>
                    <a href="https://github.com/{github}" target="_blank" class="social-link"><i class="fab fa-github fa-lg"></i> GitHub</a>
                    <a href="https://www.youtube.com/channel/{youtube}" target="_blank" class="social-link"><i class="fab fa-youtube fa-lg"></i> YouTube</a>
                </p>
    """
    footer = """
            <div class="col-sm-12">
                <p>
                    This website is based on the lightweight and easy-to-use template from Michael Niemeyer. <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">Check out his github repository for instructions on how to use it!</a>
                </p>
            </div>
    """
    return name, bio_text, footer

def get_author_dict():
    with AUTHOR_FILE.open() as f:
        return json.load(f)

def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name='Kashyap Chitta', 
                         add_links=True, equal_contribution=None):
    links = get_author_dict() if add_links else {}
    s = ""

    equal_contributors = -1
    if equal_contribution is not None:
        equal_contributors = equal_contribution
    for idx, p in enumerate(persons):
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'): 
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span class="author-self">{make_bold_name}</span>'
        if idx < equal_contributors:
            string_part_i += "*"
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_paper_entry(entry_key, entry, show_highlight=True):
    if show_highlight and 'highlight' in entry.fields.keys():
        s = """<div class="entry entry-highlight"> <div class="row"><div class="col-sm-3">"""
    else:
        s = """<div class="entry"> <div class="row"><div class="col-sm-3">"""

    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""

    if 'award' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <span class="award">({entry.fields['award']})</span><br>"""
    else:
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <br>"""

    if 'equal_contribution' in entry.fields.keys():
        s += f"""{generate_person_html(entry.persons['author'], equal_contribution=int(entry.fields['equal_contribution']))} <br>"""
    else:
        s += f"""{generate_person_html(entry.persons['author'])} <br>"""

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

    cite = "<pre><code>@" + entry.type + "{" + f"{entry_key}, \n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    for entr in ['title', 'booktitle', 'year']:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</code></pre>"""
    s += f""" / <details class="bibtex"><summary>Bibtex</summary><div class="bibtex-code"><button type="button" class="copy-bibtex" aria-label="Copy BibTeX">Copy</button>{cite}</div></details>"""
    s += """ </div> </div> </div>"""
    return s

def get_talk_entry(entry_key, entry):
    s = """<div class="entry"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""{entry.fields['title']}<br>"""
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

def get_publications_html(highlighted_only=False, show_highlight=True):
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        entry = bib_data.entries[k]
        if highlighted_only:
            if 'highlight' in entry.fields.keys():
                s += get_paper_entry(k, entry, show_highlight=show_highlight)
        else:
            s += get_paper_entry(k, entry, show_highlight=show_highlight)
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

def get_html_header(title, assets_prefix=""):
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

  <title>{title}</title>
  <link rel="icon" type="image/x-icon" href="{assets_prefix}assets/favicon.ico">
  <link rel="stylesheet" href="{assets_prefix}assets/site.css">
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
</body>

</html>
"""

def get_page_html(title, body, footer):
    return get_html_header(title) + f"""
<body>
    <div class="container">
        {body}
        <div class="row page-footer">
            {footer}
        </div>
    </div>
""" + get_html_footer()

def get_name_row(name, linked=False):
    title = f"""<span class="text-bold">{name[0]}</span> {name[1]}"""
    if linked:
        title = f"""<a href="index.html" class="page-title-link">{title}</a>"""

    return f"""
        <div class="row page-title-row">
            <div class="col-sm-12 page-title-wrap">
            <h3 class="display-4 page-title">{title}</h3>
            </div>
        </div>
"""

def get_section_row(title, content, margin_top="1em", view_all_href=None, view_all_text=None):
    section_class = "content-section-spacious" if margin_top == "3em" else "content-section"
    view_all = ""
    if view_all_href is not None:
        view_all = f"""
                <p><a href="{view_all_href}">{view_all_text}</a></p>"""

    return f"""
        <div class="row {section_class}">
            <div class="col-sm-12">
                <h4>{title}</h4>{view_all}
                <hr>
                {content}
            </div>
        </div>
"""

def get_index_intro_row(name, bio_text):
    return f"""
        <div class="row intro-row">
            <div class="col-sm-12 page-title-wrap">
            <h3 class="display-4 page-title"><span class="text-bold">{name[0]}</span> {name[1]}</h3>
            </div>
            <br>
            <div class="col-md-8">
                {bio_text}
            </div>
            <div class="col-md-4">
                <img src="assets/img/profile.jpg" class="img-thumbnail" alt="Profile picture">
            </div>
        </div>
"""

def get_index_html():
    pub = get_publications_html(highlighted_only=True, show_highlight=False)
    talks = get_talks_html(highlighted_only=True)
    name, bio_text, footer = get_personal_data()
    body = get_index_intro_row(name, bio_text)
    body += get_section_row("Selected Publications", pub, view_all_href="publications.html", view_all_text="View all publications")
    body += get_section_row("Selected Talks", talks, margin_top="3em", view_all_href="talks.html", view_all_text="View all talks")
    return get_page_html(f"{name[0]} {name[1]} | AI Researcher", body, footer)

def get_publications_page_html():
    pub = get_publications_html(highlighted_only=False, show_highlight=True)
    name, _, footer = get_personal_data()
    body = get_name_row(name, linked=True)
    body += get_section_row("Publications", pub)
    return get_page_html(f"Publications | {name[0]} {name[1]}", body, footer)

def get_talks_page_html():
    talks = get_talks_html()
    name, _, footer = get_personal_data()
    body = get_name_row(name, linked=True)
    body += get_section_row("Talks", talks)
    return get_page_html(f"Talks | {name[0]} {name[1]}", body, footer)

def write_html(content, filename):
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Written content to {filename}.')

if __name__ == '__main__':
    write_html(get_index_html(), 'index.html')
    write_html(get_publications_page_html(), 'publications.html')
    write_html(get_talks_page_html(), 'talks.html')
