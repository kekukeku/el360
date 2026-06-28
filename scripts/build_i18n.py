#!/usr/bin/env python3
"""Generate multilingual pages for EverLab360 static site."""

import json
import os
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
I18N_DIR = ROOT / "i18n"

LANGUAGES = {
    "zh": {"dir": "", "html_lang": "zh-TW", "label": "繁體中文", "short": "繁中"},
    "en": {"dir": "en", "html_lang": "en", "label": "English", "short": "EN"},
    "ja": {"dir": "ja", "html_lang": "ja", "label": "日本語", "short": "JA"},
    "ko": {"dir": "ko", "html_lang": "ko", "label": "한국어", "short": "KO"},
    "vi": {"dir": "vi", "html_lang": "vi", "label": "Tiếng Việt", "short": "VI"},
    "fr": {"dir": "fr", "html_lang": "fr", "label": "Français", "short": "FR"},
}

TEAM_IMAGES = [
    "assets/2025/07/adobe-express-file-edited-1.png",
    "assets/2025/07/mina-chen-photo-1.jpg-edited.png",
    "assets/2025/07/daniel-hsiao-photo.jpg-1-edited-1.png",
    "assets/2025/07/kevin-kuo-photo-1-edited-1.png",
    "assets/2025/07/pica-pic_face_swap-20250309205042-photoroom-2-edited.png",
]

BLOG_NOTICE = {
    "en": "This article is currently available in Traditional Chinese.",
    "ja": "この記事は現在繁体字中国語で提供されています。",
    "ko": "이 글은 현재 번체 중국어로 제공됩니다.",
    "vi": "Bài viết này hiện có bằng tiếng Trung Phồn thể.",
    "fr": "Cet article est actuellement disponible en chinois traditionnel.",
}


def load_translations():
    data = {}
    for lang in LANGUAGES:
        path = I18N_DIR / f"{lang}.json"
        with open(path, encoding="utf-8") as f:
            data[lang] = json.load(f)
    return data


def prefix(rel_root: int) -> str:
    return "../" * rel_root


def asset(rel_root: int, path: str) -> str:
    return prefix(rel_root) + path


def lang_home(target_lang: str, rel_root: int, current_lang: str) -> str:
    if target_lang == current_lang and current_lang != "zh":
        if rel_root == 1:
            return "index.html"
        if rel_root == 2:
            return "../index.html"
    base = prefix(rel_root)
    if target_lang == "zh":
        return f"{base}index.html"
    return f"{base}{LANGUAGES[target_lang]['dir']}/index.html"


def lang_switcher(current: str, rel_root: int) -> str:
    options = []
    for code, meta in LANGUAGES.items():
        href = lang_home(code, rel_root, current)
        selected = " selected" if code == current else ""
        options.append(
            f'<option value="{href}"{selected}>{meta["label"]}</option>'
        )
    return f"""<div class="lang-switcher">
            <select id="lang-select-{rel_root}-{current}" class="lang-select" aria-label="Language" onchange="if(this.value)window.location.href=this.value">
                {''.join(options)}
            </select>
        </div>"""


def social_links() -> str:
    return """<div class="social-links">
            <a href="https://www.facebook.com/everlab360" title="Facebook" target="_blank" rel="noopener">FB</a>
            <a href="https://www.linkedin.com/company/everlab-360" title="LinkedIn" target="_blank" rel="noopener">LI</a>
            <a href="https://www.instagram.com/everlab360/" title="Instagram" target="_blank" rel="noopener">IG</a>
        </div>"""


def header(lang: str, rel_root: int, t: dict, home_anchor: bool = True) -> str:
    ui = t["ui"]
    home = lang_home(lang, rel_root, lang)

    def nav_href(anchor: str) -> str:
        if lang == "zh" and rel_root == 0:
            return f"#{anchor}"
        return f"{home}#{anchor}"

    if lang == "zh" and rel_root == 0 and home_anchor:
        logo_href = "#"
    else:
        logo_href = home

    return f"""<header class="site-header">
    <div class="container">
        <a href="{logo_href}" class="site-logo">
            <img src="{asset(rel_root, 'assets/2025/03/everlab360.png')}" alt="EverLab360 Logo" onerror="this.style.display='none'">
            <span>{ui['company_name']}</span>
        </a>
        <nav class="site-nav">
            <a href="{nav_href('about')}">{ui['nav']['about']}</a>
            <a href="{nav_href('team')}">{ui['nav']['team']}</a>
            <a href="{nav_href('service')}">{ui['nav']['service']}</a>
            <a href="{nav_href('collaborators')}">{ui['nav']['collaborators']}</a>
            <a href="{nav_href('reviews')}">{ui['nav']['reviews']}</a>
            <a href="{nav_href('blog')}">{ui['nav']['blog']}</a>
            <a href="{nav_href('contact')}">{ui['nav']['contact']}</a>
            {lang_switcher(lang, rel_root)}
        </nav>
        {social_links()}
    </div>
</header>"""


