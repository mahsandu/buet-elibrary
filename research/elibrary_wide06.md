## Facet: Live OPAC Scraping & E-Resource Authentication

### Key Findings
- There are **open-source projects that scrape or augment Koha OPAC data**, but most target enrichment rather than live availability. The BI-Library project on GitHub retrieves and displays open-access status (DOAJ/DOAB) within Koha OPAC by embedding ISSN data attributes in XSLT and querying APIs via a PHP proxy—demonstrating the exact pattern BUET could adapt for shelf-status scraping [^1]. Another project, `koha-plugin-opac-theme-galadriel`, shows how Koha plugins can inject JavaScript into the OPAC to pull live external data [^2].
- **Best practices for scraping library OPACs** are well-documented in the web-scraping industry: always check `robots.txt` first, implement **random delays** (1–3 seconds or more), rotate **User-Agent strings** and request headers, cap concurrency at 5–10 requests, and schedule jobs during off-peak hours (midnight–6 AM) to avoid impacting real users [^3][^4]. Production scrapers should use **exponential backoff with jitter** for retries (e.g., 2^attempt + random seconds), classify retryable vs. terminal errors, and log all requests [^3].
- For **dynamic or JavaScript-rendered OPAC content**, headless browsers are necessary. **Playwright** (Microsoft) is the modern recommended choice over Selenium for new Python projects: it is faster, has async-first architecture, lower block rates (~18% headless vs. Selenium's ~32%), and handles intelligent element waiting automatically [^5][^6]. **Selenium** remains viable for legacy projects or cross-browser needs, while **Pyppeteer** is Chromium-only and less actively maintained [^6].
- **EZproxy** is the dominant commercial proxy solution for off-campus database access, used by 3,600+ websites globally (Wappalyzer data). It is a URL-rewriting proxy that changes an off-campus user's apparent IP to one within the library's licensed range [^7][^8]. Pricing is typically below US $100/month (SaaS hosted) or requires a one-time license for self-hosted [^7].
- **OpenAthens** is a cloud-based, managed SAML/SSO identity service that is rapidly replacing EZproxy at major institutions (e.g., UBC, Harvard, MSU, Delaware). It offers a comprehensive admin dashboard, user management, granular reporting, and a "Where Are You From" (WAYF) federation experience. Unlike EZproxy, it does not require server management or config.txt stanza maintenance [^9][^10][^11].
- **Shibboleth** is open-source SAML software that provides SSO infrastructure but is acknowledged to be "difficult to install and manage for libraries with little experience" and requires deep campus IT collaboration [^12][^13]. OpenAthens and Shibboleth are interoperable because both use SAML standards; the difference is that OpenAthens is a managed cloud service with an SLA, while Shibboleth is self-hosted [^13][^14].
- **Open-source alternatives to EZproxy exist** but are limited and mostly proof-of-concept. GitHub projects `ffzg/via-proxy`, `alexandr-lib/no-ezproxy`, and `ajspadial-science/canciella` demonstrate Apache `mod_proxy` or nginx configurations as free alternatives, but they lack the URL-rewriting magic and extensive database stanza libraries that make EZproxy turnkey [^15][^16][^17]. A 2011 StackExchange answer and a 2017 blog post both note that a simple Apache reverse proxy can work for IP-based authentication but breaks when sites use absolute URLs or JavaScript redirects [^15][^18].
- **Muse Proxy** is a commercial alternative used by consortia such as LIRN (Library and Information Resources Network). It supports generic OAuth, LTI integration for LMS, and multitenant architecture allowing new member instances to be deployed "in a matter of minutes" [^19].
- **LDAP and SSO integration** in library discovery platforms typically follows a hub-and-spoke model: the institution's LDAP/Active Directory (or Azure AD/Google Workspace) serves as the Identity Provider (IdP), while the library system (Koha, VuFind, or discovery layer) acts as the Service Provider (SP) via SAML or OAuth2. Koha natively supports SSO via Azure AD, Shibboleth, and other SAML providers, and can manage multiple unique user identifiers (e.g., barcode + chip) [^20][^21]. ePlatform and Accessit (school library systems) show common patterns: LDAP/AD sync for patron data, SSO via SAML/OpenID for login, and SIP2 for real-time ILS authentication [^21][^22].
- **Security risks when scraping and proxying library content** include **XSS vulnerabilities** that can lead to admin session hijacking, **stored XSS via improperly sanitized input**, and **session hijacking through malicious ServiceWorkers or AppCache** [^23][^24]. Proxy servers themselves introduce risks: if a proxy config is misconfigured, users may be forced to authenticate for open resources, or session cookies may leak across domains. The HKUST library explicitly notes that EZproxy "never sends your username or password to the subscription resource" because SSL wraps the proxy session [^25].
- **In developing countries and South Asia**, the dominant challenges for e-resource access are **budget constraints**, **lack of skilled IT/library professionals**, **poor internet connectivity**, and **inadequate ICT infrastructure** [^26][^27][^28]. A 2025 study from Manipal Academy (India) found that "a significant obstacle is possible resistance from users who have grown accustomed to authentication techniques," and that "implementation of SSO is possible with the latest computer specifications, but integrating existing library applications can be tedious" [^26]. Libraries in Tanzania, Nigeria, and Kenya report similar issues: lack of funds for subscriptions, poor bandwidth, unreliable power, and inability to access e-resources off-campus due to IP limitations [^27][^28].
- **Library consortia in developing countries** have addressed proxy/auth challenges through shared infrastructure. The **Library and Information Resources Network (LIRN)** in Florida moved to Muse Proxy to give small private colleges (without IT staff) a turnkey off-campus access solution [^19]. In Africa, **INASP** and **KLISC** have supported consortium licensing and shared authentication, but budget constraints remain severe [^27]. The **Bangladesh INASP** ecosystem has historically worked through PERI/INASP for journal access, though these programs are increasingly transitioning to Research4Life.

### Major Players & Sources
- **Koha Community / Open Fifth / ByWater Solutions**: Koha is the underlying ILS BUET uses. Open Fifth and ByWater are major support providers. Koha's REST API is the preferred integration method, but BUET's SSL restrictions force scraping fallback [^20][^29].
- **BeautifulSoup / requests (Python)**: The standard stack for lightweight HTML scraping. Combined with `urllib.robotparser` for robots.txt compliance and `fake-useragent` for rotation, this is the simplest scraping path [^3][^4].
- **Playwright (Microsoft)**: The modern headless-browser automation tool recommended for dynamic content. Faster than Selenium, better at avoiding bot detection, and with a unified API across Chromium/Firefox/WebKit [^5][^6].
- **EZproxy (OCLC)**: The incumbent commercial proxy. ~3,600 live sites. URL-rewriting, cookie-based session management, extensive database stanza library. Requires config.txt maintenance. Hosted SaaS available [^7][^8].
- **OpenAthens (Jisc / Eduserv)**: Cloud-based SAML/SSO identity provider. Strong reporting, no server management, works with any SAML-compliant SP. Explicitly compared to EZproxy in migration guides (UBC, MSU, Delaware) [^9][^10][^11].
- **Shibboleth (Internet2)**: Open-source SAML IdP. High technical complexity; requires SAML expertise and campus IT collaboration. Often deployed in hybrid mode with EZproxy as a fallback [^12][^13][^14].
- **Muse Global / Muse Proxy**: Commercial proxy and federated search provider. Used by LIRN consortium. Supports OAuth, LTI, multitenant deployment. Positioned as a more flexible alternative to EZproxy for consortia [^19].
- **LibLynx**: Alternative to EZproxy offering hosted proxy + SSO + user management + portal. Mentioned in academic literature as a "vendor-neutral" option but less widely adopted [^12].
- **INASP / Research4Life / KLISC**: NGO and consortium networks supporting e-resource access in developing countries. Provide shared licensing, training, and (in some cases) proxy infrastructure for institutions that cannot afford individual subscriptions [^27][^28].
- **Oxylabs / Bright Data / ScraperAPI**: Commercial proxy and scraping infrastructure providers. They offer rotating residential IPs, CAPTCHA solving, and browser fingerprinting—relevant only if BUET's scraping scales beyond internal use [^3][^30].

### Trends & Signals
- **Trend: Migration from EZproxy to OpenAthens / SAML SSO** is accelerating. UBC (2021), Harvard (2024–2026), MSU (2026), and Delaware (2025) have all completed or begun transitions. The driver is "more secure, reliable and streamlined experience" and reduced server management burden [^9][^10][^11].
- **Trend: Headless-browser scraping is replacing simple HTTP parsers** for modern web apps. As more OPACs and vendor sites use React/Vue/Angular, Playwright or Selenium are becoming necessary. Playwright's 2020 release and Microsoft backing have made it the default for new projects [^5][^6].
- **Trend: Cloud-based authentication management** is replacing on-premise proxy servers. OpenAthens Compass offers a "comprehensive portal for managing all configuration," whereas EZproxy requires "all configuration is managed on the server" [^14]. This reduces the need for library IT staff—critical for smaller institutions.
- **Trend: Developing-country libraries are trapped between IP-authentication limitations and SSO complexity.** A 2025 comparative study notes that "a small library with a limited budget can use IP-based authentication," while "an enormous library with numerous databases without budgetary issues can opt for SSO" [^26]. This suggests a **two-tier gap** in the Global South.
- **Signal: Nginx/OpenResty as a DIY proxy** has been discussed in the library tech community since at least 2011 (ServerFault) and 2017 (Bibliographic Wilderness blog), but no mature, widely adopted open-source EZproxy replacement has emerged. The "Open Extensible Proxy" breakout session at Code4Lib attracted ~30 attendees but produced only a brainstorm [^15][^17][^18].
- **Signal: Koha's plugin architecture (KPZ)** allows JavaScript injection into the OPAC without modifying core Koha code. This means BUET could potentially build a **Koha plugin** that fetches live availability from an external scraper and displays it inline, rather than building a separate discovery layer [^2].
- **Signal: South Asian and African libraries face severe off-campus access barriers.** A Tanzania case study identified "inaccessibility of e-resources outside university premises due to IP address limitations" as a core challenge [^27]. This validates BUET's need for a centralized proxy or authentication solution.
- **Signal: Proxy stanza maintenance is a hidden labor cost.** The ALA LTR guide notes that "library proxies require the maintenance of several configuration files... URLs, hosts, and domains are grouped by platform into entries called stanzas and need to be frequently updated" [^31]. This manual overhead is a major reason institutions are moving to cloud-managed solutions.

### Controversies & Conflicting Claims
- **Scraping vs. API: Is scraping a legitimate fallback?** Industry best-practice guides say "check for a public API or direct download first" before scraping [^3]. However, BUET's explicit constraint (SSL restrictions block REST API use) makes scraping a legitimate engineering fallback, not an anti-pattern. The trade-off is fragility: if Koha's OPAC HTML changes, the scraper breaks.
- **EZproxy vs. OpenAthens: which is cheaper?** OpenAthens is a subscription SaaS; EZproxy can be self-hosted with a one-time license or hosted as SaaS. For a small institution with existing Linux sysadmin capacity, self-hosted EZproxy may be cheaper. For an institution without IT staff, OpenAthens' managed service may have lower total cost of ownership despite recurring fees. The 2025 Manipal study explicitly flags "budget" as the deciding factor [^26].
- **Shibboleth: powerful but too complex?** Multiple sources agree that Shibboleth "generally requires more technical skill to manage than does EZproxy" [^12]. OpenAthens positions itself as "an easy way for libraries with no expertise in SAML to set up an identity server" [^13]. However, OpenAthens is a vendor lock-in; Shibboleth is open-source and federated. The choice depends on whether the institution values vendor independence or operational simplicity.
- **Open-source proxy alternatives: viable or fantasy?** The `via-proxy`, `no-ezproxy`, and `canciella` projects prove that Apache/nginx can proxy traffic, but they lack the critical URL-rewriting and JavaScript-link-fixing behavior that EZproxy provides. One blogger called the nginx-replacement idea "something I won't be doing anytime soon" because of the complexity [^18]. A 2011 StackExchange answer conceded that "any absolute links in their site code... would break things" [^15]. This suggests a custom proxy is feasible only for a small, well-defined set of resources—not a full IEEE/Elsevier portfolio.
- **Security: Is proxying less secure than SSO?** SAML-based SSO (OpenAthens/Shibboleth) is generally considered more secure than cookie-based IP proxying because it eliminates the need to share IP ranges and reduces session-hijacking surface. However, SSO introduces its own risks: if the IdP is compromised, all services are compromised. EZproxy's SSL-wrapped sessions do not expose credentials to vendors, but cookie theft remains a risk if the proxy server is misconfigured [^25].
- **Playwright vs. Selenium for library scraping**: Playwright is faster and more modern, but Selenium has broader language support and a larger community. For a Python-only project, Playwright is the consensus choice; for a project that might need Java or C# integration, Selenium retains an advantage [^6].

### Recommended Deep-Dive Areas
- **Koha OPAC Scraping Architecture**: BUET should prototype a BeautifulSoup + requests scraper against its own Koha OPAC to identify the exact CSS selectors for shelf status, item availability, and hold counts. It should test whether Playwright is needed (if Koha renders items via JavaScript) or if static HTML parsing suffices. This is a high-priority, low-cost spike.
- **Koha Plugin as OPAC Enricher**: Rather than building a separate discovery layer, BUET could investigate writing a **Koha Plugin (KPZ)** that injects JavaScript into the OPAC to call a microservice for live availability. This would keep the user in Koha's native interface while adding the missing real-time data. The `galadriel` plugin and BI-Library's open-access project provide code patterns [^1][^2].
- **Proxy Solution TCO Analysis**: BUET should compare total cost of ownership for (a) self-hosted EZproxy, (b) OpenAthens subscription, (c) a minimalist Apache/nginx reverse proxy for a small set of core databases (IEEE, Elsevier), and (d) VPN-based access. Given Bangladeshi budget constraints, a self-hosted EZproxy or nginx solution may be most viable, but the maintenance burden must be modeled.
- **LDAP/SSO Integration with Koha**: BUET's campus likely already has Active Directory or an LDAP directory. Deep-diving into Koha's native LDAP patron authentication and SAML/SSO support (via Azure AD or a local Shibboleth IdP) would determine whether patron login can be unified before the proxy layer is even addressed. Koha's support for "more than one unique user number" is relevant for students with both barcode and chip IDs [^20].
- **Security Hardening for Scrapers and Proxies**: If BUET deploys a scraper, it must handle session cookies securely, validate all scraped input before rendering, and avoid becoming an open proxy. A security review should cover XSS prevention in any scraped-data display, rate-limiting to prevent abuse, and SSL/TLS configuration for the proxy server.
- **South Asian Consortium Models**: Investigating whether Bangladeshi libraries (e.g., through UGC or BANSDOC) can join or form a consortium for shared e-resource licensing and proxy infrastructure. The LIRN model (Muse Proxy for small private colleges) and INASP/Research4Life models are directly relevant [^19][^27].

---

[^1]: BI-Library. "Retrieving and showing open access status within Koha OPAC." GitHub. 2023. https://github.com/BI-Library/retrieving-and-showing-open-access-status-within-Koha-OPAC

[^2]: ByWater Solutions. "Koha OPAC Theme plugin - Galadriel." GitHub. 2018. https://github.com/bywatersolutions/koha-plugin-opac-theme-galadriel

[^3]: Oxylabs. "Web Scraping Best Practices: Complete 2026 Guide." 2024/2026. https://oxylabs.io/blog/web-scraping-best-practices

[^4]: IJNRD. "Web Scraping: Leveraging the Power of Python, APIs, and Automation." PDF. https://www.ijnrd.org/papers/IJNRD2403143.pdf

[^5]: Froxy Blog. "How to Scrape Websites with Dynamic Content." 2025. https://blog.froxy.com/en/web-scraping-dynamic-content

[^6]: Firecrawl Blog. "How to Scrape Dynamic Websites with Headless Browsers in Python." 2025. https://www.firecrawl.dev/blog/headless-web-scraping-dynamic-websites

[^7]: Wappalyzer. "Websites using EZproxy." https://www.wappalyzer.com/technologies/reverse-proxies/ezproxy/

[^8]: Electronic Resource Management in Libraries. PDF. http://pustaka.unp.ac.id/file/abstrak_kki/EBOOKS/LIBRARIES%2C%20ELECTRONIC%20INFORMATION%20RESOURCES%20%20Electronic%20resource%20management%20in%20libraries%2C%20research%20and%20practice.pdf

[^9]: UBC Library. "OpenAthens transforms user access to library resources, replacing EZproxy and IP address authentication." 2021. https://about.library.ubc.ca/2021/06/02/openathens-transforms-user-access-to-library-resources-replacing-ezproxy-and-ip-address-authentication/

[^10]: MSU Libraries. "MSU Libraries to begin transition from EZproxy to OpenAthens in May." 2026. https://lib.msu.edu/news/article/2026-04/msu-libraries-begin-transition-ezproxy-openathens-may-news-articles

[^11]: University of Delaware Library. "OpenAthens FAQs." 2026. https://library.udel.edu/services/connect/openathens-faqs/

[^12]: ALA Library Technology Reports. "Techniques for Electronic Resource Management: TERMS and the Transition to Open." PDF. https://pdfs.semanticscholar.org/e5b2/50757a0fcabdaf434bd6a0bdd6f727c1fa87.pdf

[^13]: ALA / OpenAthens. "What Is the Difference between Shibboleth and OpenAthens?" PDF. https://alatest.pkpps03.publicknowledgeproject.org/index.php/ltr/article/download/7849/10935

[^14]: OpenAthens. "OpenAthens Compass or Shibboleth?" 2025. https://www.openathens.net/librarians/openathens-compass/

[^15]: ServerFault. "Open Source (Free) alternative to EZProxy." 2011. https://serverfault.com/questions/341696/open-source-free-alternative-to-ezproxy

[^16]: GitHub. "ffzg/via-proxy: Free EzProxy alternative for our library using Apache config." 2018. https://github.com/ffzg/via-proxy

[^17]: GitHub. "ajspadial-science/canciella: A free software alternative to EZProxy." 2016. https://github.com/ajspadial-science/canciella

[^18]: Bibliographic Wilderness. "Idea I won't be doing anytime soon of the week: replace EZProxy with nginx." 2017. https://bibwild.wordpress.com/2017/03/03/idea-i-wont-be-doing-anytime-soon-of-the-week-replace-ezproxy-with-nginx/

[^19]: Library Journal. "LIRN Consortium Implements New Proxy Platform." 2018. https://www.libraryjournal.com/story/lirn-consortium-implements-new-proxy-platform

[^20]: OpenFifth. "Koha LMS for academic libraries." 2026. https://openfifth.co.uk/koha-lms-for-academic-libraries/

[^21]: ePlatform. "Your Guide to LMS and SSO Integrations on ePlatform." 2025. https://www.eplatform.co/hk/blog/2025/lms-and-sso-integration-guide/

[^22]: Accessit Library. "Partners and Integrations." 2026. https://accessitlibrary.com/integrations/

[^23]: Rewterz. "Stored XSS in Ivanti EPM Allows Admin Session Hijacking." 2025. https://rewterz.com/threat-advisory/stored-xss-in-ivanti-epm-allows-admin-session-hijacking

[^24]: Nuclear'Atk Security Lab. "利用 Appcache 和 ServiceWorker 进行持久型session hijacking 和 XSS." 2015. https://lcx.cc/post/4564/

[^25]: HKUST Library. "EZProxy: Off-Campus Access to Subscription Resources." 2023/2026. https://library.hkust.edu.hk/find-borrow/resources/ezproxy-campus-access-subscription-resources

[^26]: Mattigiri, M. T., Rao, M., & Bhat K. S. "A Comparative Analysis of Single Sign-On and Proxy Solutions for Facilitating Remote Access to Electronic Resources in Academic Libraries." DESIDOC Journal of Library & Information Technology, 45(1), 2025. http://publicationsdrdo.in/index.php/djlit/article/download/19823/8488/88541

[^27]: Mkolo, A. "Examining the Availability and Use of Electronic Resources... Muhimbili University." Tanzania. PDF. http://repository.out.ac.tz/2985/1/AGNES%20%20MKOLO%20tyr.pdf

[^28]: Ani et al. "An Overview of Application of E-Resources as Strategies for Enhancing Effective Library Services in Academic Libraries." PDF. https://pdfs.semanticscholar.org/a5e5/61556cc2e7047ba6b0b81982d3d7ebce073a.pdf

[^29]: ScraperAPI. "Best User Agent List for Web Scraping in 2026 with Examples." 2026. https://www.scraperapi.com/web-scraping/best-user-agent-list-for-web-scraping/

[^30]: Bright Data. "How to Fix Inaccurate Web Scraping Data." 2026. https://brightdata.com/blog/web-data/fix-inaccurate-web-scraping-data

[^31]: ALA Library Technology Reports. "The Current Landscape of Electronic Resources Access Issues." PDF. https://journals.ala.org/index.php/ltr/issue/download/844/610
