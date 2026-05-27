# UX Research Report

**Problem Statement:** Design an onboarding flow for a fintech mobile app

**Generated:** 2026-05-27 23:24

---

## Stage 1 — UX Laws & Principles

### Fitts' Law
**Definition:** The time to acquire a target is a function of the distance to and size of the target.

**Application:** During fintech onboarding, primary CTAs like 'Continue', 'Verify Identity', and 'Link Bank Account' must be large, thumb-reachable buttons placed at the bottom of the screen within the natural thumb arc. Small touch targets for agreeing to Terms & Conditions or tapping KYC document upload icons will cause friction and drop-off at critical conversion points. Error correction actions like 'Resend OTP' or 'Re-enter PIN' must also be adequately sized to reduce frustration during high-stakes moments.

**Design Implication:** Make all primary onboarding action buttons at least 48x48dp, full-width where possible, and anchored to the bottom safe zone; never place critical actions like 'Agree & Continue' in the top half of the screen on mobile.

**Priority:** `high`

### Hick's Law
**Definition:** The time to make a decision increases with the number and complexity of choices available.

**Application:** At the account setup stage, presenting users with multiple account types, investment options, or KYC verification methods simultaneously will paralyze new users who are already anxious about sharing financial data. Asking users to choose between linking a bank via net banking, UPI, IFSC, or card number all at once creates decision fatigue at a trust-critical moment. Each onboarding screen should present one primary path forward, with alternatives tucked behind a secondary option.

**Design Implication:** Limit each onboarding step to a single decision or input task; default to the most commonly used verification method (e.g., mobile OTP) and surface alternatives like email verification only as a fallback link.

**Priority:** `high`

### Miller's Law
**Definition:** The average person can hold approximately 7 (plus or minus 2) items in working memory at one time.

**Application:** Onboarding steps that require users to recall or enter long account numbers, IFSC codes, or policy reference numbers exceed working memory limits, especially when users must switch between apps to copy this data. Progress indicators showing more than 7 onboarding stages will feel overwhelming and reduce perceived completion likelihood. Grouping required documents into logical clusters — 'Identity', 'Address', 'Financial' — respects chunking principles and reduces cognitive overload.

**Design Implication:** Chunk the onboarding flow into no more than 5 named stages shown in a progress bar, and pre-fill or auto-detect data (e.g., bank name from IFSC prefix) to minimize manual recall burdens.

**Priority:** `high`

### Jakob's Law
**Definition:** Users spend most of their time on other apps and expect your app to work the same way those apps do.

**Application:** Fintech users arrive with mental models from apps like Paytm, Groww, or Revolut, expecting OTP-based phone verification as the first onboarding step, not email registration. Deviating from the pattern of phone number → OTP → profile setup will cause confusion and abandonment. UI patterns like swipe-to-confirm for transactions, face ID prompts after signup, and card-style account summaries are established conventions users expect to carry over.

**Design Implication:** Mirror the onboarding sequence convention of phone verification → OTP → minimal profile → KYC, and use standard platform components (native date pickers, OS-level biometric prompts) rather than custom-built equivalents.

**Priority:** `high`

### Law of Proximity
**Definition:** Objects that are near each other are perceived as a group and assumed to be related.

**Application:** On the KYC document upload screen, placing the upload button, file size limit, and accepted formats far apart will make users uncertain about what the button applies to. Form fields for 'First Name' and 'Last Name' must be visually grouped and separated clearly from 'Date of Birth' to signal they belong to different data categories. Security reassurance microcopy like 'Your data is encrypted' must be placed immediately adjacent to the field requesting PAN or SSN — not at the bottom of the screen where spatial distance breaks the association.

**Design Implication:** Place all contextual help text, format hints, and security badges within 8px of the specific input field they relate to, not in a generic footer, so users process them as part of that field's interaction.

**Priority:** `medium`

### Aesthetic-Usability Effect
**Definition:** Users perceive aesthetically pleasing designs as more usable and trustworthy, even when functionality is identical.

**Application:** In fintech onboarding, where users are asked to submit sensitive documents and link bank accounts, a polished visual design directly increases perceived trustworthiness and willingness to share data. Inconsistent typography, misaligned form fields, or generic stock icons during the KYC screens signal low legitimacy and trigger abandonment. A clean, minimal aesthetic with consistent brand color usage on verification screens reduces the subconscious alarm users feel when sharing financial credentials.

**Design Implication:** Invest in pixel-perfect visual design for the KYC and bank-linking screens specifically — these are the highest trust-risk moments — using consistent iconography, generous whitespace, and brand-aligned color to signal institutional credibility.

**Priority:** `high`

