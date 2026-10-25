# Notes 2026-10-25

## News
None (weekend)

## Deep dive: Better work, not better workers? Autor et al.'s three-month patent-lawyer RCT on whether AI builds or erodes expertise

Main source: David Autor, Tanya Rodchenko, Josh Martin, Zanna Iscenko, Scott Strand, David Pearl, Melissa Ferere, "Does AI Assistance Enhance or Erode Expertise? Evidence from a Three-Month Field Experiment in Patent Drafting", NBER Working Paper 35720 (September 2026, revised October 2026). Full text read (MIT version dated October 7, 2026).
- NBER page: https://www.nber.org/papers/w35720
- Full text: https://economics.mit.edu/sites/default/files/2026-10/Does%20AI%20Assistance%20Enhance%20or%20Erode%20Expertise%20Evidence%20from%20a%20Three-Month%20Field%20Experiment%20in%20Patent%20Drafting.pdf
- Pre-registration: https://www.socialscienceregistry.org/trials/15823

### Why this topic, why now
- The paper is in this week's feeds (The Decoder, 24 October) and is the first RCT that measures skill acquisition separately from AI-assisted output, for practising professionals working in their own field over months. That's a step up from the call-centre episode (2026-10-11), which looked at productivity and hiring. This one asks what happens to the human capital of the people who stay.
- It ties together three of Lucas's interests. Economics of AI: human capital, apprenticeship, the junior pipeline. Research methods: how to measure skill when a tool is in the loop, and LLM raters versus expert raters. His own agent design: if his role is to be the "acceptor" of agent output (TRACE episode, 2026-10-20), his own judgment is the thing that must not erode.
- Sunday slot: AI for research / economics of AI.

### Outline (each point builds on the last)

1. **The tension and why it's hard to measure.** Expertise in law, medicine and consulting is built by learning-by-doing under supervision. AI could speed that up by giving good examples and on-the-spot feedback, or it could stunt it when juniors hand off the very tasks that build judgment. Measuring this needs three things: sustained use, a skill measure that is separate from AI-assisted output, and experimental control over access. The authors say no previous study had all three in a high-stakes professional setting. Mechanism to stress: AI is "easy to operate but hard to evaluate", so the judgment needed to check its output is exactly what learning-by-doing builds. [primary] (https://economics.mit.edu/sites/default/files/2026-10/Does%20AI%20Assistance%20Enhance%20or%20Erode%20Expertise%20Evidence%20from%20a%20Three-Month%20Field%20Experiment%20in%20Patent%20Drafting.pdf)

2. **The design: assisted output versus unassisted judgment.** 133 patent lawyers at 11 US IP firms (all with drafting relationships with Google), randomised 2:1 within firm, stratified by experience. Three tasks: AI-assisted drafting at 10 days, a harder drafting task at 90 days, and at 90 days a redlining task done *without AI*, marking up an AI-generated patent draft. Redlining is the skill measure, because it draws on judgment rather than producing text. Blinded raters from an independent IP firm scored the work on five dimensions. The core idea: the same people are measured once with the tool and once without it. [primary]

3. **Result 1, output: AI levels the field.** Drafting quality rose by 0.34 SD at 10 days and 0.38 SD at 90 days. The gains were bigger for juniors (0.58 and 0.60 SD) than for seniors (0.22 and 0.30 SD). The gain comes from fewer poor drafts, not more excellent ones. With AI, juniors beat untreated seniors at 10 days. This is the familiar leveling pattern from Noy & Zhang, Brynjolfsson et al. and others. [primary]

4. **Result 2, judgment: the ordering flips.** On unassisted redlining, treated lawyers beat controls by 0.32 SD, and *all* of that comes from seniors (+0.45 SD). Juniors: −0.03 SD, no average gain. Junior scores bifurcated: 0.22 more poor scores, 0.42 fewer mediocre ones, and a 0.19 rise in good scores that is imprecisely estimated. Treated seniors' scores became *less* dispersed. Three months of AI drafting opened a junior–senior gap in unassisted judgment that does not exist among controls. The authors' reading: AI was "a springboard for some juniors and a cushion for others", and foundational expertise may be needed to turn AI-assisted practice into lasting skill. [primary]

