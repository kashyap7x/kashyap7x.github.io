from pybtex.database.input import bibtex

def get_personal_data():
    name = ["Kashyap", "Chitta"]
    email = "kashyap.chitta@tue.mpg.de"
    twitter = "kashyap7x"
    github = "kashyap7x"
    linkedin = "kchitta"
    bio_text = f"""
                <p>
                    I am a PhD student at the Max Planck Institute for Intelligent Systems and the University of Tübingen, Germany, where I am part of the <a href = "https://uni-tuebingen.de/en/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/autonomous-vision/home/" target="_blank">Autonomous Vision Group</a> led by <a href = "http://www.cvlibs.net" target="_blank">Prof. Andreas Geiger</a>.
                </p>
                <p>
                    <span style="font-weight: bold;">Research:</span>
                    I am excited about data-driven solutions to complex decision-making tasks. Currently, my research focuses on self-driving vehicles. Specifically, I am interested in how autonomous agents can use attention-based deep neural networks to create abstract representations suitable for safe navigation. Further, I am big fan of simulation, and am interested in building simulators tailored towards improving the robustness and generalization of learned policies. 
                </p>
                <p>
                    <span style="font-weight: bold;">Bio:</span>
                    I did a bachelor's degree in electronics at the <a href="https://www.rvce.edu.in/" target="_blank">RV College of Engineering</a>, India. I then moved to the USA in 2018 to obtain my Master's degree in computer vision from <a href="https://www.ri.cmu.edu/" target="_blank">Carnegie Mellon University</a>, where I was advised by <a href = "http://www.cs.cmu.edu/~hebert/" target="_blank">Prof. Martial Hebert</a>. During this time, I was also an intern on two occasions at NVIDIA working with <a href = "https://alvarezlopezjosem.github.io/" target="_blank">Dr. Jose M. Alvarez</a>.
                    In 2019, I started my PhD in the <a href="https://uni-tuebingen.de/en/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/autonomous-vision/home/" target="_blank">Autonomous Vision Group</a> under the supervision of <a href="http://cvlibs.net/" target="_blank">Prof. Andreas Geiger</a>. I plan to graduate by the end of 2023.
                </p>
                <p>
                    <a href="https://kashyap7x.github.io/assets/pdf/kchitta_cv.pdf" target="_blank" style="margin-right: 15px"><i class="fa fa-address-card fa-lg"></i> CV</a>
                    <a href="mailto:{email}" style="margin-right: 15px"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a href="https://twitter.com/{twitter}" target="_blank" style="margin-right: 15px"><i class="fab fa-twitter fa-lg"></i> Twitter</a>
                    <a href="https://scholar.google.com/citations?user=vX5i2CcAAAAJ&hl=en" target="_blank" style="margin-right: 15px"><i class="fa-solid fa-book"></i> Scholar</a>
                    <a href="https://github.com/{github}" target="_blank" style="margin-right: 15px"><i class="fab fa-github fa-lg"></i> Github</a>
                    <a href="https://www.linkedin.com/in/{linkedin}" target="_blank" style="margin-right: 15px"><i class="fab fa-linkedin fa-lg"></i> LinkedIn</a>
                </p>
    """
    footer = """
            <div class="col-sm-12" style="">
                <p>
                    This website is based on the lightweight and easy-to-use template from Michael Niemeyer. <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">Check out his github repository for instructions on how to use it!</a>
                </p>
            </div>
    """
    return name, bio_text, footer