### Peak-End Rule
**Definition:** People judge an experience based on how they felt at its most intense moment and at its end, not the average of every step.

**Application:** The 'peak' in fintech onboarding is likely the KYC document submission or bank account linking — high anxiety, high effort moments that must be actively softened with reassurance, progress feedback, and clear next-step communication. The 'end' is the moment the account is activated or the first transaction is enabled, which must be celebrated with a visually rewarding success state to encode a positive final memory. A generic 'Setup Complete' text screen as the endpoint will result in a weak emotional closing that dampens overall onboarding recall.

**Design Implication:** Design a dedicated, animated success screen at onboarding completion — showing the user's name, account status, and a clear first action to take — and add reassurance copy at the document upload step to transform the anxiety peak into a moment of confident progress.

**Priority:** `high`

### Doherty Threshold
**Definition:** Productivity and engagement soar when a computer and its users interact at a pace of under 400ms, eliminating any need for users to wait.

**Application:** During onboarding, if OTP verification, bank account validation, or KYC document processing takes more than 400ms without visual feedback, users interpret the silence as an error and either tap again or abandon. Bank name auto-population from a typed IFSC code or PAN must resolve near-instantly to feel like intelligent assistance rather than a slow lookup. Loading states during ID verification that exceed a few seconds must include animated progress indicators with estimated time to prevent the user from assuming the app has crashed.

**Design Implication:** Instrument all onboarding API calls to target sub-400ms response times, and for calls that inherently take longer (e.g., KYC processing), implement skeleton screens or step-by-step processing animations with copy like 'Verifying your identity — this takes about 10 seconds' to maintain perceived responsiveness.

**Priority:** `medium`

### Postel's Law
**Definition:** Be liberal in what you accept from users, and conservative in what you output.

**Application:** During onboarding form entry, if a user types their phone number with spaces, dashes, or a country code prefix, the app should silently normalize it rather than throwing a validation error that breaks flow. For name fields, accepting mixed case, extra spaces, or non-Latin characters without error prevents drop-off from users whose legal names don't fit ASCII-only input assumptions. Dates of birth entered in any regional format (DD/MM/YYYY or MM-DD-YYYY) should be auto-interpreted, not rejected with a format error.

**Design Implication:** Build input normalization logic for all onboarding fields — phone numbers, names, dates, account numbers — so the app strips formatting noise silently before validation, and only surface an error when the core data is genuinely missing or invalid.

**Priority:** `medium`

### Progressive Disclosure
**Definition:** Present only the information necessary for the current task, revealing additional detail only as users need it.

**Application:** Asking a new user to complete full KYC, set notification preferences, choose a spending category, and set a PIN all before seeing the app's core value will cause drop-off. The onboarding flow should unlock only the minimum required data to activate the account — phone, name, basic KYC — and defer secondary configurations like nominee details, investment risk profiling, and referral codes to post-activation contextual prompts. Advanced options like 'Use a different verification method' or 'Enter details manually' should be hidden behind a low-prominence secondary link, not presented upfront.

**Design Implication:** Scope the onboarding critical path to the minimum fields legally required for account activation, and schedule all secondary personalisation (spending limits, notification preferences, linked accounts) as in-app prompts triggered by first use of the relevant feature.

**Priority:** `high`

### Tesler's Law (Conservation of Complexity)
**Definition:** Every application has an inherent amount of complexity that cannot be removed — it can only be shifted between the system and the user.

**Application:** Fintech onboarding carries unavoidable regulatory complexity: KYC laws require identity verification, AML rules require source-of-funds disclosures, and data privacy laws require consent capture. The design team cannot eliminate this complexity, but they can absorb it into the system — pre-populating fields via DigiLocker or Open Banking APIs, auto-detecting document types from uploaded images, and generating consent summaries in plain language. If the system fails to absorb this complexity, it cascades onto the user as manual data entry, legal jargon, and multi-step verification sequences.

**Design Implication:** Prioritize backend integrations with identity verification APIs (e.g., DigiLocker, Aadhaar eKYC, Plaid) that allow the system to absorb the data-collection burden, so the user experience can be reduced to confirmation steps rather than manual entry steps.

**Priority:** `high`

### Von Restorff Effect
**Definition:** When multiple similar objects are present, the one that differs from the rest is most likely to be remembered and noticed.

**Application:** On a screen listing onboarding steps or required documents, users will only notice and remember items that are visually differentiated — making the 'currently active' step or a mandatory-but-overlooked document like 'Proof of Address' visually distinct is critical to preventing incomplete submissions. A highlighted security badge or trust seal placed uniquely on the bank-linking screen — different from every other screen — will anchor user attention on the trust signal at the highest-anxiety moment. Using the same button style and color for both 'Skip' and 'Continue' on the same screen is a direct Von Restorff failure that will cause users to accidentally skip required steps.

