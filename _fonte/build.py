#!/usr/bin/env python3
"""Gera o site kaironbr.com (home + 3 landings) com SEO e GEO.
Uso: python3 build.py <pasta_saida> <whatsapp_com_ddi_ex_5521999999999>
"""
import json, os, shutil, sys
from datetime import date

OUT = sys.argv[1]
WA = sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://kaironbr.com"
TODAY = date.today().isoformat()
WA_FMT = f"+{WA[:2]} ({WA[2:4]}) {WA[4:-4]}-{WA[-4:]}" if len(WA) >= 12 else WA

LOGO = ("<svg viewBox='0 0 34 34' aria-hidden='true'><rect width='34' height='34' rx='9' fill='#1C1B19'/>"
        "<path d='M11 9h12M11 25h12M12 9c0 5.5 10 6.5 10 16M22 9c0 5.5-10 6.5-10 16' stroke='#C9A46A' "
        "stroke-width='1.8' fill='none' stroke-linecap='round'/></svg>")
WA_ICON = ("<svg viewBox='0 0 32 32' aria-hidden='true'><path fill='#fff' d='M16 3C9 3 3.3 8.6 3.3 15.6c0 2.3.6 4.5 "
           "1.8 6.4L3 29l7.2-1.9c1.8 1 3.8 1.5 5.8 1.5 7 0 12.7-5.6 12.7-12.6S23 3 16 3zm0 23.2c-1.8 0-3.6-.5-5.2-1.4l-.4-.2"
           "-4.3 1.1 1.1-4.1-.2-.4c-1-1.6-1.6-3.5-1.6-5.4C5.4 9.9 10.2 5.2 16 5.2s10.6 4.7 10.6 10.5S21.8 26.2 16 26.2zm5.8-7.9"
           "c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.3-.5-2.5-1.5-.9-.8-1.6-1.8-1.7-2.1-.2-.3"
           " 0-.5.1-.6l.5-.6c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2"
           " 3.2 1.4 3.4c.2.2 2.4 3.6 5.7 5 .8.3 1.4.5 1.9.7.8.3 1.5.2 2.1.1.6-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6"
           "-.4z'/></svg>")

ORG = {
    "@type": "Organization", "@id": f"{SITE}/#org", "name": "KAIRON",
    "alternateName": ["KAIRON Bots", "KAIRON Obras", "KAIRON Escala", "Kairon Automação"],
    "url": f"{SITE}/", "email": "contato@kaironbr.com", "telephone": f"+{WA}",
    "slogan": "Processos sob controle, no tempo certo.",
    "description": ("Empresa de engenharia de processos, automação com inteligência artificial e controle de obras "
                    "para pequenas e médias empresas, condomínios, construtoras e clínicas no Rio de Janeiro e em São Paulo."),
    "knowsAbout": ["automação de processos", "inteligência artificial para pequenas empresas", "chatbot de WhatsApp",
                   "automação de planilhas e relatórios", "Power Automate", "Power BI", "Python", "RPA",
                   "project controls", "cronograma físico-financeiro", "curva S", "medição de obras",
                   "escala 6x1", "dimensionamento de equipes", "Lean", "Seis Sigma"],
    "areaServed": [{"@type": "City", "name": "Rio de Janeiro"}, {"@type": "City", "name": "São Paulo"},
                   {"@type": "Country", "name": "Brasil"}],
    "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": f"+{WA}",
                     "email": "contato@kaironbr.com", "availableLanguage": "pt-BR"},
}

NAV = [("index", "/", "Início"), ("bots", "/bots", "Bots"), ("obras", "/obras", "Obras"), ("escala", "/escala", "Escala 6x1")]


def faq_html(items):
    out = []
    for i, (q, a) in enumerate(items):
        out.append(f"<details{' open' if i == 0 else ''}><summary>{q}</summary><p>{a}</p></details>")
    return "<div class='faq'>" + "".join(out) + "</div>"


def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def final_cta(title, text, options, default=0):
    opts = "".join(f"<option{' selected' if i == default else ''}>{o}</option>" for i, o in enumerate(options))
    return f"""
<section id="diagnostico" style="padding-top:0"><div class="wrap"><div class="final">
  <div>
    <p class="kicker">Diagnóstico gratuito</p>
    <h2>{title}</h2>
    <p>{text}</p>
    <div class="alt">Prefere direto? <a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp {WA_FMT}</a> ou <a href="mailto:contato@kaironbr.com">contato@kaironbr.com</a></div>
  </div>
  <form id="diag-form">
    <div class="form-row">
      <label>Nome<input name="nome" required autocomplete="name"></label>
      <label>Empresa ou condomínio<input name="empresa" required autocomplete="organization"></label>
    </div>
    <label>Seu WhatsApp<input name="whatsapp" type="tel" autocomplete="tel"></label>
    <label>Principal desafio<select name="desafio">{opts}</select></label>
    <label>Conte em poucas linhas<textarea name="msg" rows="3"></textarea></label>
    <div class="cta-row" style="margin:6px 0 0">
      <button class="btn btn-light" type="submit" value="wa">Enviar pelo WhatsApp</button>
      <button class="btn btn-ghost" style="color:#fff;border-color:rgba(255,255,255,.35)" type="submit" value="email">Enviar por e-mail</button>
    </div>
  </form>
</div></div></section>"""


CHALLENGES = ["Automatizar rotinas e relatórios", "Controlar prazo, custo e medições de obra",
              "Revisar a escala da equipe (6x1)", "Ainda não sei"]


PROMO_ATE = "2026-11-30"


def promo_bar(slug):
    if TODAY > PROMO_ATE or slug == "black-friday":
        return ""
    return ("<a class='promo' href='/black-friday'><b>Black Friday:</b> Agente SDR de IA no seu WhatsApp, 24h, "
            "implantação por R$ 920. Só até 30/11 →</a>")


