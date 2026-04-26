def get_personal_data():
    name = ["Kashyap", "Chitta"]
    full_name = " ".join(name)
    site_url = "https://kashyap7x.github.io"
    site_title_suffix = "AI Researcher"
    job_title = "Postdoctoral Researcher"
    location = "Tübingen, Germany"
    research_focus = "visual reasoning and causal world models"
    research_topics = "autonomous driving, simulation, world models, and Physical AI"
    profile_image = "assets/img/profile.jpg"
    cv_url = "assets/pdf/kchitta_cv.pdf"
    email = "kchitta@nvidia.com"
    scholar = "vX5i2CcAAAAJ"
    substack = "kashyap7x"
    linkedin = "kchitta"
    github = "kashyap7x"
    youtube = "UC_rpEkxE-pUAV8v0wjdtg5w"
    organization = {
        "name": "NVIDIA Autonomous Vehicle Research Group",
        "url": "https://research.nvidia.com/labs/avg/",
    }
    profiles = {
        "scholar": f"https://scholar.google.com/citations?user={scholar}&hl=en",
        "substack": f"https://{substack}.substack.com",
        "linkedin": f"https://www.linkedin.com/in/{linkedin}",
        "github": f"https://github.com/{github}",
        "youtube": f"https://www.youtube.com/channel/{youtube}",
    }
    personal_data = {
        "name": name,
        "full_name": full_name,
        "self_author_name": full_name,
        "site_url": site_url,
        "site_title_suffix": site_title_suffix,
        "description": f"{full_name} is an AI researcher working on {research_focus}.",
        "publications_description": f"Complete publication list for {full_name}, including papers on {research_topics}.",
        "talks_description": f"Selected invited talks by {full_name} on {research_topics}.",
        "location": location,
        "research_focus": research_focus,
        "profile_image": profile_image,
        "profile_image_alt": f"Portrait of {full_name}",
        "cv_url": cv_url,
        "email": email,
        "job_title": job_title,
        "organization": organization,
        "profiles": profiles,
        "substack": substack,
    }

    bio_details = """
                    <p>I earned my bachelor's degree in electronics from the <a href="https://www.rvce.edu.in/" target="_blank">RV College of Engineering</a>, India, before moving to the US in 2017 for a Master's degree in computer vision at <a href="https://www.ri.cmu.edu/" target="_blank">Carnegie Mellon University</a>, where I was advised by <a href = "http://www.cs.cmu.edu/~hebert/" target="_blank">Prof. Martial Hebert</a>. During this time, I was also an intern at the <a href = "https://research.nvidia.com/labs/av-applied-research/" target="_blank">NVIDIA Autonomous Vehicles Applied Research Group</a>, working with <a href = "https://alvarezlopezjosem.github.io/" target="_blank">Dr. Jose M. Alvarez</a>. From 2019, I was a PhD student in the <a href="https://uni-tuebingen.de/en/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/autonomous-vision/home/" target="_blank">Autonomous Vision Group</a> at the University of Tübingen, Germany, supervised by <a href="http://cvlibs.net/" target="_blank">Prof. Andreas Geiger</a>. I was selected for the <a href="https://iccv2023.thecvf.com/doctoral.consortium-353000-2-30.php" target="_blank">doctoral consortium</a> at ICCV 2023, named a 2023 <a href="https://sites.google.com/view/rsspioneers2023/participants" target="_blank">RSS Pioneer</a>, and recognized as an outstanding reviewer for <a href="https://cvpr2023.thecvf.com/Conferences/2023/OutstandingReviewers" target="_blank">CVPR</a>, <a href="https://twitter.com/kashyap7x/status/1712169445349560517" target="_blank">ICCV</a>, <a href="https://eccv.ecva.net/Conferences/2024/Reviewers" target="_blank">ECCV</a>, and <a href="https://neurips.cc/Conferences/2023/ProgramCommittee#top-reivewers" target="_blank">NeurIPS</a>. I have also won multiple autonomous driving challenge awards <a href="https://opendrivelab.com/challenge2023/#nuplan_planning" target="_blank">[nuPlan 2023]</a> <a href="https://leaderboard.carla.org/challenge/#previous-carla-ad-challenges" target="_blank">[CARLA 2020, 2021, 2022, 2023, 2024]</a> <a href="https://waymo.com/open/challenges/" target="_blank">[Waymo 2025]</a> <a href="https://realadsim.github.io/2025/#challenge" target="_blank">[HUGSIM 2025]</a>.</p>
    """
    bio_text = f"""
                <p>
                    I am a {personal_data['job_title']} at the <a href="{personal_data['organization']['url']}" target="_blank">{personal_data['organization']['name']}</a>, based in {personal_data['location']}. My research focuses on {personal_data['research_focus']}.
                </p>
                <div class="social-links">
                    <details class="bio-dropdown">
                        <summary><i class="fa-solid fa-user fa-lg"></i> Bio</summary>
                    </details>
                    <a href="{personal_data['cv_url']}" target="_blank" class="social-link"><i class="fa fa-address-card fa-lg"></i> CV</a>
                    <a href="mailto:{personal_data['email']}" class="social-link"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a href="{personal_data['profiles']['scholar']}" target="_blank" class="social-link"><i class="fa-solid fa-graduation-cap"></i> Scholar</a>
                    <a href="{personal_data['profiles']['substack']}" target="_blank" class="social-link"><i class="fa-solid fa-feather fa-lg"></i> Substack</a>
                    <a href="{personal_data['profiles']['linkedin']}" target="_blank" class="social-link"><i class="fab fa-linkedin fa-lg"></i> Linkedin</a>
                    <a href="{personal_data['profiles']['github']}" target="_blank" class="social-link"><i class="fab fa-github fa-lg"></i> GitHub</a>
                    <a href="{personal_data['profiles']['youtube']}" target="_blank" class="social-link"><i class="fab fa-youtube fa-lg"></i> YouTube</a>
                    <div class="bio-dropdown-content">
                        {bio_details}
                    </div>
                </div>
    """
    footer = """
            <div class="col-sm-12">
                <p class="template-credit">
                    This website is based on the lightweight and easy-to-use template from Michael Niemeyer. <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">Check out his github repository for instructions on how to use it!</a>
                </p>
            </div>
    """
    personal_data["bio_text"] = bio_text
    personal_data["footer"] = footer
    return personal_data