**Design Implication:** Apply a single high-contrast accent color exclusively to the primary CTA on each onboarding screen, ensure 'Skip' or 'Do Later' options are always rendered in a lower-contrast secondary style, and visually differentiate the bank-linking screen with a distinct trust-focused layout to make it memorable as a safe interaction.

**Priority:** `medium`

---

## Stage 2 — Proto Personas

### Marcus Chen — Software Engineer
**Age:** 28 | **Tech Comfort:** 5/5

**Primary Goal:** Get through onboarding as fast as possible and start exploring investment features without unnecessary friction

> *"I've onboarded into like six finance apps this year. If yours makes me tap through twelve screens before I see a single number, I'm already forming a bad opinion."*

**Frustrations:**
- Multi-step onboarding flows that ask for information he'll never use — he wants to skip optional steps
- Apps that don't support biometric login or autofill from the start, forcing manual data entry
- Being shown tutorials for things he already understands intuitively from using similar fintech apps

**Motivations:**
- Reaching the actual dashboard quickly so he can evaluate whether the app is worth keeping
- Trusting that the app is secure based on how polished and deliberate the setup process feels
- Seeing advanced features like portfolio analytics teased during onboarding so he knows the depth is there

**Relevant UX Laws:**
- **Jakob's Law**: Marcus has deep experience with competing fintech apps and will expect onboarding conventions like progressive account setup and biometric prompts to match what he already knows — deviating from these patterns creates unnecessary cognitive load for him.
- **Progressive Disclosure**: Marcus is frustrated by upfront information overload; revealing advanced settings and optional configurations only after core setup respects his goal of reaching the dashboard fast while keeping power features accessible when he wants them.
- **Doherty Threshold**: Any loading screen or verification delay above 400ms during account creation will feel broken to Marcus, who expects near-instant feedback — slow transitions will signal poor engineering quality and reduce his trust in the app.

### Diane Kowalski — High School Art Teacher
**Age:** 43 | **Tech Comfort:** 3/5

**Primary Goal:** Set up a savings account and understand what the app can do for her retirement planning without feeling overwhelmed

> *"I'm not bad with money, I just don't speak banker. If the app makes me feel stupid in the first five minutes, I'm deleting it and going back to my credit union's website."*

**Frustrations:**
- Financial jargon like 'APY', 'FDIC-insured', or 'routing number' appearing without any explanation during setup
- Being asked to make too many decisions at once — like choosing account types — before she understands the difference
- Onboarding flows that look cluttered or untrustworthy, making her second-guess whether the app is legitimate

**Motivations:**
- Feeling confident that her money is safe and that the app is backed by a real institution
- Getting a clear sense of progress through setup so she knows how close she is to being done
- Having the app feel welcoming and non-judgmental about her current savings situation

**Relevant UX Laws:**
- **Hick's Law**: Diane is vulnerable to decision paralysis during onboarding — presenting too many account options or configuration choices simultaneously will slow her down and increase drop-off risk, making it critical to limit choices per screen to one or two clear options.
- **Aesthetic-Usability Effect**: Diane consciously uses visual polish as a trust signal for financial apps — a clean, calm design will make her perceive the onboarding as more intuitive and the app as more legitimate, even before she has evaluated any features.
- **Peak-End Rule**: Diane will judge the entire onboarding experience based on its most emotionally impactful moment and its final screen — a reassuring confirmation message with a warm welcome and clear next step will anchor her memory of setup as positive, regardless of minor friction along the way.

### Roy Tanner — Retired Postal Worker
**Age:** 67 | **Tech Comfort:** 2/5

**Primary Goal:** Successfully link his existing bank account to track his pension deposits and understand where his money is going each month

> *"My daughter set up my first smartphone. I can manage fine now, but when an app rushes me or hides things in small print, I just don't trust it with my bank account."*

**Frustrations:**
- Small tap targets and dense form fields that are hard to interact with accurately on his phone
- Being timed out of sessions mid-onboarding when he steps away to find his bank details from paper statements
- Verification steps like SMS codes that expire quickly, requiring him to restart the whole process

**Motivations:**
- Feeling like someone designed this app with him in mind, not just for young people
- Having a family member — his daughter — recommend the app and be able to help him set it up remotely
- Knowing exactly what he agreed to before submitting any personal or financial information