def page(slug, title, desc, body, ld_extra, h1_short):
    canonical = f"{SITE}/" if slug == "index" else f"{SITE}/{slug}"
    nav = "".join(f"<a href='{href}'{' class=active aria-current=page' if s == slug else ''}>{label}</a>"
                  for s, href, label in NAV)
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE}/"}]
    if slug != "index":
        crumbs.append({"@type": "ListItem", "position": 2, "name": h1_short, "item": canonical})
    graph = [ORG, {"@type": "WebPage", "@id": canonical + "#page", "url": canonical, "name": title,
                   "description": desc, "inLanguage": "pt-BR", "isPartOf": {"@id": f"{SITE}/#site"},
                   "about": {"@id": f"{SITE}/#org"}, "dateModified": TODAY},
             {"@type": "WebSite", "@id": f"{SITE}/#site", "url": f"{SITE}/", "name": "KAIRON",
              "inLanguage": "pt-BR", "publisher": {"@id": f"{SITE}/#org"}},
             {"@type": "BreadcrumbList", "itemListElement": crumbs}] + ld_extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    csp = ("default-src 'none'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; "
           "img-src 'self' data:; script-src 'self'; connect-src 'none'; form-action 'none'; base-uri 'none'; "
           "object-src 'none'; upgrade-insecure-requests")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="KAIRON">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#1C1B19">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body data-wa="{WA}">
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
{promo_bar(slug)}
<header id="top"><div class="wrap nav">
  <a href="/" class="brand" aria-label="KAIRON, página inicial">{LOGO}KAIRON</a>
  <nav class="menu" id="menu" aria-label="Principal">{nav}<a href="#diagnostico" class="btn btn-dark btn-sm">Diagnóstico gratuito</a></nav>
  <button class="burger" id="burger" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu">☰</button>
</div></header>
<main id="conteudo">
{body}
</main>
<footer><div class="wrap">
  <div class="foot">
    <div><a href="/" class="brand" style="margin-bottom:14px;color:var(--ink)">{LOGO}KAIRON</a>
      <p>Processos sob controle, no tempo certo. Automação, IA e engenharia de processos para pequenas e médias empresas no Rio de Janeiro e em São Paulo.</p></div>
    <div><h4>Soluções</h4><a href="/bots">KAIRON Bots</a><a href="/obras">KAIRON Obras</a><a href="/escala">KAIRON Escala</a></div>
    <div><h4>Empresa</h4><a href="/#como-funciona">Método</a><a href="/#duvidas">Dúvidas frequentes</a><a href="#diagnostico">Diagnóstico gratuito</a></div>
    <div><h4>Contato</h4><a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp {WA_FMT}</a><a href="mailto:contato@kaironbr.com">contato@kaironbr.com</a><p style="padding-top:4px">Rio de Janeiro e São Paulo</p></div>
  </div>
  <div class="legal"><span>© {date.today().year} KAIRON. Todos os direitos reservados.</span><span>kaironbr.com</span></div>
</div></footer>
<a class="wa-float" href="https://wa.me/{WA}?text=Ol%C3%A1!%20Vim%20pelo%20site%20da%20KAIRON." target="_blank" rel="noopener" aria-label="Falar no WhatsApp">{WA_ICON}</a>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def icon(path):
    return f"<div class='ico'><svg viewBox='0 0 24 24'>{path}</svg></div>"


def hero(eyebrow, h1, lead, primary, secondary, trust, visual):
    t = "".join(f"<span>{x}</span>" for x in trust)
    return f"""
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="cta-row"><a href="#diagnostico" class="btn btn-dark">{primary}</a><a href="{secondary[1]}" class="btn btn-ghost">{secondary[0]}</a></div>
    <div class="trust">{t}</div>
  </div>
  <div class="visual">{visual}</div>
</div></section>"""


def notes(items):
    return "".join(f"<div class='note'><div class='top'><span>{a}</span><span>{b}</span></div><b>{c}</b><small>{d}</small></div>"
                   for a, b, c, d in items)


def head(kicker, h2, p=""):
    return f"<div class='head'><p class='kicker'>{kicker}</p><h2>{h2}</h2>{f'<p>{p}</p>' if p else ''}</div>"


def steps(items, cols):
    s = "".join(f"<div class='step'><span class='n'>{i+1:02d}</span><h3>{h}</h3><p>{p}</p></div>" for i, (h, p) in enumerate(items))
    return f"<div class='grid g{cols}'>{s}</div>"


def tiles(items, cols):
    return f"<div class='grid g{cols}'>" + "".join(f"<div class='tile'><h3>{h}</h3><p>{p}</p></div>" for h, p in items) + "</div>"


def pains(items):
    return "<div class='pains'>" + "".join(f"<div class='pain'><span class='dot'></span><div><b>{h}</b>{p}</div></div>" for h, p in items) + "</div>"


def prices(items):
    out = []
    for name, sub, bullets, cta, featured in items:
        lis = "".join(f"<li>{b}</li>" for b in bullets)
        out.append(f"<div class='price{' featured' if featured else ''}'>{'<span class=badge>Recomendado</span>' if featured else ''}"
                   f"<h3>{name}</h3><p class='val'>{sub}</p><ul>{lis}</ul>"
                   f"<a href='#diagnostico' class='btn {'btn-dark' if featured else 'btn-ghost'}'>{cta}</a></div>")
    return "<div class='grid g3'>" + "".join(out) + "</div>"


def service_ld(name, desc, url, catalog):
    return {"@type": "Service", "name": name, "description": desc, "url": url, "provider": {"@id": f"{SITE}/#org"},
            "areaServed": ["Rio de Janeiro", "São Paulo", "Brasil"],
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": name,
                                "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": c}} for c in catalog]}}


# ---------------------------------------------------------------- HOME
home_faq = [
    ("O que a KAIRON faz?", "A KAIRON mede, automatiza e controla processos de pequenas e médias empresas no Rio de Janeiro e em São Paulo. Atua em três frentes: automação com IA (atendimento no WhatsApp, planilhas e relatórios), controle de prazo e custo de obras de médio porte e estudo de impacto do fim da escala 6x1."),
    ("Preciso comprar um software novo?", "Não. A KAIRON trabalha com as ferramentas que a empresa já usa, como WhatsApp, Excel, Google Planilhas, Microsoft 365, Power BI e e-mail. O objetivo é automatizar sem custo fixo alto."),
    ("Quanto custa?", "Depende do escopo. O primeiro passo é um diagnóstico gratuito. Depois a KAIRON envia uma proposta com preço fechado, prazo e o ganho estimado em horas ou em reais."),
    ("Onde a KAIRON atende?", "Rio de Janeiro e São Paulo, presencial ou remoto. Projetos de automação podem ser feitos 100% online para empresas de todo o Brasil."),
    ("O que é o estudo de impacto da escala 6x1?", "É uma análise que calcula quantas pessoas a operação precisa em cada cenário de escala (6x1, 5x2, 12x36), o custo mensal de cada cenário e um plano de transição. Atende condomínios, clínicas e comércio com equipes por turno."),
    ("Quanto tempo leva para ver resultado?", "O diagnóstico gratuito é entregue em até 5 dias úteis. A primeira automação costuma rodar em protótipo em cerca de 5 dias após o início do projeto."),
    ("Meus dados ficam seguros?", "Sim. As automações rodam nas contas da própria empresa, com acesso mínimo necessário e de acordo com a LGPD. Nenhum dado é vendido ou compartilhado."),
]
home_body = hero(
    "Automação, IA e engenharia de processos no RJ e SP",
    "Processos sob controle, <em>no tempo certo.</em>",
    "Automatizamos atendimento, planilhas e relatórios com IA, controlamos prazo e custo de obras e calculamos o impacto da escala 6x1. Com as ferramentas que sua empresa já usa e sem custo fixo alto.",
    "Fazer diagnóstico gratuito", ("Ver soluções", "#solucoes"),
    ["Resposta em até 5 dias úteis", "Sem software caro", "Método de grandes projetos"],
    notes([("Hoje · KAIRON Bots", "08:02", "Relatório semanal enviado", "Gerado da planilha, sem ninguém copiar e colar."),
           ("Hoje · WhatsApp", "09:15", "Cliente remarcou o horário", "Agenda atualizada e confirmação enviada."),
           ("Hoje · KAIRON Obras", "11:40", "Alerta: etapa 3 fora da tolerância", "Curva S atualizada no painel."),
           ("Equipe", "agora", "Só o que precisa de decisão humana", "O repetitivo já foi resolvido.")]))