def get_author_dict():
    return {
        'Otniel-Bogdan Mercea': 'https://merceaotniel.github.io/',
        'Sophia Koepke': 'https://www.eml-unitue.de/people/almut-sophia-koepke',
        'Zeynep Akata': 'https://www.eml-unitue.de/people/zeynep-akata',
        'Niklas Hanselmann': 'https://lasnik.github.io/',
        'Apratim Bhattacharyya': 'https://apratimbhattacharyya18.github.io/',
        'Bernhard Jaeger': 'https://kait0.github.io/',
        'Zehao Yu': 'https://niujinshuchong.github.io/',
        'Katrin Renz': 'https://www.katrinrenz.de/',
        'Axel Sauer': 'https://axelsauer.com/',
        'Jens Muller': 'https://scholar.google.com/citations?user=ayN8HoQAAAAJ&hl=en',
        'Marissa Weis': 'https://scholar.google.com/citations?user=fxJ_ZOQAAAAJ&hl=en',
        'Yash Sharma': 'https://www.yash-sharma.com/',
        'Wieland Brendel': 'https://robustml.is.mpg.de/person/wbrendel',
        'Matthias Bethge': 'http://bethgelab.org/people/matthias/',
        'Alexander Ecker': 'https://eckerlab.org/',
        'Elmar Haussmann': 'https://scholar.google.com/citations?user=HzaEH_MAAAAJ&hl=en',
        'Michele Fenzi': 'https://scholar.google.com/citations?hl=en&user=x3xLe8wAAAAJ',
        'Jan Ivanecky': 'https://www.linkedin.com/in/jan-ivanecky-226b31116',
        'Hanson Xu': 'https://ieeexplore.ieee.org/author/37088650397',
        'Donna Roy': 'https://scholar.google.com/citations?user=Pvt-cf0AAAAJ&hl=en',
        'Akshita Mittel': 'https://scholar.google.com/citations?user=OQOmmooAAAAJ&hl=en',
        'Nicolas Koumchatzky': 'https://www.linkedin.com/in/nicolaskoumchatzky',
        'Clement Farabet': 'http://www.clement.farabet.net/',
        'Aditya Prakash': 'https://ap229997.github.io/',
        'Aseem Behl': 'https://aseembehl.github.io/',
        'Eshed Ohn-Bar': 'https://eshed1.github.io/',
        'Andreas Geiger': 'https://www.cvlibs.net/',
        'Martial Hebert': 'http://www.cs.cmu.edu/~hebert/',
        'Jose Alvarez': 'https://alvarezlopezjosem.github.io/',
        'Adam Lesnikowski': 'https://scholar.google.com/citations?user=jPbTs2QAAAAJ&hl=en',
        }

def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name='Kashyap Chitta', add_links=True):
    links = get_author_dict() if add_links else {}
    s = ""
    for p in persons:
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'): 
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold";>{make_bold_name}</span>'
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_paper_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""

    if 'award' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <br>"""

    s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

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

    cite = "<pre><code>@InProceedings{" + f"{entry_key}, \n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    for entr in ['title', 'booktitle', 'year']:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
    s += " /" + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    s += """ </div> </div> </div>"""
    return s

def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""{entry.fields['title']}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

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

def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_paper_entry(k, bib_data.entries[k])
    return s

def get_talks_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('talk_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_talk_entry(k, bib_data.entries[k])
    return s

def get_index_html():
    pub = get_publications_html()
    talks = get_talks_html()
    name, bio_text, footer = get_personal_data()
    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <title>{name[0] + ' ' + name[1] + ' | AI Researcher'}</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
</head>

<body>
    <div class="container">
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="margin-bottom: 1em;">
            <h3 class="display-4" style="text-align: center;"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3>
            </div>
            <br>
            <div class="col-md-8" style="">
                {bio_text}
            </div>
            <div class="col-md-4" style="">
                <img src="assets/img/profile.jpg" class="img-thumbnail" alt="Profile picture">
            </div>
        </div>
        <div class="row" style="margin-top: 1em;">
            <div class="col-sm-12" style="">
                <h4>Publications</h4>
                <hr>
                {pub}
            </div>
        </div>
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Talks</h4>
                <hr>
                {talks}
            </div>
        </div>
        <div class="row" style="margin-top: 3em; margin-bottom: 1em;">
            {footer}
        </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
</body>

</html>
    """
    return s


def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written index content to {filename}.')

if __name__ == '__main__':
    write_index_html('index.html')