**Relevant UX Laws:**
- **Fitts' Law**: Roy's reduced fine motor precision on a touchscreen means that small or closely spaced tap targets — like inline form action buttons or tiny checkbox labels — will produce frequent errors, making generously sized, well-spaced interactive elements essential throughout his onboarding path.
- **Miller's Law**: Roy can comfortably hold only a small number of items in working memory at once, so chunking the onboarding into clearly labeled phases of no more than three to four steps per section will prevent cognitive overload and help him track where he is in the process.
- **Tesler's Law (Conservation of Complexity)**: The inherent complexity of KYC verification and bank linking cannot be eliminated — but the app must absorb as much of that complexity as possible through smart defaults, document scanning, and pre-filled fields so Roy is never asked to manually transfer information he cannot easily locate.

---

## Stage 3 — Critical Design Thinking

### Empathize

**Key Questions:**
- When Roy Tanner steps away mid-onboarding to find his paper bank statement, what happens to his session — and how does that moment of abandonment feel to him?
- When Diane Kowalski encounters the term 'APY' or is asked to choose between account types on screen two, what emotional response does that trigger before she has any context?
- When Marcus Chen hits a mandatory field asking for information he considers irrelevant — like a physical mailing address before he's seen a single investment feature — how quickly does his tolerance expire?

**Activities:**
- Conduct a contextual inquiry session where Roy Tanner attempts to link his bank account using only his paper statements as reference, observed in his home environment — recording every tap error, pause, and moment of session timeout anxiety
- Run a think-aloud protocol with Diane Kowalski on a competitor fintech onboarding flow (e.g. Acorns or Betterment), asking her to narrate confusion at every jargon term or decision fork — cataloguing the specific words and UI moments that cause her to hesitate or want to quit
- Diary study over 5 days with Marcus Chen installing 3 fintech apps back-to-back, logging time-to-first-feature, number of screens before value, and explicit moments where he considered abandoning — with annotations on what specifically broke his flow

**Insights:** Roy Tanner's core emotional state during onboarding is one of precarious trust — he is willing to engage but a single timeout or form error threatens to permanently break his confidence in the product. His frustration with small tap targets and dense fields is not merely a usability complaint; it represents a fear of making irreversible mistakes with his financial data. Diane Kowalski enters onboarding with genuine curiosity about retirement planning but that curiosity collapses the moment she encounters unexplained jargon or is forced to make consequential account-type decisions without scaffolded understanding — her frustration is rooted in feeling intellectually excluded. Marcus Chen's frustration is the inverse: he is not excluded, he is over-included in steps designed for less experienced users, and every unnecessary screen reads to him as a product team that does not respect his time or technical capability. All three personas share an unmet need for control and legibility, but the definition of those terms is radically different for each of them.

### Define

**Key Questions:**
- What is the single most dangerous assumption baked into a linear, one-size-fits-all onboarding flow — the assumption that all three personas need the same information in the same order?
- How do we write a POV statement that captures Diane Kowalski's need without defaulting to the patronising solution of 'just simplify everything' — which would alienate Marcus Chen?
- Where is the line between progressive disclosure (which helps Roy and Diane) and excessive gating (which frustrates Marcus) — and can a single onboarding architecture serve both?

**Activities:**
- POV statement workshop: facilitator presents the three persona cards and their frustrations side-by-side; team writes competing POV statements for each persona, then stress-tests them by asking 'does solving this POV actively harm another persona?' — mapping tensions explicitly
- Jobs-to-be-Done reframe exercise: for each persona, complete the sentence 'When I open this fintech app for the first time, I want to _____ so that I can feel _____' — then cluster the functional, emotional, and social jobs to find shared underlying needs beneath the surface-level differences
- Define a 'minimum viable trust' framework: identify the irreducible set of data points the product legally and functionally requires at onboarding versus what is being collected for analytics or future features — used to challenge every mandatory field against Roy's and Marcus's frustrations

**Insights:** The defining tension in this problem is not between simplicity and power — it is between legibility and velocity. Diane Kowalski needs time, context, and plain language to build enough understanding to trust the product with her retirement savings; Roy Tanner needs large, forgiving interaction targets and a session model that accommodates his real-world behaviour of stepping away; Marcus Chen needs the product to get out of his way and trust that he already knows what he's doing. A single POV cannot serve all three without a branching or adaptive architecture. The most precise POV for this sprint is: Diane Kowalski, a high school art teacher planning for retirement, needs onboarding that teaches while it collects — because encountering financial jargon or forced account-type decisions before she has context causes her to feel intellectually excluded from her own financial future, making her likely to abandon before she reaches the features that would genuinely help her.

### Ideate