home_body += f"""
<section class="soft"><div class="wrap">
  {head("Por que automatizar", "Sua equipe no que importa. O repetitivo fica com os robôs.")}
  <div class="grid g3">
    <div class="benefit">{icon("<circle cx='12' cy='12' r='9'/><path d='M12 7v5l3 2'/>")}<h3>Horas de volta</h3><p>Respostas, conferências e relatórios que hoje tomam o dia passam a rodar sozinhos.</p></div>
    <div class="benefit">{icon("<path d='M4 17l6-6 4 4 6-6'/><path d='M14 9h6v6'/>")}<h3>Custo sob controle</h3><p>Sem licença cara nem contratação extra. Usamos o que você já paga.</p></div>
    <div class="benefit">{icon("<rect x='4' y='4' width='16' height='16' rx='3'/><path d='M8 15v-3M12 15V9M16 15v-5'/>")}<h3>Decisão com dados</h3><p>Painel semanal com indicadores e alertas antes que o problema apareça.</p></div>
  </div>
</div></section>
<section id="solucoes"><div class="wrap">
  {head("Soluções", "Três frentes, um mesmo método de engenharia.", "Comece pela que dói mais. As outras se conectam depois.")}
  <div class="grid g3">
    <article class="card"><p class="tag">KAIRON Bots</p><h3>Automação e IA para pequenas e médias empresas</h3><p class="for">Para quem vive de tarefas repetitivas e planilhas espalhadas.</p>
      <ul><li>Atendimento e triagem no WhatsApp</li><li>Planilhas e relatórios que se atualizam sozinhos</li><li>Agentes de IA para rotinas internas</li></ul><a href="/bots" class="link">Conhecer o KAIRON Bots →</a></article>
    <article class="card"><p class="tag">KAIRON Obras</p><h3>Controle de prazo e custo para obras de médio porte</h3><p class="for">Para construtoras, incorporadoras e condomínios em reforma.</p>
      <ul><li>Cronograma físico-financeiro e curva S</li><li>Boletins de medição e controle de custos</li><li>Painel semanal com alertas de desvio</li></ul><a href="/obras" class="link">Conhecer o KAIRON Obras →</a></article>
    <article class="card"><p class="tag">KAIRON Escala</p><h3>Estudo de impacto do fim da escala 6x1</h3><p class="for">Para condomínios, clínicas e comércio com equipes por turno.</p>
      <ul><li>Dimensionamento de postos de trabalho</li><li>Custo mensal por cenário de escala</li><li>Plano de transição com parceiros jurídico e contábil</li></ul><a href="/escala" class="link">Conhecer o KAIRON Escala →</a></article>
  </div>
</div></section>
<section id="como-funciona" class="soft"><div class="wrap">
  {head("Como funciona", "Medir, automatizar, controlar.", "Kairós, em grego, é o tempo oportuno. Nosso trabalho é fazer você decidir antes do problema.")}
  {steps([("Medir", "Mapeamos como o trabalho acontece hoje: tempos, custos, prazos e gargalos."), ("Automatizar", "Eliminamos tarefas repetitivas e conectamos planilhas e sistemas que não conversam."), ("Controlar", "Entregamos um painel com indicadores e alertas para acompanhar toda semana.")], 3)}
</div></section>
<section id="para-quem"><div class="wrap">
  {head("Para quem", "Feito para operações reais, não para apresentação.")}
  {tiles([("Condomínios", "Dimensionamento da portaria, automação da administração e controle da reforma da fachada."), ("Construtoras", "Controle físico-financeiro, relatórios automáticos para o cliente e planejamento das próximas obras."), ("Clínicas", "Escala da recepção, agendamento e confirmação automática, painel de ocupação da agenda."), ("Comércio e serviços", "Atendimento no WhatsApp, controle em planilha e relatórios de vendas automáticos.")], 4)}
</div></section>
<section class="soft"><div class="wrap split">
  {head("Quem está por trás", "Rigor de grandes projetos, no tamanho da sua empresa.", "Equipe com formação em engenharia de produção e civil, experiência em planejamento de projetos de grande porte e em transformação digital no setor público.")}
  <ul class="checks"><li><b>Automação premiada</b> no atendimento ao cidadão no setor público</li><li><b>Planejamento de grande porte</b>: cronograma e custo em projetos complexos</li><li><b>Lean e Seis Sigma</b>: medir antes de mudar</li><li><b>Implantação com as pessoas</b>: a automação tira o repetitivo, não o emprego</li></ul>
</div></section>
<section id="duvidas"><div class="wrap">{head("Dúvidas frequentes", "Antes de conversar.")}{faq_html(home_faq)}</div></section>
{final_cta("Descubra onde sua operação perde tempo e dinheiro.", "Em até 5 dias úteis você recebe um resumo das oportunidades de maior retorno, seja qual for a frente. Sem compromisso.", CHALLENGES)}"""
home_ld = [faq_ld(home_faq),
           {"@type": "ProfessionalService", "@id": f"{SITE}/#service", "name": "KAIRON", "url": f"{SITE}/",
            "email": "contato@kaironbr.com", "telephone": f"+{WA}", "priceRange": "$$",
            "parentOrganization": {"@id": f"{SITE}/#org"},
            "address": {"@type": "PostalAddress", "addressLocality": "Rio de Janeiro", "addressRegion": "RJ", "addressCountry": "BR"},
            "areaServed": ["Rio de Janeiro", "São Paulo"],
            "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": f"{SITE}/{u}"}}
                           for n, u in [("KAIRON Bots: automação e IA para PMEs", "bots"), ("KAIRON Obras: project controls para obras", "obras"), ("KAIRON Escala: estudo de impacto da escala 6x1", "escala")]]
                          + [{"@type": "Offer", "price": "0", "priceCurrency": "BRL", "itemOffered": {"@type": "Service", "name": "Diagnóstico gratuito"}}]}]