def footer(lang: str, rel_root: int, t: dict) -> str:
    ui = t["ui"]
    home = lang_home(lang, rel_root, lang)

    def flink(anchor: str) -> str:
        if lang == "zh" and rel_root == 0:
            return f"#{anchor}"
        return f"{home}#{anchor}"

    company_line = ui["company_name"]
    if lang == "zh":
        company_line = f"EverLab360 Inc. {ui['company_name']}"

    return f"""<footer class="site-footer">
    <div class="container">
        <div>
            <h3>{company_line}</h3>
            <p>{ui['tagline']}</p>
            <p style="margin-top:0.5rem;opacity:0.7">{ui['footer']['tax_id_label']}：93522258</p>
        </div>
        <div>
            <h3>{ui['footer']['quick_links']}</h3>
            <p><a href="{flink('about')}">{ui['nav']['about']}</a></p>
            <p><a href="{flink('team')}">{ui['nav']['team']}</a></p>
            <p><a href="{flink('service')}">{ui['nav']['service']}</a></p>
        </div>
        <div>
            <h3>{ui['footer']['more']}</h3>
            <p><a href="{flink('collaborators')}">{ui['nav']['collaborators']}</a></p>
            <p><a href="{flink('reviews')}">{ui['nav']['reviews']}</a></p>
            <p><a href="{flink('blog')}">{ui['nav']['blog']}</a></p>
        </div>
        <div>
            <h3>{ui['footer']['contact']}</h3>
            <p>{ui['address_floor']}</p>
            <p>{ui['line']}</p>
            <p>{ui['email']}</p>
        </div>
    </div>
    <div class="footer-bottom">
        {ui['footer']['copyright']}
    </div>
</footer>"""


def page_shell(lang: str, rel_root: int, title: str, body: str, t: dict, main_class: str = "page-content") -> str:
    return f"""<!DOCTYPE html>
<html lang="{LANGUAGES[lang]['html_lang']}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="{asset(rel_root, 'style.css')}">
</head>
<body>
{header(lang, rel_root, t, home_anchor=False)}
    <main class="{main_class}">
{body}
    </main>
{footer(lang, rel_root, t)}
</body>
</html>"""


def read_zh_page_body(filename: str) -> str:
    path = ROOT / filename
    html = path.read_text(encoding="utf-8")
    m = re.search(r"<main class=\"page-content\">(.*)</main>", html, re.DOTALL)
    return m.group(1).strip() if m else ""


def service_items_html(lang: str, rel_root: int, services: list) -> str:
    cards = []
    for svc in services:
        items_html = []
        links = svc.get("links", {})
        for i, item in enumerate(svc["items"]):
            href = links.get(str(i))
            if not href and ("MFCA" in item or "物質流" in item):
                href = "mfca.html"
            if not href and ("Synesgy" in item or "synesgy" in item.lower()):
                href = "synesgy.html"
            if href:
                items_html.append(f'<li><a href="{href}">{item}</a></li>')
            else:
                items_html.append(f"<li>{item}</li>")
        cards.append(f"""            <div class="service-card">
                <h3>{svc['title']}</h3>
                <ul>
                    {''.join(items_html)}
                </ul>
            </div>""")
    return "\n".join(cards)