**Key Questions:**
- What if onboarding did not begin with data collection at all — what if it began with demonstrating value, and only asked for information at the moment that information unlocked a specific feature the user had just expressed interest in?
- How might we design a session persistence model so radical that Roy Tanner could start onboarding on Monday, leave his phone on the kitchen counter, and resume without penalty on Wednesday?
- What is the most incremental change — a single screen modification — that would most immediately reduce Diane Kowalski's jargon-induced anxiety without requiring a full architecture rebuild?

**Activities:**
- Worst possible idea warm-up: team generates the most hostile onboarding flow imaginable for Roy Tanner — 47 mandatory steps, 6-point font, 90-second timeout, no autofill — then inverts each element to generate genuine design ideas that directly address his stated frustrations
- Crazy 8s sketch sprint (8 minutes, 8 frames per participant) focused on the single screen where Diane Kowalski must choose an account type — each sketch must include a mechanism that gives her enough context to choose confidently without adding more than one additional tap or read
- Assumption reversal: take the core assumption 'onboarding must be completed before the user accesses the app' and reverse it to 'the user accesses the app first and onboarding completes itself in the background over the first 7 days as the user takes natural actions'

**Insights:** Three divergent ideas emerged as the most generative. The radical idea is a Value-First Deferred Onboarding model: Marcus Chen, Diane Kowalski, and Roy Tanner all enter the app with a single biometric or email step, immediately see a read-only personalised dashboard populated with illustrative data, and are only asked for real information at the moment a specific action requires it — linking a bank account surfaces only when Roy taps 'track my deposits', and account-type selection surfaces for Diane only after a 60-second interactive explainer she triggers by choice. The incremental idea is a Contextual Glossary Tooltip system: every piece of jargon in Diane's onboarding flow (APY, FDIC, routing number) is underlined in a distinct colour and expands inline to a plain-English two-sentence explanation without navigating away from the current step — zero additional screens, zero friction for Marcus who will never tap them. The reframe idea is a Persistent Session Envelope for Roy: the app treats onboarding as a multi-day asynchronous object — storing partial state to the device with no timeout penalty, sending a gentle push notification after 24 hours of inactivity reading 'Welcome back, Roy — you were right in the middle of linking your bank account. Your progress is saved.' These three ideas can coexist in a single architecture.

### Prototype

**Key Questions:**
- What is the single core assumption that, if wrong, would invalidate the Value-First Deferred Onboarding concept — and what is the cheapest possible artefact that tests only that assumption?
- Can a paper prototype with handwritten tooltip cards adequately simulate the Contextual Glossary Tooltip experience for Diane Kowalski, or does the interaction fidelity need to be higher to surface her real behaviour?
- How do we prototype the Persistent Session Envelope for Roy Tanner without building any backend — and can a Wizard of Oz technique (a researcher manually 'resuming' his session) produce valid signal?

**Activities:**
- Build a 7-screen paper prototype of the Value-First Deferred Onboarding flow using printed phone-frame templates and hand-drawn UI — screen 1 is a single large biometric button, screens 2–4 are a read-only illustrative dashboard, screens 5–7 show the progressive unlocking of real data entry triggered by user-initiated actions; no digital tools used, total build time under 3 hours
- Create a Figma clickthrough prototype (low fidelity, greyscale, no visual polish) of the account-type selection screen for Diane, with two variants: Variant A shows account types as a list with no explanation, Variant B shows the same list where each account type has a one-tap inline explainer with a plain-English summary and a 'which one is right for me?' quiz of two questions — prototype is shareable via link with no installation required
- Simulate Roy Tanner's session persistence scenario using a Wizard of Oz method: a researcher pre-loads a partially completed onboarding state on a test device, Roy begins the session, 'steps away' for 15 minutes (leaves the room), returns to find a push notification on the lock screen reading 'Your progress is saved — tap to continue where you left off' — the researcher has manually preserved the state; no code written

**Insights:** The lowest-fidelity prototype that tests the most critical assumption is the 7-screen paper prototype of Value-First Deferred Onboarding. The core assumption it tests is that users — specifically Marcus Chen and Diane Kowalski — will find more value in seeing a demonstrative dashboard before providing personal data than they will feel anxiety about the absence of a traditional 'secure setup first' flow. If Marcus does not engage with the illustrative dashboard and immediately asks 'where do I put my real account details', the deferred model fails for him. If Diane feels uncertain or unprotected by skipping upfront verification, the model fails for her. Both failure modes are detectable in a paper prototype session without a single line of code. For Roy, the Wizard of Oz session persistence test is the minimum viable artefact — it requires no backend, no notification infrastructure, and no polished UI, yet it directly tests whether the emotional experience of returning to a saved session reduces his anxiety and restores his willingness to continue.