# ---------------------------------------------------------------- BOTS
bots_faq = [
    ("Preciso trocar de sistema?", "Não. A KAIRON conecta o que você já usa: WhatsApp, e-mail, planilhas, Google ou Microsoft 365."),
    ("E se a automação errar?", "Toda automação tem pontos de revisão humana e alertas. Decisões importantes continuam com a sua equipe."),
    ("Meus dados ficam seguros?", "Os dados ficam nas suas contas e ferramentas. A KAIRON segue a LGPD e acessa só o necessário."),
    ("Quanto tempo leva?", "Você vê a primeira automação funcionando em protótipo em cerca de 5 dias. Depois vêm ajustes, treinamento e documentação."),
    ("Que tipo de empresa atendem?", "Pequenas e médias empresas de serviço, clínicas, condomínios, administradoras, escritórios e comércio, no Rio de Janeiro, em São Paulo ou remotamente."),
]
bots_body = hero(
    "KAIRON Bots · Automação e IA para pequenas e médias empresas",
    "Sua equipe no que importa. <em>O repetitivo fica com os robôs.</em>",
    "Automatizamos atendimento no WhatsApp, planilhas, documentos e relatórios com as ferramentas que sua empresa já usa. Sem software caro e sem custo fixo alto.",
    "Mapear minhas rotinas", ("O que automatizamos", "#automatizamos"),
    ["Mapeamento inicial gratuito", "Protótipo em cerca de 5 dias", "Revisão humana onde importa"],
    notes([("WhatsApp · Cliente", "09:12", "Quero remarcar meu horário", "Mensagem recebida às 21h, fora do expediente."),
           ("Robô KAIRON", "09:12", "Mostra horários livres e confirma", "Sem fila, sem atendente."),
           ("Agenda e planilha", "09:13", "Atualizadas sozinhas", "Confirmação enviada ao cliente."),
           ("Equipe", "agora", "Recebe só o que precisa de decisão", "O resto já foi resolvido.")]))
bots_body += f"""
<section class="soft"><div class="wrap">
  {head("Reconhece alguma destas cenas?", "O dia some em tarefas que uma máquina faria melhor.")}
  {pains([("Mesmas perguntas, o dia todo", "Horário, preço, endereço, segunda via. Respondidos um a um no WhatsApp."), ("Relatório montado à mão", "Toda semana alguém copia, cola e formata a mesma planilha."), ("Dados digitados duas vezes", "Do sistema para a planilha, da planilha para o e-mail."), ("Documentos conferidos um a um", "Notas, contratos e comprovantes revisados no olho, com risco de erro.")])}
</div></section>
<section id="automatizamos"><div class="wrap">
  {head("O que automatizamos", "Quatro frentes, sempre com as suas ferramentas.")}
  <div class="grid g4">
    <div class="tile">{icon("<path d='M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z'/>")}<h3>Atendimento</h3><p>Triagem, respostas frequentes, agendamento e confirmação no WhatsApp e no e-mail.</p></div>
    <div class="tile">{icon("<rect x='4' y='4' width='16' height='16' rx='3'/><path d='M8 15v-3M12 15V9M16 15v-5'/>")}<h3>Planilhas e relatórios</h3><p>Painéis em Power BI e planilhas que se atualizam sozinhas a partir das suas fontes.</p></div>
    <div class="tile">{icon("<path d='M7 3h7l5 5v13H7z'/><path d='M14 3v5h5M10 13h6M10 17h6'/>")}<h3>Documentos</h3><p>Leitura, classificação e conferência de documentos com IA, com revisão humana onde importa.</p></div>
    <div class="tile">{icon("<rect x='5' y='8' width='14' height='11' rx='3'/><path d='M12 4v4M9 13h.01M15 13h.01'/>")}<h3>Agentes de IA</h3><p>Assistentes que executam rotinas internas e avisam a equipe quando algo precisa de atenção.</p></div>
  </div>
</div></section>
<section class="soft"><div class="wrap">
  {head("Como funciona", "Do mapeamento ao suporte, em quatro passos.")}
  {steps([("Mapeamento", "Listamos as rotinas e medimos quanto tempo cada uma consome."), ("Protótipo", "Você vê a primeira automação funcionando em cerca de 5 dias."), ("Implantação", "Ajustamos, treinamos a equipe e documentamos o fluxo."), ("Suporte", "Monitoramos e evoluímos as automações todo mês.")], 4)}
</div></section>
<section id="pacotes"><div class="wrap">
  {head("Pacotes", "Comece por uma rotina. Cresça quando fizer sentido.", "Preço fechado depois do mapeamento gratuito.")}
  {prices([("Automação pontual", "Preço fechado sob consulta", ["Uma rotina automatizada de ponta a ponta", "Documentação e treinamento", "30 dias de ajustes"], "Começar por uma rotina", False),
           ("Pacote de rotinas", "Preço fechado sob consulta", ["Várias rotinas integradas", "Painel de acompanhamento", "Agente de IA para a equipe"], "Solicitar proposta", True),
           ("Suporte mensal", "Mensalidade sob consulta", ["Monitoramento das automações", "Novas melhorias todo mês", "Atendimento prioritário"], "Falar com a equipe", False)])}
</div></section>
<section class="soft"><div class="wrap">{head("Perguntas frequentes", "Antes de automatizar.")}{faq_html(bots_faq)}</div></section>
<section style="padding-bottom:0"></section>
{final_cta("Qual rotina toma mais tempo da sua equipe?", "Conte para nós. O mapeamento inicial é gratuito e você recebe as oportunidades de maior retorno em até 5 dias úteis.", CHALLENGES, 0)}"""
bots_ld = [faq_ld(bots_faq), service_ld("KAIRON Bots", "Automação de atendimento no WhatsApp, planilhas, documentos e relatórios com IA para pequenas e médias empresas, usando as ferramentas que a empresa já usa.", f"{SITE}/bots", ["Automação pontual", "Pacote de rotinas", "Suporte mensal"])]

