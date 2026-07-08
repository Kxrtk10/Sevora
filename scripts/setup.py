from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]


PRODUCTS = {
    "Forge": "An internal and external toolkit for building reliable AI-enabled workflows, automations, and product prototypes.",
    "FuelFlow": "A business operations product for tracking revenue, pipeline, delivery capacity, and execution health.",
    "Ember": "A relationship and retention product for turning customer signals into timely, useful action.",
    "Astra": "A decision intelligence product for leaders who need clear visibility across strategy, metrics, and risk.",
    "StockSage": "An investing research assistant focused on disciplined analysis, watchlists, and market learning.",
    "Raasta": "A navigation and planning product for local commerce, logistics, and route-aware service experiences.",
}


SOLUTIONS = {
    "Healthcare": ("Healthcare", "administrative overload, patient follow-up gaps, fragmented records, staff scheduling pressure", "intake assistants, care-plan copilots, triage workflows, document automation"),
    "Restaurants": ("Restaurants", "thin margins, inconsistent demand, manual inventory, slow customer feedback loops", "demand forecasting, menu analytics, reservation copilots, review intelligence"),
    "Education": ("Education", "teacher workload, uneven student support, curriculum planning, parent communication", "lesson copilots, adaptive tutoring, progress dashboards, administrative automation"),
    "Enterprise": ("Enterprise", "knowledge silos, slow internal processes, disconnected tools, unclear operating metrics", "internal copilots, workflow automation, executive dashboards, knowledge retrieval"),
    "Manufacturing": ("Manufacturing", "downtime, quality drift, inventory waste, safety compliance", "predictive maintenance, inspection assistants, supply planning, SOP copilots"),
    "Hospitality": ("Hospitality", "guest service delays, staffing volatility, inconsistent personalization, review management", "guest concierges, operations dashboards, sentiment analysis, staff workflow tools"),
    "Fitness": ("Fitness", "member churn, generic programming, manual coaching follow-up, weak community loops", "personalized plans, retention signals, coach copilots, habit tracking"),
    "Retail": ("Retail", "stockouts, low conversion, support load, limited personalization", "inventory intelligence, shopping assistants, merchandising analytics, support automation"),
    "RealEstate": ("Real Estate", "lead qualification, document complexity, slow follow-up, market research burden", "listing copilots, lead scoring, document summaries, neighborhood intelligence"),
}