### Test

**Key Questions:**
- When Marcus Chen encounters the illustrative dashboard in the Value-First prototype, does he interpret it as a respectful preview of value or as a deceptive delay before real setup — and how quickly does that interpretation form?
- Does Diane Kowalski's comprehension of the difference between a savings account and an investment account meaningfully improve after interacting with Variant B's inline explainer — and does that comprehension translate into confident selection or continued hesitation?
- When Roy Tanner returns after a 15-minute absence and sees the 'Your progress is saved' notification, does his body language and verbalisation indicate relief and renewed confidence — or does he distrust the saved state and want to start over anyway?

**Activities:**
- Moderated usability test with Diane Kowalski: facilitator presents both Figma variants back-to-back in counterbalanced order; Diane completes a think-aloud protocol, and the facilitator records: time-to-selection on the account-type screen, number of taps on inline explainers, confidence rating (1–5 Likert) after selection, and unprompted verbalisation of jargon terms — session is 45 minutes, recorded with consent
- Unmoderated speed test with Marcus Chen: he is given the paper prototype link (photographed and uploaded to Marvel or InVision) and a single instruction — 'get to the investment features as fast as possible'; facilitator records time-to-first-investment-screen, number of screens skipped, and asks one post-task question: 'At any point did you feel the app was wasting your time? If yes, at which screen?' — session is under 15 minutes with no facilitator present
- Wizard of Oz session-persistence test with Roy Tanner: conducted in a home setting with a researcher present but silent; Roy begins onboarding on a test device, is asked to 'go find your bank details' (researcher hands him a prop paper statement in another room), returns after 15 minutes; researcher records: whether Roy notices the notification unprompted, latency before he taps it, first words he speaks, and whether he successfully resumes without restarting — success is defined as task completion within 5 minutes of return without requesting help

**Insights:** Testing must be conducted with all three personas because the proposed solutions make divergent bets on each of them and a failure mode for one persona may be invisible if only one persona is tested. The critical success metric for Marcus Chen is time-to-first-investment-feature — if the Value-First dashboard adds more than 45 seconds to that journey compared to a traditional flow, the deferred model needs a hard 'skip to setup' escape hatch designed specifically for his persona. For Diane Kowalski, the success metric is not speed but confident comprehension — she should be able to explain, in her own words, the difference between the two account types after seeing Variant B, without referencing the explainer text verbatim; if she cannot, the explainer content has not achieved plain-language transfer. For Roy Tanner, success is binary and behavioural: does he resume the saved session without abandoning, and does he complete bank account linking within the same session after returning? Any result where Roy restarts from the beginning or asks 'did I lose everything?' is a failure state requiring immediate design intervention in the session persistence notification copy and visual design.

---

## Stage 4 — Research Synthesis

### Affinity Clusters

**Speed & Friction Tolerance**
- From Marcus Chen: He wants to skip optional steps and get to investment features as fast as possible, indicating a strong preference for progressive disclosure over front-loaded data collection.
- From Marcus Chen: He is frustrated when apps do not support biometric login or autofill from the start, showing that power users expect zero-friction authentication from day one.
- From UX Laws: Hick's Law requires limiting each onboarding step to a single decision or input task, with the most common verification method defaulted and alternatives offered only as fallback.
- From Design Thinking Ideate phase: A Value-First Deferred Onboarding concept emerged as the most generative radical idea, suggesting users should experience app value before being required to complete full registration.
*Experienced users actively resist onboarding friction and respond best when the flow defaults intelligently, defers optional steps, and surfaces value before demanding full commitment.*

**Trust, Legibility & Visual Confidence**
- From Diane Kowalski: Financial jargon like APY, FDIC-insured, or routing number appearing without explanation causes anxiety and distrust during setup.
- From Diane Kowalski: Cluttered or untrustworthy-looking screens make her second-guess the app's legitimacy, linking visual design quality directly to perceived security.
- From UX Laws: Law of Proximity requires contextual help text, format hints, and security badges to be placed within 8px of the specific input field they relate to, not in a generic footer.
- From Design Thinking Define phase: The defining tension in this problem is not between simplicity and power but between legibility and trust.
*Users interpret visual clarity and contextually placed explanations as signals of legitimacy, meaning design quality and inline guidance are not aesthetic choices but trust infrastructure.*