# ---------------------------------------------------------------- OBRAS
obras_faq = [
    ("Preciso comprar algum software?", "Não. A KAIRON trabalha com Excel, MS Project e Power BI. Se a obra já usa um sistema de gestão, integramos com ele."),
    ("Vocês ficam no canteiro?", "O controle é feito à distância, com visitas de medição conforme o plano contratado."),
    ("A obra já começou. Ainda dá tempo?", "Sim. Reconstruímos a linha de base a partir do que já foi executado e passamos a controlar dali em diante."),
    ("Atendem fora do Rio de Janeiro?", "O foco é o Rio de Janeiro. Obras em outras cidades são avaliadas caso a caso."),
    ("O que é curva S?", "É o gráfico do avanço acumulado da obra ao longo do tempo, comparando o planejado com o realizado. Mostra cedo se a obra está atrasando ou gastando acima do previsto."),
]
curva = ("<svg viewBox='0 0 320 170' width='100%' role='img' aria-label='Curva S planejado versus real'>"
         "<g stroke='#E7E3DC'><line x1='20' y1='150' x2='310' y2='150'/><line x1='20' y1='110' x2='310' y2='110'/>"
         "<line x1='20' y1='70' x2='310' y2='70'/><line x1='20' y1='30' x2='310' y2='30'/></g>"
         "<path d='M20 148 C 90 145, 120 120, 160 85 S 250 32, 310 28' fill='none' stroke='#1C1B19' stroke-width='2.5'/>"
         "<path d='M20 148 C 90 147, 120 132, 160 106 S 190 92, 205 88' fill='none' stroke='#C9A46A' stroke-width='3'/>"
         "<circle cx='205' cy='88' r='5' fill='#8A5A1F'/></svg>")
obras_visual = (f"<div class='panel'><div class='ptitle'><b>Curva S · planejado x real</b><span>Semana 18</span></div>{curva}"
                "<div class='legend'><span><i style='background:#1C1B19'></i>Planejado</span><span><i style='background:#C9A46A'></i>Real</span></div>"
                "<div class='alert'>Alerta: desvio acima da tolerância na estrutura</div></div>")
obras_body = hero(
    "KAIRON Obras · Project controls para obras de médio porte no RJ",
    "Sua obra no prazo e no orçamento, <em>com números toda semana.</em>",
    "Montamos e operamos o controle da sua obra: cronograma físico-financeiro, medição, custo e riscos num painel único. Você decide com o atraso ainda pequeno.",
    "Enviar o cronograma da obra", ("Ver como funciona", "#como-funciona"),
    ["Raio-x em 5 dias úteis", "Engenharia civil e de produção", "Sem software caro"], obras_visual)
obras_body += f"""
<section class="soft"><div class="wrap">
  {head("O problema", "O atraso não aparece de repente.", "Ele se acumula em silêncio quando o físico está numa planilha, o financeiro em outra e a medição chega semanas depois.")}
  {pains([("Cronograma esquecido", "Feito para aprovar a obra e não atualizado depois."), ("Medição solta", "Avanço medido à mão, sem ligação com o orçamento."), ("Custo sem alerta", "O estouro só aparece no fechamento do mês."), ("Empreiteiros sem controle", "Pagamento sem conferência do que foi executado.")])}
</div></section>
<section><div class="wrap split">
  {head("A solução", "Um escritório de controle de obra, sem montar um escritório.", "Você mantém a engenharia de campo. Nós cuidamos do controle: atualizamos o cronograma, cruzamos medição e custo e entregamos o painel e o relatório semanal prontos para a diretoria ou para o cliente final.")}
  <ul class="checks"><li>Método de controle de grandes projetos aplicado à obra média</li><li>Engenharia civil e engenharia de produção na mesma equipe</li><li>Painel que se atualiza com automação, não com retrabalho</li><li>Sem software caro: usamos o que você já tem</li></ul>
</div></section>
<section id="como-funciona" class="soft"><div class="wrap">
  {head("Como funciona", "Do diagnóstico ao encerramento.")}
  {steps([("Diagnóstico", "Você envia cronograma e orçamento. Devolvemos um raio-x dos riscos de prazo e custo."), ("Setup", "Estruturamos EAP, linha de base, curva S, critérios de medição e o painel."), ("Acompanhamento", "Medição, atualização e relatório toda semana, com alertas de desvio."), ("Entrega", "Relatório de encerramento com o histórico de prazo, custo e lições para a próxima obra.")], 4)}
</div></section>
<section><div class="wrap">
  {head("O que você recebe", "Seis entregas que tiram a obra do escuro.")}
  {tiles([("Cronograma físico-financeiro", "Atividades, caminho crítico e desembolso previsto por mês."), ("Curva S planejado x real", "O avanço da obra em uma imagem, atualizada toda semana."), ("Boletim de medição", "Base para pagar empreiteiros pelo que foi de fato executado."), ("Painel em Power BI", "Prazo, custo e avanço no celular, sem depender de planilha."), ("Alertas de desvio", "Aviso automático quando prazo ou custo saem da tolerância."), ("Matriz de riscos", "Riscos priorizados, com responsável e plano de resposta.")], 3)}
</div></section>
<section id="pacotes" class="soft"><div class="wrap">
  {head("Pacotes", "Comece pelo diagnóstico.", "O plano mensal é onde o controle gera resultado.")}
  {prices([("Diagnóstico", "Preço fechado sob consulta", ["Análise do cronograma e do orçamento", "Riscos de prazo e custo priorizados", "Entrega em 5 dias úteis"], "Pedir diagnóstico", False),
           ("Setup do controle", "Preço fechado sob consulta", ["EAP, linha de base e curva S", "Critérios de medição", "Painel Power BI configurado"], "Solicitar proposta", False),
           ("Controle mensal", "Mensalidade sob consulta", ["Medição e atualização semanais", "Relatório executivo e alertas", "Reunião quinzenal de análise"], "Falar com a equipe", True)])}
</div></section>
<section><div class="wrap">
  {head("Para quem", "Obras de médio porte que não podem atrasar.")}
  {tiles([("Construtoras", "Pequenas e médias, com equipe de campo enxuta."), ("Incorporadoras", "Várias obras em paralelo e um painel só."), ("Retrofit e reformas", "Reformas comerciais com prazo curto e cliente exigente."), ("Condomínios", "Obra de fachada, telhado ou áreas comuns, com prestação de contas aos condôminos.")], 4)}
</div></section>
<section class="soft"><div class="wrap">{head("Perguntas frequentes", "Antes de enviar o cronograma.")}{faq_html(obras_faq)}</div></section>
<section style="padding-bottom:0"></section>
{final_cta("Envie o cronograma da sua obra.", "Devolvemos um raio-x de prazo e custo em até 5 dias úteis.", CHALLENGES, 1)}"""
obras_ld = [faq_ld(obras_faq), service_ld("KAIRON Obras", "Project controls para obras de médio porte no Rio de Janeiro: cronograma físico-financeiro, curva S, boletins de medição, controle de custos, painel em Power BI e alertas de desvio.", f"{SITE}/obras", ["Diagnóstico de cronograma e orçamento", "Setup do controle", "Controle mensal"])]