FILES = {
    ".gitignore": """
        # Python
        __pycache__/
        *.py[cod]
        .venv/
        venv/

        # Node and web tooling
        node_modules/
        dist/
        build/
        .next/

        # Environment and local secrets
        .env
        .env.*
        !.env.example

        # OS and editor files
        .DS_Store
        Thumbs.db
        .vscode/
        .idea/

        # Generated exports
        exports/
        tmp/
    """,
    "LICENSE": """
        Copyright (c) 2026 Sevora

        All rights reserved.

        This repository contains the internal operating system, strategy, and intellectual property of Sevora. No part of this repository may be copied, modified, distributed, sublicensed, or used outside Sevora without written permission.
    """,
    "README.md": """
        # SevoraOS v1

        SevoraOS is the operating system for Sevora: the place where the company records its strategy, products, brand, sales motion, research, and operating principles.

        This repository is not a client project and it is not one of Sevora's products. It is the brain of the company: a durable internal system designed to help Sevora make better decisions, build better software, and compound knowledge over the next decade.

        ## What Sevora Is

        Sevora is an AI Product Studio. We build intelligent software, develop our own products, and solve real business problems for companies through practical AI systems.

        Sevora is not an agency. We do not exist to sell hours. We exist to create useful technology, own durable product IP, and help serious businesses adopt AI with clarity.

        ## Mission

        To build intelligent products and systems that help companies operate with more speed, insight, and leverage.

        ## Vision

        Sevora will become a global technology company known for building thoughtful AI products, trusted business systems, and category-defining software.

        ## Philosophy

        We believe AI should make work clearer, not noisier. Great software should feel calm, capable, and deeply useful. Sevora will prioritize durable products, sharp execution, honest research, and long-term trust over short-term hype.

        ## What We Build

        Sevora builds across three connected tracks:

        - Owned products that can scale into independent businesses.
        - Industry solutions that solve repeated, high-value problems for companies.
        - Internal systems that make Sevora more focused, organized, and operationally excellent.

        ## Repository Structure

        - [docs](docs/) contains the company's foundations, strategy, and operating records.
        - [website](website/) defines Sevora's public web presence and content roadmap.
        - [products](products/) tracks product ideas, status, and long-term direction.
        - [solutions](solutions/) organizes industry problem spaces and AI solution opportunities.
        - [branding](branding/) captures identity, voice, design principles, and visual systems.
        - [sales](sales/) defines the commercial motion, discovery process, and proposal approach.
        - [operations](operations/) documents how the company runs.
        - [research](research/) collects AI, industry, competitor, and future product research.
        - [assets](assets/) stores brand and product media.
        - [scripts](scripts/) contains maintenance utilities for SevoraOS.

        ## Long-Term Roadmap

        1. Establish the foundation: mission, principles, product map, brand, and operating rhythm.
        2. Build the first credible public website and product narrative.
        3. Validate initial solution categories through focused discovery and prototypes.
        4. Convert repeated service patterns into reusable products and platforms.
        5. Create a portfolio of owned products supported by strong research and distribution.
        6. Evolve SevoraOS into a living company intelligence layer with dashboards, decision history, and AI-assisted planning.

        ## Contribution Guidelines

        - Keep documentation concise, specific, and useful.
        - Prefer clear decisions over vague brainstorming.
        - Link related documents instead of duplicating information.
        - Update decision logs when strategy changes.
        - Treat this repository as a long-term company asset.

        ## Future SevoraOS Vision

        SevoraOS should eventually become more than documentation. It should become an internal intelligence system that connects goals, research, products, customer insights, financial models, delivery workflows, and company memory.

        The goal is simple: as Sevora grows, the company should become more coherent, not more chaotic.
    """,
    "docs/foundations/Mission.md": """
        # Mission

        Sevora's mission is to build intelligent products and systems that help companies operate with more speed, insight, and leverage.

        We focus on real business problems: repetitive workflows, fragmented information, slow decisions, weak customer follow-up, and missed operational signals. AI is valuable when it improves outcomes, reduces friction, or creates new capabilities that were previously too expensive or complex.

        ## Mission Commitments

        - Build software that solves meaningful problems.
        - Turn repeated business pain into reusable product systems.
        - Use AI responsibly, practically, and with measurable value.
        - Create long-term assets instead of one-off deliverables.
        - Help customers become more capable, not more dependent.
    """,
    "docs/foundations/Vision.md": """
        # Vision

        Sevora will become a global technology company known for building thoughtful AI products, trusted business systems, and category-defining software.

        The company begins as a focused AI Product Studio, but the long-term ambition is larger: a portfolio of products, platforms, and operating knowledge that compounds over time.

        ## Ten-Year Direction

        - Build products that serve real industries.
        - Develop a repeatable system for discovering and validating AI opportunities.
        - Create a recognizable product and design standard.
        - Grow from studio execution into durable software ownership.
        - Become a company that talented people are proud to build with.
    """,
    "docs/foundations/Manifesto.md": """
        # Manifesto

        Sevora exists because AI should become useful infrastructure, not theater.

        We are interested in the quiet power of better systems: fewer manual tasks, faster decisions, cleaner operations, and software that understands the shape of a business. We respect craft. We respect customers. We respect the difference between a demo and a product.

        We will build with ambition, but also with restraint. The best technology companies are not built by chasing every trend. They are built by choosing important problems and solving them with taste, discipline, and persistence.

        Sevora will be a company that learns in public, thinks in systems, and builds for decades.
    """,
    "docs/foundations/CoreValues.md": """
        # Core Values

        ## Usefulness First

        Every product, document, workflow, and decision should make the company or customer more capable.

        ## Long-Term Craft

        We optimize for durable quality. Speed matters, but not at the cost of trust.

        ## Clear Thinking

        We write things down, define terms, and make decisions visible.

        ## Product Ownership

        We prefer reusable systems and owned IP over disposable work.

        ## Customer Respect

        We solve real problems, communicate honestly, and avoid selling complexity for its own sake.
    """,
    "docs/foundations/CompanyPrinciples.md": """
        # Company Principles

        - Start with the problem, not the model.
        - Build small, useful systems before large speculative platforms.
        - Document decisions so future teams understand the reasoning.
        - Convert repeated work into reusable assets.
        - Protect focus. A company cannot become excellent at everything at once.
        - Keep the customer close to the product process.
        - Measure outcomes, not activity.
    """,
    "docs/strategy/BusinessModel.md": """
        # Business Model

        Sevora's business model combines product ownership with high-value AI solution development.

        ## Core Tracks

        - Product Studio: build and validate owned software products.
        - Solution Partnerships: solve repeated AI and automation problems for businesses.
        - Platform Assets: convert repeated delivery patterns into reusable internal tools and future products.

        ## Strategic Intent

        Revenue from client-facing work should fund product development, deepen market understanding, and reveal repeatable opportunities. Over time, owned products should become a larger share of company value.
    """,
    "docs/strategy/IdealClients.md": """
        # Ideal Clients

        Sevora is best suited for companies with real operational complexity and a willingness to improve how work gets done.

        ## Strong Fits

        - Growing businesses with manual workflows.
        - Industry operators with domain knowledge but limited AI capability.
        - Teams with fragmented tools, data, or customer processes.
        - Founders and leaders who want practical systems, not novelty demos.

        ## Weak Fits

        - Organizations seeking vague AI experimentation without a business problem.
        - Teams unwilling to provide process access or feedback.
        - Buyers who value the lowest upfront price over long-term outcomes.
    """,
    "docs/strategy/GrowthRoadmap.md": """
        # Growth Roadmap

        ## Phase 1: Foundation

        Establish SevoraOS, brand direction, website, first product concepts, and a focused solution portfolio.

        ## Phase 2: Validation

        Run discovery with target industries, build demos, document repeatable pain points, and secure early customers.

        ## Phase 3: Productization

        Turn repeated solutions into reusable modules, templates, and product candidates.

        ## Phase 4: Scale

        Grow owned products, hire specialized talent, expand distribution, and build stronger internal operating systems.
    """,
    "docs/strategy/RevenueModel.md": """
        # Revenue Model

        Sevora should develop multiple revenue streams without diluting focus.

        ## Potential Streams

        - Fixed-scope AI product builds.
        - Monthly retainers for ongoing optimization and support.
        - SaaS subscriptions for owned products.
        - Usage-based pricing for workflow automation or AI infrastructure.
        - Strategic partnerships with industry operators.

        The long-term goal is to increase recurring and product-led revenue while using services selectively to learn, fund, and validate.
    """,
    "docs/strategy/PricingPhilosophy.md": """
        # Pricing Philosophy

        Sevora should price based on value, clarity, and seriousness.

        Low prices create weak commitment and make excellent work harder. High prices must be justified by strong discovery, clear scope, professional delivery, and measurable outcomes.

        ## Principles

        - Prefer transparent packages over vague hourly work.
        - Price discovery separately when the problem is unclear.
        - Tie proposals to business outcomes where possible.
        - Leave room for maintenance, iteration, and support.
    """,
    "docs/company/MeetingNotes.md": """
        # Meeting Notes

        This document is the index for important company meetings.

        ## Format

        - Date:
        - Participants:
        - Context:
        - Decisions:
        - Action Items:
        - Follow-Up Date:

        Keep notes short, decision-oriented, and linked to relevant documents.
    """,
    "docs/company/DecisionLog.md": """
        # Decision Log

        The decision log records meaningful company choices so future Sevora team members can understand why the company moved in a certain direction.

        ## Format

        - Date:
        - Decision:
        - Context:
        - Options Considered:
        - Rationale:
        - Expected Review Date:

        ## Initial Decisions

        - Sevora is positioned as an AI Product Studio, not an agency.
        - This repository is the company operating system, not a product repository.
    """,
    "docs/company/CompanyGoals.md": """
        # Company Goals

        ## Current Priorities

        - Establish SevoraOS v1 as the foundation for strategy and operations.
        - Define the first public Sevora website and brand narrative.
        - Select the most promising initial product and solution opportunities.
        - Build a repeatable discovery and proposal process.

        ## Goal Standard

        Goals should be specific, time-bound, measurable where possible, and connected to company strategy.
    """,
    "branding/README.md": """
        # Branding

        This folder defines how Sevora looks, sounds, and feels.

        Brand is not decoration. It is the company's public memory: the repeated signals that tell customers what Sevora believes, how it works, and why it can be trusted.
    """,
    "branding/LogoIdeas.md": """
        # Logo Ideas

        Sevora's logo should feel intelligent, precise, and enduring.

        ## Directions

        - A clean wordmark with subtle custom geometry.
        - A symbol based on signal, systems, or structured intelligence.
        - A mark that works in monochrome before relying on color.

        Avoid trendy AI motifs that may age quickly.
    """,
    "branding/BrandVoice.md": """
        # Brand Voice

        Sevora's voice should be clear, calm, ambitious, and technically credible.

        ## Voice Traits

        - Direct without being cold.
        - Ambitious without exaggeration.
        - Practical about AI.
        - Confident because the thinking is clear.

        ## Avoid

        - Hype-heavy AI language.
        - Generic innovation slogans.
        - Overly casual startup slang.
    """,
    "branding/Typography.md": """
        # Typography

        Sevora typography should support clarity, trust, and modern product taste.

        ## Direction

        - Use a strong sans-serif for interface and marketing text.
        - Prioritize readability across dashboards, documents, and websites.
        - Keep hierarchy disciplined: fewer sizes, stronger spacing, better contrast.

        Candidate type systems can be evaluated during website design.
    """,
    "branding/ColorSystem.md": """
        # Color System

        Sevora's color system should feel modern, technical, and trustworthy without becoming generic.

        ## Early Direction

        - Neutral foundation for seriousness and readability.
        - One strong primary accent for recognition.
        - Supporting colors for product status, data, and industry categories.

        Color decisions should be tested in real interfaces, not only brand boards.
    """,
    "branding/DesignPrinciples.md": """
        # Design Principles

        - Make complex systems feel understandable.
        - Prefer useful density over decorative emptiness.
        - Use motion and visuals only when they clarify.
        - Design for repeated use, not just first impressions.
        - Keep interfaces calm under operational pressure.
    """,
    "website/README.md": """
        # Website

        This folder plans Sevora's public website.

        The website should explain Sevora clearly, signal product taste, attract serious customers, and create confidence that Sevora can build practical AI systems.
    """,
    "website/Sitemap.md": """
        # Sitemap

        ## Initial Website

        - Home
        - Products
        - Solutions
        - Research
        - About
        - Contact

        ## Future Pages

        - Case Studies
        - Careers
        - Product Detail Pages
        - Industry Landing Pages
        - SevoraOS Narrative
    """,
    "website/WebsiteVision.md": """
        # Website Vision

        Sevora's website should feel like the public surface of a serious AI product company.

        It should avoid agency cliches and focus on what Sevora builds: products, systems, research, and practical AI solutions for business.
    """,
    "website/WebsiteRoadmap.md": """
        # Website Roadmap

        ## v1

        Launch a concise website with positioning, product previews, solution categories, and a contact path.

        ## v2

        Add case studies, research notes, stronger product pages, and lead capture.

        ## v3

        Add demos, interactive product experiences, customer proof, and hiring pages.
    """,
    "website/ContentPlan.md": """
        # Content Plan

        ## Core Themes

        - Practical AI adoption for businesses.
        - Product thinking in AI systems.
        - Industry-specific automation opportunities.
        - Lessons from building Sevora products.

        Content should build trust by being specific, useful, and grounded in real problems.
    """,
    "sales/README.md": """
        # Sales

        This folder defines how Sevora earns trust, qualifies opportunities, and converts business problems into valuable work.

        Sales at Sevora should feel consultative, precise, and outcome-oriented.
    """,
    "sales/SalesProcess.md": """
        # Sales Process

        1. Identify a business problem with meaningful operational value.
        2. Run discovery to understand workflow, data, users, constraints, and success metrics.
        3. Recommend a focused solution path.
        4. Present a clear proposal with scope, timeline, pricing, and assumptions.
        5. Deliver in visible milestones.
        6. Review outcomes and identify productization opportunities.
    """,
    "sales/DiscoveryQuestions.md": """
        # Discovery Questions

        - What workflow currently consumes the most time or creates the most errors?
        - Where does information get lost between people, tools, or teams?
        - What would improve if this process became 50 percent faster?
        - What data or systems are involved?
        - Who will use the solution every week?
        - What risks would make this project unsuccessful?
        - How will we measure value after launch?
    """,
    "sales/ProposalTemplate.md": """
        # Proposal Template

        ## Context

        Summarize the customer's current situation and business problem.

        ## Recommended Solution

        Describe the proposed system in plain language.

        ## Scope

        List what is included and what is excluded.

        ## Timeline

        Define phases, milestones, and review points.

        ## Investment

        State pricing, payment schedule, and support terms.

        ## Success Metrics

        Define how value will be measured.
    """,
    "sales/PricingIdeas.md": """
        # Pricing Ideas

        ## Starting Models

        - Paid discovery sprint.
        - Fixed-price prototype.
        - Production build package.
        - Monthly optimization and support retainer.
        - SaaS subscription for productized systems.

        Pricing should reflect business value, implementation complexity, support needs, and strategic learning value for Sevora.
    """,
    "operations/README.md": """
        # Operations

        This folder documents how Sevora runs as a company.

        Good operations reduce confusion, preserve energy, and make high-quality work repeatable.
    """,
    "operations/HiringRoadmap.md": """
        # Hiring Roadmap

        ## Early Roles

        - Product-minded engineer.
        - AI systems engineer.
        - Designer with strong interface taste.
        - Growth and partnerships lead.

        Hiring should follow proven demand. Each role should remove a real constraint in product quality, delivery speed, or distribution.
    """,
    "operations/StandardOperatingProcedures.md": """
        # Standard Operating Procedures

        SOPs should document repeated work that must be done consistently.

        ## Candidate SOPs

        - Client discovery.
        - Product validation.
        - Proposal creation.
        - Launch checklist.
        - Research review.
        - Decision logging.

        Keep SOPs short enough to use and specific enough to matter.
    """,
    "operations/KnowledgeBase.md": """
        # Knowledge Base

        The knowledge base is for reusable company learning: technical notes, customer insights, market lessons, and operating patterns.

        Entries should be linked to products, solutions, or decisions whenever possible.
    """,
    "research/README.md": """
        # Research

        Research helps Sevora choose better problems, build sharper products, and avoid shallow assumptions.

        This folder collects AI trends, industry analysis, competitor notes, and future product ideas.
    """,
    "research/AI.md": """
        # AI Research

        Track useful developments in models, agents, retrieval, automation, evaluation, safety, and deployment.

        Research should answer: what changed, why it matters, what Sevora should test, and what should be ignored for now.
    """,
    "research/Industries.md": """
        # Industry Research

        Use this document to compare industries by pain intensity, budget, urgency, data availability, and productization potential.

        Strong opportunities usually combine repeated workflows, measurable value, accessible buyers, and poor existing software.
    """,
    "research/FutureIdeas.md": """
        # Future Ideas

        Capture promising ideas without letting them distract current execution.

        ## Idea Format

        - Problem:
        - User:
        - Existing Alternatives:
        - Why Now:
        - Prototype:
        - Validation Signal:
    """,
    "research/Competitors.md": """
        # Competitors

        Competitor research should clarify positioning, not create imitation.

        ## Track

        - Product category.
        - Target customer.
        - Pricing model.
        - Strengths.
        - Weaknesses.
        - Opportunity for Sevora.
    """,
    "assets/README.md": """
        # Assets

        This folder stores visual and presentation material for Sevora.

        Assets should be organized by usage so brand files, product mockups, website images, icons, and pitch materials remain easy to find as the company grows.
    """,
    "assets/logos/README.md": """
        # Logos

        Store Sevora logo files, wordmarks, symbols, and approved export variants here.

        Keep source files separate from production exports when the logo system becomes more mature.
    """,
    "assets/mockups/README.md": """
        # Mockups

        Store product mockups, website previews, interface explorations, and concept visuals here.

        Mockups should be named clearly by product, date, and purpose when possible.
    """,
    "assets/presentations/README.md": """
        # Presentations

        Store pitch decks, company presentations, sales decks, and investor-facing materials here.

        Final exports and editable source files should be easy to distinguish.
    """,
    "assets/icons/README.md": """
        # Icons

        Store icon sets, app icons, product marks, and interface icon exports here.

        Icons should follow the brand and design principles defined in ../../branding/DesignPrinciples.md.
    """,
    "assets/images/README.md": """
        # Images

        Store website imagery, product visuals, team photos, and approved marketing images here.

        Prefer specific, useful visuals over generic stock-style imagery.
    """,}