**Accessibility & Physical Usability**
- From Roy Tanner: Small tap targets and dense form fields are hard to interact with accurately, making physical accessibility a functional barrier to completion.
- From Roy Tanner: Session timeouts mid-onboarding when he steps away to find paper bank statements cause him to restart the entire process, creating a critical drop-off risk.
- From Roy Tanner: SMS codes that expire quickly and force a full restart compound the trust erosion for users who need more time to gather information.
- From UX Laws: Fitts' Law mandates all primary action buttons be at least 48x48dp, full-width, and anchored to the bottom safe zone to support accurate tapping on mobile.
*Older or less dexterous users face compounding failure loops when tap targets are too small and time-sensitive verification steps penalise the natural pace of real-world information gathering.*

**Cognitive Load & Decision Architecture**
- From Diane Kowalski: Being asked to choose account types before understanding the differences makes her feel overwhelmed, confirming that decision overload early in the flow damages confidence.
- From Marcus Chen: He resents being shown tutorials for things he already understands, revealing that one-size-fits-all onboarding education creates friction for experienced fintech users.
- From UX Laws: Miller's Law recommends chunking the flow into no more than five named stages shown in a progress bar, and using auto-detection like IFSC prefix lookup to reduce recall load.
- From UX Laws: Jakob's Law supports mirroring the industry-standard sequence of phone verification, OTP, minimal profile, and KYC, using native platform components instead of custom ones.
*Cognitive overload manifests differently across experience levels, requiring the flow to sequence decisions in order of familiarity, chunk steps visibly, and lean on platform conventions to reduce mental effort for all users.*

### How Might We Opportunities

- How Might We design a tiered onboarding flow that lets power users skip optional steps while surfacing progressive guidance only for users who signal they need it
- How Might We replace all financial jargon at the point of input with plain-language inline tooltips that appear within 8px of the relevant field without cluttering the screen
- How Might We extend session persistence and OTP validity windows so users who need to retrieve physical documents are not penalised with forced restarts
- How Might We apply Value-First Deferred Onboarding to let users explore core app features before completing KYC, reducing the perceived cost of starting the flow
- How Might We use auto-detection, native platform components, and smart defaults to reduce the number of manual inputs required across every onboarding stage

### Critical Insights

**Onboarding completion is less a function of flow length than of whether each step respects the user's real-world context, particularly their pace, physical environment, and prior fintech experience.**
Evidence: Roy Tanner's frustrations with session timeouts mid-flow while retrieving paper statements and expiring OTPs directly contradict a design assumption that users complete onboarding in a single uninterrupted sitting. Marcus Chen's demand for biometric autofill and skip options confirms the opposite failure mode: forcing capable users through steps designed for the slowest-paced user erodes engagement at the top of the funnel.

**Trust in a fintech onboarding flow is constructed at the component level, not the brand level, meaning every unexplained input field and every piece of jargon is an independent trust-destruction event.**
Evidence: Diane Kowalski explicitly links cluttered screens and unexplained financial terms like APY and routing number to second-guessing the app's legitimacy. The Law of Proximity finding reinforces this by specifying that security badges and help text must be within 8px of the relevant field, not relegated to footers, because users process them as part of that specific field's trustworthiness, not as a global reassurance.

**The standard industry onboarding sequence provides a shared mental model that reduces cognitive load, but it only succeeds when each stage is presented as a single decision and rendered with native platform components that users already know how to operate.**
Evidence: Jakob's Law evidence from the UX Laws corpus confirms that mirroring the phone verification, OTP, minimal profile, KYC sequence leverages existing user expectations from comparable fintech apps. Hick's Law compounds this by showing that presenting multiple decisions per screen undermines the benefit of familiar sequencing, a pattern directly reflected in Diane Kowalski's frustration at being asked to choose account types before she understands the differences.

---

## Stage 5 — User Journey Map

**Persona:** Marcus Chen

### Awareness & Discovery 😊
**Emotion Score:** 1/2
**Thoughts:** Looks promising — the feature set is exactly what I want. Let me just hope the onboarding isn't a 20-step nightmare like the last one I tried.

**Touchpoints:** Twitter/X tech finance thread, App Store listing, App Store reviews and ratings
**Pain Points:**
- App Store screenshots don't clearly show whether advanced investment features are accessible early
- Reviews mention a lengthy verification process but don't specify whether it can be deferred
**Opportunities:**
- How Might We apply Value-First Deferred Onboarding to let users explore core app features before completing KYC, reducing the perceived cost of starting the flow

### Download & Initial Launch 😐
**Emotion Score:** 0/2
**Thoughts:** Good — it asked for Face ID right away using the native iOS prompt. That's a green flag. Let's see how bad the signup actually is.