# ---------------------------------------------------------------- ESCALA
escala_faq = [
    ("A escala 6x1 já acabou?", "Acompanhe o andamento oficial da proposta no Congresso. O estudo prepara você para qualquer desfecho, com cenários calculados antes da decisão."),
    ("Quais dados vocês precisam?", "A escala atual, o quadro de funcionários por posto e o horário de funcionamento. Dados pessoais não são necessários."),
    ("Serve para portaria terceirizada?", "Sim. O estudo ajuda a negociar o novo contrato com a empresa prestadora usando números próprios."),
    ("O estudo substitui orientação jurídica?", "Não. O estudo é técnico e operacional. Quando há mudança de contrato ou acordo coletivo, a KAIRON conecta você a parceiros de contabilidade e advocacia trabalhista."),
    ("Quanto custa o estudo?", "O estudo inicial é sem custo para síndicos e gestores. Em troca, pedimos um retorno sincero sobre o resultado e, se fizer sentido, uma indicação."),
]
escala_visual = ("<div class='panel'><div class='ptitle'><b>Estrutura do estudo</b><span>por posto</span></div><div class='scen'>"
                 "<div>Cenário atual (6x1)<span>calculado no estudo</span></div>"
                 "<div>Cenário 5x2<span>calculado no estudo</span></div>"
                 "<div>Cenário 12x36<span>calculado no estudo</span></div>"
                 "<div class='best'>Recomendação<span>menor custo com cobertura total</span></div></div></div>")
escala_body = hero(
    "KAIRON Escala · Estudo de impacto da escala de trabalho",
    "Quanto a mudança da escala 6x1 <em>vai custar para você?</em>",
    "A discussão sobre o fim da escala 6x1 pode mudar quantas pessoas você precisa por posto. Calculamos o impacto antes, para você decidir com números e sem susto.",
    "Pedir estudo inicial sem custo", ("Ver o que o estudo entrega", "#entregas"),
    ["Estudo inicial sem custo", "Resultado em 5 dias úteis", "Sem dados pessoais"], escala_visual)
escala_body += f"""
<section class="soft"><div class="wrap">
  {head("Para quem", "Para quem tem equipe em turnos.")}
  {tiles([("Condomínios", "Portaria, limpeza e zeladoria, com material pronto para levar à assembleia."), ("Clínicas e consultórios", "Recepção e equipe assistencial, sem buracos na agenda de atendimento."), ("Comércio e serviços", "Lojas e operações com abertura aos fins de semana.")], 3)}
</div></section>
<section id="entregas"><div class="wrap">
  {head("O que o estudo entrega", "Seis entregas para decidir com números.")}
  {tiles([("Mapa dos postos", "Cada posto, horário e cobertura atual, num só quadro."), ("Dimensionamento por cenário", "Quantas pessoas cada escala exige para manter o serviço."), ("Custo mensal comparado", "Folha e encargos estimados lado a lado."), ("Plano de transição", "O caminho recomendado, com prazos e pontos de atenção."), ("Apresentação pronta", "Para assembleia, conselho ou diretoria."), ("Onde automatizar", "Tarefas que podem sair da equipe e reduzir a necessidade de horas.")], 3)}
</div></section>
<section class="soft"><div class="wrap">
  {head("Como funciona", "Quatro passos, sem burocracia.")}
  {steps([("Envio da escala", "Você manda a escala atual e o quadro de funcionários."), ("Levantamento", "Confirmamos postos, horários e demanda real de cada turno."), ("Cenários", "Calculamos pessoas e custo para cada escala possível."), ("Apresentação", "Explicamos o resultado e entregamos o material de decisão.")], 4)}
</div></section>
<section><div class="wrap grid g2">
  <div class="note-box"><h3>Estudo inicial sem custo para síndicos e gestores</h3><p>Fazemos o primeiro estudo sem cobrar. Em troca, pedimos um retorno sincero sobre o resultado e, se fizer sentido, uma indicação para outro síndico ou gestor.</p></div>
  <div class="note-box" style="background:var(--soft)"><h3>Rede de parceiros</h3><p>Quando o estudo indica mudança de contrato ou de acordo coletivo, conectamos você a parceiros de contabilidade e de advocacia trabalhista.</p><p class="fine">O estudo é técnico e operacional e não substitui orientação jurídica.</p></div>
</div></section>
<section class="soft"><div class="wrap">{head("Perguntas frequentes", "Antes de enviar a escala.")}{faq_html(escala_faq)}</div></section>
<section style="padding-bottom:0"></section>
{final_cta("Envie a escala atual da sua equipe.", "Devolvemos o estudo inicial em até 5 dias úteis, sem custo.", CHALLENGES, 2)}"""
escala_ld = [faq_ld(escala_faq), service_ld("KAIRON Escala", "Estudo de impacto do fim da escala 6x1 para condomínios, clínicas e comércio: dimensionamento de postos, custo mensal por cenário (6x1, 5x2, 12x36) e plano de transição.", f"{SITE}/escala", ["Estudo inicial sem custo", "Plano de transição", "Apresentação para assembleia"])]