5. **The likely mechanism: time on task and engagement.** Juniors saved more time (−18 minutes at 10 days against a junior control mean of about 124) but gained no unassisted skill. Seniors drafted better but were barely faster (−5 minutes). Juniors' satisfaction rose sharply (+1.48 SD at 90 days) and they believed their quality had improved. That belief held for assisted work, not for unassisted work. The authors point to Strömberg et al. (Chinese secondary students): AI adopters spent less time on homework, got higher homework scores and lower high-stakes exam scores, and students who kept their study time did fine. Other studies point the same way. Bastani et al.: a GPT Tutor that gives hints instead of answers removed the exam penalty. Shen & Tamkin: interaction patterns that keep people cognitively engaged preserved learning. The working hypothesis: whether you build skill depends on whether you stay engaged, and seniors know what to check. The authors say their experiment does not show *why* some juniors gained and others lost, and that testing time-on-task as the channel would require manipulating it directly. [primary for the paper; Bastani secondary; Shen & Tamkin primary]

6. **How much to trust this.** Small sample: 91 completed the redlining, and the junior subgroup has 50 rating-level observations. No baseline skill test (the partner firms refused it), so the skill interpretation rests on randomisation balance. The window is three months. The sample is sophisticated firms working for Google, the study was funded by Google, and the AI tool came from Google Labs. AI use during redlining couldn't be monitored. The authors ran a lot of robustness checks, but some results are fragile. They're useful to tell Lucas as a researcher, because they show how to stress-test a small RCT. See the facts list below.

### Facts and examples with sources