def generate_index(lang: str, t: dict) -> str:
    idx = t["index"]
    ui = t["ui"]
    rel_root = 0 if lang == "zh" else 1

    team_cards = []
    for i, member in enumerate(idx["team"]):
        team_cards.append(f"""            <div class="team-card">
                <img src="{asset(rel_root, TEAM_IMAGES[i])}" alt="{member['name']}">
                <h3>{member['name']}</h3>
                <p>{member['bio']}</p>
            </div>""")

    collab = idx["collaborators"]
    partners = collab["business_partners"]
    if partners and isinstance(partners[0], dict):
        partners_html = "\n".join(
            f'                    <li><a href="{p["url"]}" target="_blank" rel="noopener">{p["name"]}</a></li>'
            for p in partners
        )
    else:
        partners_html = "\n".join(f"                    <li>{p}</li>" for p in partners)

    clients_html = "\n".join(
        f'                    <li><strong>{c["category"]}</strong>{c["items"]}</li>'
        for c in collab["past_clients"]
    )

    reviews_html = "\n".join(
        f"""            <div class="review-card">
                <div class="review-stars">★★★★★</div>
                <p class="review-text">{r['text']}</p>
                <p class="review-author">{r['author']}</p>
            </div>"""
        for r in idx["reviews"]
    )

    beliefs = "\n".join(
        f'        <p class="text-center mb-2">"{b}"</p>' for b in idx["team_belief"]
    )
    stats = "\n".join(
        f'        <p class="text-center mb-{"3" if i == 2 else "1"}">{s}</p>'
        for i, s in enumerate(collab["stats"])
    )

    # Blog preview from Chinese source
    blog_posts = extract_blog_posts()
    blog_items = []
    for post in blog_posts[:20]:
        title = post["title_zh"]
        if lang != "zh" and post["file"] in t.get("blog_titles", {}):
            title = t["blog_titles"][post["file"]]
        href = f"blog/{quote(post['file'])}"
        blog_items.append(f"""        <li>
            <a href="{href}">{title}</a>
            <span class="post-date">{post['date']}</span>
        </li>""")

    body = f"""
    <section class="hero" id="about">
        <div class="container">
            <h1>{idx['hero_title']}</h1>
            <p>{idx['hero_desc']}</p>
        </div>
        <img src="{asset(rel_root, 'assets/2025/03/moutains-8445767.jpg')}" alt="Sustainability" style="max-width:100%;height:auto;display:block;margin:0 auto;">
    </section>

    <section class="section" id="team">
        <div class="section-title">
            <h2>{idx['team_section_title']}</h2>
        </div>
        <p class="text-center mb-2">{idx['team_belief_intro']}</p>
{beliefs}
        <p class="text-center mb-3"></p>
        <div class="team-grid">
{chr(10).join(team_cards)}
        </div>
    </section>

    <section class="section section-alt" id="service">
        <div class="section-title">
            <h2>{ui['nav']['service']}</h2>
        </div>
        <div class="service-grid">
{service_items_html(lang, rel_root, idx['services'])}
        </div>
    </section>

    <section class="section" id="collaborators">
        <div class="section-title">
            <h2>{ui['nav']['collaborators']}</h2>
        </div>
{stats}
        <div class="collab-grid">
            <div>
                <h3>{collab['business_partners_title']}</h3>
                <ul class="collab-list">
{partners_html}
                </ul>
            </div>
            <img src="{asset(rel_root, 'assets/2025/03/handshake-4487082.jpg')}" alt="Partnership">
        </div>
        <div class="spacer"></div>
        <div class="collab-grid">
            <img src="{asset(rel_root, 'assets/2025/03/ai-generated-9104303.jpg')}" alt="Clients">
            <div>
                <h3>{collab['past_clients_title']}</h3>
                <ul class="collab-list">
{clients_html}
                </ul>
            </div>
        </div>
    </section>

    <section class="section section-alt" id="reviews">
        <div class="section-title">
            <h2>{ui['nav']['reviews']}</h2>
        </div>
        <div class="reviews-grid">
{reviews_html}
        </div>
    </section>

    <section class="section" id="blog">
        <div class="section-title">
            <h2>{ui['nav']['blog']}</h2>
            <p>{idx['blog_subtitle']}</p>
        </div>
        <div class="blog-section">
            <ul class="blog-list">
{chr(10).join(blog_items)}
            </ul>
            <p class="text-center mt-2"><a href="blog/index.html" class="btn btn-outline">{ui['view_all_posts'].format(count=46)}</a></p>
        </div>
    </section>

    <section class="section section-alt text-center">
        <div class="container">
            <h2>{ui['newsletter_title']}</h2>
            <p class="mt-1">{ui['newsletter_desc']}</p>
        </div>
    </section>

    <section class="section" id="contact">
        <div class="section-title">
            <h2>{ui['visit_us']}</h2>
        </div>
        <div class="contact-section">
            <address>
                {ui['address_en']}<br>
                {ui['address_zh']}
            </address>
            <img src="{asset(rel_root, 'assets/2025/03/everlab360.png')}" alt="EverLab360 Logo">
            <p>{ui['line']}<br>{ui['email']}</p>
            <div class="social-links" style="justify-content:center;margin-top:1rem;">
                <a href="https://www.facebook.com/everlab360" title="Facebook" target="_blank" rel="noopener">FB</a>
                <a href="https://www.linkedin.com/company/everlab-360" title="LinkedIn" target="_blank" rel="noopener">LI</a>
                <a href="https://www.instagram.com/everlab360/" title="Instagram" target="_blank" rel="noopener">IG</a>
            </div>
        </div>
    </section>"""

    return f"""<!DOCTYPE html>
<html lang="{LANGUAGES[lang]['html_lang']}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{idx['title']}</title>
    <link rel="stylesheet" href="{asset(rel_root, 'style.css')}">
</head>
<body>
{header(lang, rel_root, t)}
{body}
{footer(lang, rel_root, t)}
</body>
</html>"""