# ---------------------------------------------------------------- BLACK FRIDAY
WA_BF = f"https://wa.me/{WA}?text=" + "Ol%C3%A1!%20Quero%20garantir%20minha%20vaga%20do%20Agente%20SDR%2024h%20da%20Black%20Friday%20(R%24%20920)."
bf_faq = [
    ("O que o agente faz, exatamente?", "Responde seus clientes no WhatsApp 24 horas por dia com as informações do seu negócio, tira dúvidas de preço e horário, faz perguntas para entender o que o cliente precisa, agenda e envia ao seu vendedor um resumo de cada cliente pronto para fechar."),
    ("Além dos R$ 920, existe custo mensal?", "Os R$ 920 cobrem a implantação completa e 30 dias de ajustes. O uso do WhatsApp Business oficial e do modelo de IA tem custo variável, cobrado direto pelas plataformas conforme o volume de conversas. A KAIRON informa a estimativa para o seu volume antes de você pagar qualquer coisa."),
    ("Preciso trocar meu número de WhatsApp?", "Na maioria dos casos é possível usar o número que você já tem. Isso é confirmado na conversa inicial, antes do pagamento."),
    ("E se o cliente perguntar algo que o agente não sabe?", "O agente avisa que vai chamar alguém da equipe e transfere a conversa para um humano, com o histórico completo."),
    ("O WhatsApp permite agente de IA?", "Sim. A política do WhatsApp Business proíbe assistentes de IA de uso geral, como o ChatGPT dentro do WhatsApp, mas permite que empresas usem IA para atender e vender aos próprios clientes. É exatamente esse o uso do agente."),
    ("Em quanto tempo fica pronto?", "Em até 7 dias úteis depois que você envia as informações do negócio: serviços, preços, horários e as perguntas mais comuns dos clientes."),
    ("Como funciona o pagamento?", "Metade via Pix para reservar a vaga e metade na entrega, com o agente funcionando no seu WhatsApp."),
    ("Até quando vale a oferta?", "Até 30/11/2026 ou até acabarem as 5 vagas, o que acontecer primeiro."),
]
bf_body = f"""
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">Black Friday KAIRON · até 30/11 · 5 vagas</span>
    <h1>Seu WhatsApp atendendo e vendendo <em>24 horas por dia.</em></h1>
    <p class="lead">Um agente SDR de inteligência artificial que responde, qualifica e agenda seus clientes no WhatsApp, inclusive à noite e no fim de semana. Implantação completa por <b>R$ 920</b>.</p>
    <div class="cta-row"><a href="{WA_BF}" target="_blank" rel="noopener" class="btn btn-wa">{WA_ICON}Garantir minha vaga</a><a href="#incluido" class="btn btn-ghost">O que está incluído</a></div>
    <div class="trust"><span>Pronto em até 7 dias úteis</span><span>30 dias de ajustes</span><span>Transferência para humano</span></div>
  </div>
  <div class="visual">{notes([("WhatsApp · 23:47", "agora", "Oi! Quanto custa a limpeza de pele?", "Cliente chegou pelo Instagram."), ("Agente KAIRON", "23:47", "A partir de R$ 180. Quinta 10h ou sexta 15h?", "Respondeu em segundos."), ("Agenda", "23:48", "Sexta, 15h, confirmado", "Lembrete agendado para a véspera."), ("Para você, de manhã", "08:00", "3 clientes agendados durante a noite", "Resumo pronto no seu WhatsApp.")])}</div>
</div></section>
<section class="soft"><div class="wrap">
  {head("O problema", "O cliente fecha com quem responde primeiro.")}
  {pains([("Ninguém responde à noite", "A mensagem das 23h só é vista no dia seguinte, quando o cliente já fechou com outro."), ("Mesmas perguntas o dia todo", "Preço, horário, endereço e formas de pagamento, respondidos um a um."), ("Vendedor gastando tempo com curioso", "Quem só queria saber o preço toma o mesmo tempo de quem quer comprar."), ("Agenda feita na mão", "Marcar, remarcar e lembrar o cliente consome horas da recepção.")])}
</div></section>
<section><div class="wrap">
  {head("O que o agente faz", "Um SDR que não dorme, não esquece e não demora.")}
  {tiles([("Responde em segundos", "Dúvidas de preço, horário, serviços e pagamento, 24 horas por dia, 7 dias por semana."), ("Qualifica o cliente", "Pergunta o que o cliente precisa, quando e quanto pretende investir."), ("Agenda e lembra", "Marca horário e envia lembrete antes do atendimento."), ("Entrega o lead pronto", "Manda ao vendedor um resumo de cada cliente pronto para fechar.")], 4)}
</div></section>
<section id="incluido" class="soft"><div class="wrap split">
  {head("O que está incluído", "Implantação completa por R$ 920.", "Preço de Black Friday, válido até 30/11/2026 ou enquanto houver vagas. São 5 vagas para garantir a qualidade da implantação.")}
  <ul class="checks">
    <li>Agente de IA configurado no WhatsApp da sua empresa</li>
    <li>Treinamento com seus serviços, preços, horários e perguntas frequentes</li>
    <li>Roteiro de qualificação feito para o seu tipo de cliente</li>
    <li>Agendamento e lembretes automáticos</li>
    <li>Transferência para humano com histórico da conversa</li>
    <li>Resumo de cada lead qualificado enviado ao vendedor</li>
    <li>30 dias de ajustes depois da entrega</li>
  </ul>
</div></section>
<section><div class="wrap">
  {head("Como funciona", "Do pagamento ao agente no ar em até 7 dias úteis.")}
  {steps([("Reserva", "Você chama no WhatsApp, tira dúvidas e garante a vaga com 50% via Pix."), ("Informações", "Você envia serviços, preços, horários e as perguntas que mais recebe."), ("Implantação", "Configuramos, testamos com você e colocamos o agente no ar."), ("Ajustes", "Durante 30 dias refinamos as respostas com base nas conversas reais.")], 4)}
</div></section>
<section class="soft"><div class="wrap">
  {head("Para quem", "Para quem vende pelo WhatsApp.")}
  {tiles([("Clínicas e estética", "Agendamento, confirmação e dúvidas de procedimento."), ("Imobiliárias", "Triagem de interessados por região, valor e prazo."), ("Escolas e cursos", "Informações de turma, preço e matrícula."), ("Serviços e comércio", "Orçamento, horário de funcionamento e pedidos.")], 4)}
</div></section>
<section><div class="wrap grid g2">
  <div class="note-box"><h3>Garantia de entrega</h3><p>Se o agente não estiver funcionando no seu WhatsApp em até 7 dias úteis depois que você enviar as informações do negócio, devolvemos 100% do valor pago.</p></div>
  <div class="note-box" style="background:var(--soft)"><h3>Transparência nos custos</h3><p>Os R$ 920 são a implantação. O uso do WhatsApp oficial e da IA é cobrado direto pelas plataformas, conforme o volume. Você recebe a estimativa antes de pagar.</p></div>
</div></section>
<section class="soft"><div class="wrap">{head("Perguntas frequentes", "Antes de garantir sua vaga.")}{faq_html(bf_faq)}</div></section>
<section style="padding-bottom:0"></section>
<section id="diagnostico"><div class="wrap"><div class="final">
  <div><p class="kicker">Black Friday · até 30/11</p><h2>Garanta uma das 5 vagas.</h2><p>Implantação completa do Agente SDR 24h no seu WhatsApp por R$ 920. Chame agora e tire suas dúvidas.</p></div>
  <div style="display:flex;flex-direction:column;justify-content:center;gap:16px">
    <a href="{WA_BF}" target="_blank" rel="noopener" class="btn btn-wa" style="height:60px;font-size:17px">Garantir minha vaga no WhatsApp</a>
    <p style="font-size:15px">Ou escreva para <a href="mailto:contato@kaironbr.com" style="color:#fff;text-decoration:underline">contato@kaironbr.com</a> · WhatsApp {WA_FMT}</p>
  </div>
</div></div></section>"""
bf_ld = [faq_ld(bf_faq), {"@type": "Service", "name": "Agente SDR 24h no WhatsApp", "url": f"{SITE}/black-friday",
    "description": "Implantação de agente SDR de inteligência artificial no WhatsApp da empresa: responde, qualifica, agenda e envia leads prontos ao vendedor, 24 horas por dia.",
    "provider": {"@id": f"{SITE}/#org"}, "areaServed": ["Rio de Janeiro", "São Paulo", "Brasil"],
    "offers": {"@type": "Offer", "name": "Black Friday 2026", "price": "920", "priceCurrency": "BRL",
               "validFrom": "2026-11-23", "validThrough": "2026-11-30T23:59:59-03:00", "availability": "https://schema.org/LimitedAvailability",
               "url": f"{SITE}/black-friday"}}]