**Design and sample** (all from https://economics.mit.edu/sites/default/files/2026-10/Does%20AI%20Assistance%20Enhance%20or%20Erode%20Expertise%20Evidence%20from%20a%20Three-Month%20Field%20Experiment%20in%20Patent%20Drafting.pdf unless stated)
- Pre-registered in the AEA RCT Registry (AEARCTR-0015823) on May 21, 2025. [primary] (https://www.socialscienceregistry.org/trials/15823)
- Of 24 IP firms with regular, non-exclusive business with Google, 11 agreed to take part. One firm's two cohorts are analysed separately, giving 12 firm cohorts. [primary]
- Of 156 lawyers put forward by firms, 133 (85%) were randomised: 90 (68%) treatment, 43 (32%) control. The 2:1 ratio was a compromise between the researchers' preference for an even split and the firms' wish to give more lawyers access sooner. [primary]
- Participants were paid their contractual hourly rate for time spent on the experiment's tasks. [primary]
- Study period May 2025 to February 2026. Cohorts started between May and September 2025. [primary]
- The tool: an unreleased Google Labs writing assistant with prompt-based text modification, feedback from multiple AI "editorial personas" and rule-based checks for internal inconsistencies. A redlining feature was added in July 2025. It was never released as a standalone product; its features were folded into other Google AI products. [primary]
- Control lawyers had standard legal tools but no generative AI writing tools. [primary]
- Both arms got basic AI training. Treatment also got tool-specific training, including a patent-specific prompt library and "common pitfalls" material. [primary]
- Tasks: 10-day drafting (5–7 dependent claims plus a detailed description, ≤1,000 words, ≤2 hours). 90-day drafting (harder, up to 2,000 words). 90-day redlining of an AI-generated patent draft, where AI was not allowed. Invention details came from a hold-out set not used to train the model. [primary]
- Completion: 105 (79%) did the 10-day task, 98 the 90-day drafting, 91 the redlining (cumulative attrition 32%). No differential attrition by treatment: point estimates 0.04, −0.02 and −0.04, all p ≥ 0.56. [primary]
- Scoring: two blinded raters per task, drawn from a pool of six at a contracted IP firm. The rubric was developed with Google's in-house counsel and covers enforceability, technical accuracy, strategic ambiguity, completeness, and clarity. Inter-rater Pearson correlations: 0.59 (10-day drafting), 0.47 (90-day drafting), 0.55 (redlining). [primary]
- "Senior" means ≥7 years of experience, which the authors describe as industry convention on the advice of Google's in-house counsel. Randomisation was stratified on the within-firm median instead. [primary]

**Results: assisted drafting**
- Treatment effect 0.34 SD at 10 days (p = 0.03, preferred stacked spec; p = 0.05 in the subject-average spec) and 0.38 SD at 90 days (p = 0.01). [primary]
- Juniors +0.58 SD (p = 0.04) at 10 days and +0.60 SD (p = 0.02) at 90 days. Seniors +0.22 SD (p = 0.24) and +0.30 SD (p = 0.08). The junior–senior difference itself is not significant (one-sided p = 0.15 and 0.17). [primary]
- With AI, juniors outperformed untreated seniors at 10 days (p = 0.05). At 90 days, treated juniors' mean was 0.36 SD against 0.13 for untreated seniors. [primary]
- Share of bottom-quintile (poor) drafting scores fell by 0.19 (p < 0.01) at 10 days and by 0.11 (p = 0.12) at 90 days. AI significantly compressed variance on the 90-day drafting task (Levene p = 0.03). [primary]

**Results: unassisted redlining (the skill measure)**
- Treated vs control: +0.32 SD (p = 0.04). Seniors +0.45 SD (p = 0.02). Juniors −0.03 SD (p = 0.89). The senior effect is significantly larger than the junior effect (one-sided p = 0.04). [primary]
- Untreated juniors and seniors performed comparably on redlining; the point estimate slightly favoured juniors (not significant). [primary]
- Treated seniors beat controls on all five subscales, each significant at p ≤ 0.10. Juniors had negative, non-significant point estimates on two of five subscales. [primary]
- Junior distribution: poor-quintile share +0.22 (p = 0.04), mediocre −0.42 (p = 0.01), good +0.19 (p = 0.20), more dispersion (Levene 3.66, p = 0.06). Senior distribution: good +0.22 (p = 0.00), poor −0.14 (p = 0.07), less dispersion (Levene 7.74, p = 0.01). No significant change in top-quintile scores for either group. [primary]

**Time and perceptions (self-reported)**
- 10-day drafting: treated lawyers about 10 minutes faster (p = 0.05) against a control mean of 110 minutes. Juniors 18 minutes faster, seniors 5. At 90 days the estimates are 22 vs 5 minutes, neither significant. [primary]
- Redlining: no time savings for treated lawyers. Treated juniors spent 4 minutes longer than control juniors, treated seniors 1 minute longer. [primary]
- Perceived speed gains: 0.72 SD at 10 days and 1.14 SD at 90 days. Perceived quality gains were not significant overall, but juniors reported 0.95 SD at 10 days (p = 0.01). Satisfaction at 90 days: juniors +1.48 SD, seniors +0.28 SD. [primary]
- Spillover: treated lawyers became more likely to report regular work-related use of *other* gen-AI tools. The gap was 17.3 points in month three (p = 0.05) on a control base of 5.6%. Roughly four in five respondents reported no or only occasional work-related gen-AI use. [primary]

**Robustness, including the fragile parts**
- Permutation test (2,000 draws): full sample p = 0.05, seniors p = 0.02, juniors p = 0.93. [primary]
- Dropping one firm at a time: the full-sample redlining estimate ranges from 0.22 to 0.38 SD and the senior estimate from 0.33 to 0.55 SD. Dropping Firm 10 (six participants, all senior) cuts the full-sample effect to 0.22 SD, which is not significant. The senior effect stays at 0.33 SD (p = 0.08). [primary]
- Seniority thresholds from 3 to 11 years: the senior redlining effect is 0.38–0.46 SD, significant at 5% at every threshold. The junior effect is never significant. [primary]
- AI-use audit: NotebookLM (Gemini 3.0 Pro) plus a manual review flagged 15 of 91 redlining submissions for possible AI use, on tells such as full-paragraph rewrites, "strained praise", "delves" and change-logs instead of inline edits. Flags were about as common among controls (4 of 29) as among treated lawyers (11 of 62). Excluding flagged submissions drops the full-sample effect to 0.25 SD (p = 0.14, not significant). The senior effect is 0.39 SD (p = 0.06) and the junior effect −0.11 SD. [primary]
- LLM-as-rater (Gemini 2.5-flash with the same rubric): it reproduces the broad pattern but gives systematically larger gaps (e.g. 0.89 vs 0.45 SD in 90-day drafting). LLM–expert correlation is only r = 0.47, 0.19 and 0.14 across the three tasks. With pooled ratings, juniors and seniors get similar drafting boosts at 90 days, which is the one place the pattern changes. The authors treat the LLM as "a third, less reliable rater". [primary]
- Tie-in to the 2026-10-06 episode (validating LLM judges): rank-order agreement on aggregate effects can coexist with very low per-item correlation.
- On-the-job outcomes (68 participants) are underpowered (minimum detectable effect about 2.3 weeks) and show no significant effects. [primary]

**Limitations stated by the authors**
- Small sample, an even smaller junior subgroup, firms that aren't representative, no baseline skill assessment (partner firms rejected it), a three-month horizon, and unmonitored AI use during redlining. They propose baseline plus repeated unassisted assessments over a longer horizon. [primary]
- Funding: Google paid the direct costs. Autor was a Google Technology and Society Visiting Fellow, and the other six authors are at Google. [primary]

**Related evidence**
- Bastani et al. (PNAS 2025): nearly 1,000 high-school maths students in Turkey. GPT Base improved practice performance by 48% but lowered exam scores by 17% relative to control. GPT Tutor, which gives hints rather than answers and was built with teacher input, improved practice by 127% with exam scores about equal to control. [secondary] (https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education)
- Shen & Tamkin, "How AI Impacts Skill Formation" (Anthropic Fellows): 52 developers learning the Python Trio library, 26 per arm, GPT-4o assistant. The AI group scored 17% lower on the comprehension quiz (4.15 points on a 27-point scale, Cohen's d = 0.738, p = 0.010) with no significant speed gain. Of six interaction patterns, "AI delegation", "progressive reliance" and "iterative debugging" scored low (≤40%). "Generation-then-comprehension", "hybrid code-explanation" and "conceptual inquiry" scored high (≥65%). [primary] (https://arxiv.org/html/2601.20245v1)
- Other studies in the paper's literature review: Budzyń et al. (Lancet Gastroenterology & Hepatology 2025) found routine AI assistance associated with deterioration of endoscopists' unassisted skill. He et al. (2026) found novice radiologists trained with predictive AI later diagnosed more accurately on their own. Bednar et al. (2026) found law students exposed to AI outperformed controls once AI was removed. [primary, as summarised in the Autor et al. paper]
- EU angle: AI Act Article 4 (AI literacy) requires providers and deployers to take measures for a sufficient level of AI literacy among staff; it has applied since 2 February 2025. [secondary] (https://artificialintelligenceact.eu/article/4/)

### Practical takeaway Lucas could apply this week
1. **Measure "with tool" and "without tool" separately in his own work.** For a task he now does with Claude (coding an estimation, summarising a literature strand), do one small instance unaided each month and compare it with his earlier work. That is the paper's design in miniature. Its closing point is that you can only judge AI's effect on skill if the evaluation separates the software's contribution from the user's expertise.
2. **Build "tutor mode" into his skills.** Following Bastani's GPT Tutor and Shen & Tamkin's high-scoring patterns, give a Claude skill used for learning a new method (say a new econometric estimator) two modes. "Do" mode produces output. "Learn" mode asks him to predict the result first, explains the reasoning and only then shows code. A hook can even require a short written rationale before an agent's diff is accepted. That keeps the acceptor role (TRACE) a real check rather than a rubber stamp.
3. **Dutch business idea: an AI-literacy and skill-retention audit for professional-services firms.** Notaries, accountants, tax advisers and patent firms have an AI Act Article 4 literacy obligation and a junior pipeline to protect. The product: a small unassisted benchmark (redlining-style review of a flawed AI draft) at onboarding and every quarter, scored by blinded seniors, plus a dashboard that splits results by experience. Pitch it as an HR/quality tool, not a SaaS platform. The paper's own methods are the template: blinded double rating, a rubric, an LLM-use audit with tells.
4. **For his own research evals:** if he uses an LLM rater, check per-item correlation with expert ratings, not just whether aggregate treatment effects line up. In this paper, r = 0.14 on redlining still gave the same headline direction.

### Mia hooks
- "I noticed this with my own juniors on a RAG project. The ones who let Claude write the retrieval code shipped faster, but when the reranker broke on a Friday, only the seniors could debug it without the agent. Is that the 'cushion' effect?"
- "Here's what bugs me as an eval person: the LLM rater correlates 0.14 with the experts on redlining and still 'corroborates' the result. If you saw r = 0.14 between your judge and your humans, would you call that corroboration?"
- "If seniors gain judgment *because* they argue with the tool, should we design agents that leave a deliberate gap for the human, like a tutor that refuses to finish the last step? What does that cost in throughput?"

## Episode
- Title: Better Work, Not Better Workers: AI and the Junior Expertise Gap
- Summary: A three-month RCT with 133 patent lawyers finds AI lifts everyone's drafts, juniors most, but when the tool is taken away only seniors come out with better judgment, and junior skill splits into winners and strugglers. We go through the design, the fragile robustness checks and the mechanism (engagement and time on task), and turn it into tutor modes for Claude skills, with-and-without-tool self-checks, and a Dutch AI-literacy audit idea.