def extract_blog_posts():
    html = (ROOT / "blog" / "index.html").read_text(encoding="utf-8")
    posts = []
    for m in re.finditer(
        r'<a href="([^"]+)">([^<]+)</a>\s*<span class="post-date">([^<]+)</span>',
        html,
    ):
        from urllib.parse import unquote
        posts.append({
            "file": unquote(m.group(1)),
            "title_zh": m.group(2),
            "date": m.group(3),
        })
    return posts


def generate_mfca(lang: str, t: dict) -> str:
    rel_root = 0 if lang == "zh" else 1
    ui = t["ui"]
    if lang == "zh":
        body = read_zh_page_body("mfca.html")
    else:
        home = "index.html"
        body = f"""        <h1>{t['mfca']['title']}</h1>
        <div class="wp-block-buttons">
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{home}">{ui['home']}</a></div>
</div>
{t['mfca']['body']}
<div class="wp-block-group alignfull" style="padding-top:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--50)">
<p class="has-text-align-right">{ui['address_en']}<br>{ui['address_zh']}</p>
<p class="has-text-align-right">{ui['line']}<br>{ui['email']}</p>
<p><a href="#Top">{ui['top']}</a></p>
</div>"""
    title = f"{t['mfca']['title']} - {ui['company_name']}"
    return page_shell(lang, rel_root, title, body, t)


def generate_synesgy(lang: str, t: dict) -> str:
    rel_root = 0 if lang == "zh" else 1
    ui = t["ui"]
    if lang == "zh":
        body = read_zh_page_body("synesgy.html")
    else:
        home = "index.html"
        body = f"""        <h1>{t['synesgy']['title']}</h1>
        <div class="wp-block-buttons">
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{home}">{ui['home']}</a></div>
</div>
{t['synesgy']['body']}
<div class="wp-block-group alignfull" style="padding-top:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--50)">
<p class="has-text-align-right">{ui['address_en']}<br>{ui['address_zh']}</p>
<p class="has-text-align-right">{ui['line']}<br>{ui['email']}</p>
<p><a href="#Top">{ui['top']}</a></p>
</div>"""
    title = f"{t['synesgy']['title']} - {ui['company_name']}"
    return page_shell(lang, rel_root, title, body, t)


def generate_contact(lang: str, t: dict) -> str:
    rel_root = 0 if lang == "zh" else 1
    ui = t["ui"]
    if lang == "zh":
        body = read_zh_page_body("contact.html")
    else:
        home = "index.html"
        body = f"""        <h1>{t['contact']['title']}</h1>
        <div class="wp-block-buttons">
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{home}">{ui['home']}</a></div>
</div>
<figure class="wp-block-embed aligncenter is-type-rich is-provider-canva wp-block-embed-canva"><div class="wp-block-embed__wrapper">
https://www.canva.com/design/DAG4RmAlR4Q/ouhdwzJctrIVxSWpCvK3hA/view
</div></figure>
<div class="wp-block-group alignfull" style="padding-top:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--50)">
<p class="has-text-align-right">{ui['address_en']}<br>{ui['address_zh']}</p>
<p class="has-text-align-right">{ui['line']}<br>{ui['email']}</p>
<p><a href="#Top">{ui['top']}</a></p>
</div>"""
    title = f"{t['contact']['title']} - {ui['company_name']}"
    return page_shell(lang, rel_root, title, body, t)