**Touchpoints:** App Store download, App splash screen, Initial permission prompts (biometrics, notifications)
**Pain Points:**
- Branding animation on the splash screen feels like wasted time before he can interact
- Uncertainty about whether he can explore the app before committing to a full sign-up
**Opportunities:**
- How Might We apply Value-First Deferred Onboarding to let users explore core app features before completing KYC, reducing the perceived cost of starting the flow
- How Might We use auto-detection, native platform components, and smart defaults to reduce the number of manual inputs required across every onboarding stage

### Account Creation & Identity Verification 😊
**Emotion Score:** 1/2
**Thoughts:** The Apple Sign-In auto-filled everything — that saved me two minutes easily. But now it wants my government ID already? At least there's a 'do this later' option.

**Touchpoints:** Sign-up screen, Email/phone input field, OTP verification screen, KYC document upload prompt
**Pain Points:**
- KYC prompt appearing before any value has been demonstrated feels premature
- No clear explanation of what features are locked versus accessible without completing KYC
**Opportunities:**
- How Might We use auto-detection, native platform components, and smart defaults to reduce the number of manual inputs required across every onboarding stage
- How Might We apply Value-First Deferred Onboarding to let users explore core app features before completing KYC, reducing the perceived cost of starting the flow
- How Might We extend session persistence and OTP validity windows so users who need to retrieve physical documents are not penalised with forced restarts

### Onboarding Flow & Profile Setup 😊
**Emotion Score:** 2/2
**Thoughts:** Finally — a flow that doesn't treat me like I've never used a phone before. Skipping those optional steps felt genuinely respectful of my time.

**Touchpoints:** Investor profile questionnaire, Risk tolerance screen, Optional preferences screens, Progress indicator
**Pain Points:**
- Risk tolerance questions still use industry jargon like 'volatility tolerance' without inline clarification
- Progress indicator resets unexpectedly after skipping steps, causing brief confusion about completion state
**Opportunities:**
- How Might We design a tiered onboarding flow that lets power users skip optional steps while surfacing progressive guidance only for users who signal they need it
- How Might We replace all financial jargon at the point of input with plain-language inline tooltips that appear within 8px of the relevant field without cluttering the screen

### First Use & Feature Exploration 😊
**Emotion Score:** 2/2
**Thoughts:** This is what I came for — the data is clean, the charts are responsive, and I haven't been interrupted by a single tutorial popup since I dismissed the first one.

**Touchpoints:** Home dashboard, Investment discovery screen, Stock/ETF detail pages, Simulated portfolio tool
**Pain Points:**
- Some premium analytics features are gated behind KYC completion with no preview or teaser available
- No persistent shortcut to resume KYC when he naturally decides he's ready
**Opportunities:**
- How Might We apply Value-First Deferred Onboarding to let users explore core app features before completing KYC, reducing the perceived cost of starting the flow
- How Might We design a tiered onboarding flow that lets power users skip optional steps while surfacing progressive guidance only for users who signal they need it

### KYC Completion (Deferred Return) 😊
**Emotion Score:** 2/2
**Thoughts:** It remembered where I stopped and the OCR pulled my details straight from the passport photo — I barely had to type anything. This is how it should always work.

**Touchpoints:** In-app KYC resume prompt, Document upload screen, Camera capture for ID, Selfie liveness check, Confirmation screen
**Pain Points:**
- Liveness check fails on first attempt due to lighting, with an error message that isn't specific enough to be actionable
- Provisional approval state is unclear — he's unsure which features are now unlocked versus pending full review
**Opportunities:**
- How Might We extend session persistence and OTP validity windows so users who need to retrieve physical documents are not penalised with forced restarts
- How Might We use auto-detection, native platform components, and smart defaults to reduce the number of manual inputs required across every onboarding stage

### Regular Use & Advocacy 😊
**Emotion Score:** 2/2
**Thoughts:** I actually recommended this to someone — that's rare. The onboarding respected my intelligence and the core product delivered on the promise.

**Touchpoints:** Daily app open via Face ID, Push notifications for portfolio events, Referral prompt, App Store review prompt
**Pain Points:**
- Referral flow requires the referred friend to complete full onboarding before Marcus receives credit, making the incentive feel distant
- Some advanced features introduced post-KYC have no contextual guidance, assuming discovery will happen organically
**Opportunities:**
- How Might We design a tiered onboarding flow that lets power users skip optional steps while surfacing progressive guidance only for users who signal they need it

**Overall Arc:** Marcus begins cautiously optimistic, spikes in satisfaction when the onboarding respects his time and technical fluency, experiences a brief dip at premature KYC gates, then recovers to strong advocacy once the deferred verification flow proves seamless and the core product delivers real value.

---

## Stage 7 — Design System Components

### Design Tokens
**Color Roles:** 
**Type Scale:** 
**Spacing:**  base unit

---