def clean(value: str) -> str:
    return dedent(value).strip() + "\n"


def write_file(relative_path: str, content: str) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(clean(content), encoding="utf-8")


def product_readme(name: str, purpose: str) -> str:
    return f"""
        # {name}

        ## Purpose

        {purpose}

        ## Current Status

        Concept stage. The product direction should be refined through research, prototypes, and customer discovery before major investment.

        ## Future Vision

        {name} should become a focused, high-quality product with a clear user, measurable value, and a path to recurring revenue.

        ## Links

        - Related strategy: ../../docs/strategy/BusinessModel.md
        - Company principles: ../../docs/foundations/CompanyPrinciples.md
    """


def solution_readme(industry: str, problems: str, solutions: str) -> str:
    return f"""
        # {industry}

        ## Industry

        {industry} organizations operate in environments where service quality, speed, cost control, and trust matter.

        ## Common Problems

        Common problems include {problems}.

        ## Potential AI Solutions

        Potential Sevora solutions include {solutions}.

        ## Future Demo Product

        Create a focused demo that solves one visible workflow for one specific user. The demo should show business value in minutes and be easy to explain to an operator in the industry.
    """


def ensure_directories() -> None:
    directories = [
        "docs/foundations",
        "docs/strategy",
        "docs/company",
        "website",
        "products",
        "solutions",
        "branding",
        "sales",
        "operations",
        "research",
        "assets/logos",
        "assets/mockups",
        "assets/presentations",
        "assets/icons",
        "assets/images",
        "scripts",
    ]
    for directory in directories:
        (ROOT / directory).mkdir(parents=True, exist_ok=True)


def main() -> None:
    ensure_directories()
    for relative_path, content in FILES.items():
        write_file(relative_path, content)
    for name, purpose in PRODUCTS.items():
        write_file(f"products/{name}/README.md", product_readme(name, purpose))
    for folder, (industry, problems, solutions) in SOLUTIONS.items():
        write_file(f"solutions/{folder}/README.md", solution_readme(industry, problems, solutions))
    print("SevoraOS v1 structure is ready.")


if __name__ == "__main__":
    main()