PAGES = [
    ("index", "KAIRON | Automação de processos, IA e controle de obras no RJ e SP",
     "A KAIRON automatiza atendimento, planilhas e relatórios com IA, controla prazo e custo de obras e calcula o impacto da escala 6x1. Rio de Janeiro e São Paulo. Diagnóstico gratuito.",
     home_body, home_ld, "Início"),
    ("bots", "KAIRON Bots | Automação e IA para pequenas e médias empresas",
     "Automação de atendimento no WhatsApp, planilhas, documentos e relatórios com IA para PMEs no RJ e SP. Sem software caro e sem custo fixo alto. Mapeamento gratuito.",
     bots_body, bots_ld, "KAIRON Bots"),
    ("obras", "KAIRON Obras | Controle de prazo e custo de obras no Rio de Janeiro",
     "Project controls para obras de médio porte no RJ: cronograma físico-financeiro, curva S, medição, custo e painel semanal com alertas. Raio-x em 5 dias úteis.",
     obras_body, obras_ld, "KAIRON Obras"),
    ("escala", "KAIRON Escala | Estudo de impacto do fim da escala 6x1",
     "Quanto o fim da escala 6x1 vai custar para seu condomínio, clínica ou comércio? Dimensionamento de postos e custo por cenário (6x1, 5x2, 12x36). Estudo inicial sem custo.",
     escala_body, escala_ld, "KAIRON Escala"),
    ("black-friday", "Black Friday KAIRON | Agente SDR de IA no WhatsApp 24h por R$ 920",
     "Agente SDR de inteligência artificial no seu WhatsApp: responde, qualifica e agenda clientes 24h. Implantação completa por R$ 920 até 30/11. 5 vagas.",
     bf_body, bf_ld, "Black Friday"),
]

os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
for slug, title, desc, body, ld, short in PAGES:
    with open(os.path.join(OUT, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(page(slug, title, desc, body, ld, short))
for name in ("site.css", "site.js"):
    shutil.copy(os.path.join(HERE, name), os.path.join(OUT, "assets", name))
with open(os.path.join(OUT, "assets", "favicon.svg"), "w") as f:
    f.write("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='#1C1B19'/>"
            "<path d='M10 8h12M10 24h12M11 8c0 5 10 6 10 16M21 8c0 5-10 6-10 16' stroke='#C9A46A' stroke-width='2' fill='none' stroke-linecap='round'/></svg>")

with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write("User-agent: *\nAllow: /\n\n# Buscadores e assistentes de IA liberados de propósito\n")
    for b in ["Googlebot", "Google-Extended", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "ClaudeBot",
              "Claude-User", "Claude-SearchBot", "PerplexityBot", "Applebot-Extended"]:
        f.write(f"User-agent: {b}\nAllow: /\n")
    f.write(f"\nSitemap: {SITE}/sitemap.xml\n")

with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for slug, pr in [("", "1.0"), ("bots", "0.9"), ("obras", "0.9"), ("escala", "0.9"), ("black-friday", "0.8")]:
        f.write(f"  <url><loc>{SITE}/{slug}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n")
    f.write("</urlset>\n")

with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as f:
    f.write(f"""# KAIRON

> KAIRON é uma empresa de engenharia de processos, automação com inteligência artificial e controle de obras para pequenas e médias empresas no Rio de Janeiro e em São Paulo. Lema: "Processos sob controle, no tempo certo." Contato: contato@kaironbr.com, WhatsApp {WA_FMT}. Site: {SITE}

## Soluções

- [KAIRON Bots]({SITE}/bots): automação de atendimento no WhatsApp, planilhas, documentos e relatórios com IA, usando ferramentas que a empresa já tem (Excel, Google Planilhas, Microsoft 365, Power Automate, Power BI, Python). Sem software caro e sem custo fixo alto. Protótipo em cerca de 5 dias.
- [KAIRON Obras]({SITE}/obras): project controls para obras de médio porte no RJ. Cronograma físico-financeiro, curva S, boletins de medição, controle de custos, painel em Power BI e alertas de desvio. Para construtoras, incorporadoras, retrofit e condomínios em obra.
- [KAIRON Escala]({SITE}/escala): estudo de impacto do fim da escala 6x1. Dimensionamento de postos, custo mensal por cenário (6x1, 5x2, 12x36), plano de transição e apresentação para assembleia. Para condomínios, clínicas e comércio. Estudo inicial sem custo.

## Oferta atual

- [Black Friday: Agente SDR 24h no WhatsApp]({SITE}/black-friday): implantação completa por R$ 920 até 30/11/2026, 5 vagas.

## Método

Medir (tempos, custos, prazos e gargalos), Automatizar (eliminar tarefas repetitivas e integrar planilhas e sistemas), Controlar (painel com indicadores e alertas semanais). Base em Lean e Seis Sigma, com implantação centrada nas pessoas.

## Como contratar

Diagnóstico gratuito com retorno em até 5 dias úteis, depois proposta com preço fechado. Atendimento presencial no Rio de Janeiro e em São Paulo, remoto para todo o Brasil.
""")
print("ok", OUT)