def generate_blog_index(lang: str, t: dict) -> str:
    rel_root = 1 if lang == "zh" else 2
    ui = t["ui"]
    idx = t["index"]
    posts = extract_blog_posts()
    items = []
    for post in posts:
        title = post["title_zh"]
        if lang != "zh":
            title = t.get("blog_titles", {}).get(post["file"], title)
        items.append(f"""        <li>
            <a href="{quote(post['file'])}">{title}</a>
            <span class="post-date">{post['date']}</span>
        </li>""")

    body = f"""        <h1>{ui['nav']['blog']}</h1>
        <p>{idx['blog_subtitle']}</p>
        <ul class="blog-list">
{chr(10).join(items)}
        </ul>"""
    title = f"{ui['nav']['blog']} - {ui['company_name']}"
    return page_shell(lang, rel_root, title, body, t)


def generate_blog_post(lang: str, t: dict, filename: str, zh_html: str) -> str:
    rel_root = 1 if lang == "zh" else 2
    ui = t["ui"]

    m = re.search(r"<main class=\"post-content\">(.*)</main>", zh_html, re.DOTALL)
    inner = m.group(1).strip() if m else ""

    title_zh = re.search(r"<h1>([^<]+)</h1>", inner)
    title = title_zh.group(1) if title_zh else filename
    if lang != "zh":
        title = t.get("blog_titles", {}).get(filename, title)
        notice = f'<p class="lang-notice"><em>{BLOG_NOTICE[lang]}</em></p>'
        inner = re.sub(r"<h1>[^<]+</h1>", f"<h1>{title}</h1>", inner, count=1)
        inner = notice + inner

    home_btn = lang_home(lang, rel_root, lang)

    # Extract content after post-meta
    meta_m = re.search(r"<div class=\"post-meta\">([^<]+)</div>", inner)
    meta = meta_m.group(1) if meta_m else ""
    content_m = re.search(
        r"<div class=\"post-meta\">[^<]+</div>\s*(.*)", inner, re.DOTALL
    )
    content = content_m.group(1).strip() if content_m else inner

    if lang != "zh":
        content = f'<p class="lang-notice"><em>{BLOG_NOTICE[lang]}</em></p>\n' + content

    content = re.sub(
        r'<div class="wp-block-buttons">.*?</div>\s*',
        "",
        content,
        count=1,
        flags=re.DOTALL,
    )

    body = f"""        <h1>{title}</h1>
        <div class="post-meta">{meta}</div>
        <div class="wp-block-buttons">
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{home_btn}">{ui['home']}</a></div>
</div>
{content}"""

    page_title = f"{title} - {ui['company_name']}"
    return page_shell(lang, rel_root, page_title, body, t, main_class="post-content")


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def main():
    translations = load_translations()
    blog_files = list((ROOT / "blog").glob("*.html"))
    blog_files = [f for f in blog_files if f.name != "index.html"]

    for lang in LANGUAGES:
        print(f"\n=== {lang} ===")
        t = translations[lang]
        out_dir = ROOT if lang == "zh" else ROOT / LANGUAGES[lang]["dir"]

        write_file(out_dir / "index.html", generate_index(lang, t))
        write_file(out_dir / "mfca.html", generate_mfca(lang, t))
        write_file(out_dir / "synesgy.html", generate_synesgy(lang, t))
        write_file(out_dir / "contact.html", generate_contact(lang, t))
        write_file(out_dir / "blog" / "index.html", generate_blog_index(lang, t))

        for bf in blog_files:
            zh_html = bf.read_text(encoding="utf-8")
            write_file(
                out_dir / "blog" / bf.name,
                generate_blog_post(lang, t, bf.name, zh_html),
            )

    print("\nDone.")


if __name__ == "__main__":
    main()