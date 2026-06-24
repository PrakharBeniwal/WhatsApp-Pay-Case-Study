# PRD — The Closed-Loop Checkout
## WhatsApp Pay × Click-to-WhatsApp Ads (India)

| | |
|---|---|
| **Author** | [Your Name] — Product Management |
| **Status** | Draft v1.0 — for review |
| **Last updated** | June 2026 |
| **Initiative** | Big Bet #1 / Tier-1 RICE solution (score 98) from the WhatsApp Pay Rejuvenation Strategy |
| **Eng / Design / DS partners** | WhatsApp Commerce · Ads (CTWA) · Payments (NPCI/UPI) · Trust & Safety · Legal/Reg |
| **Companion artifact** | `WhatsApp_Pay_CTWA_Wireframes.pptx` (user flow + screen-by-screen UX) |

---

## 1. TL;DR

WhatsApp Pay holds **<1% of India's UPI market** despite WhatsApp's ~500M-user distribution. The root cause — established in the diagnosis phase of this case study — is not a product-quality problem; it is a **business-model problem**: under India's zero-MDR regime a UPI transaction earns Meta ~₹0, so the payment has near-zero LTV and Meta has rationally under-invested.

This PRD specs the one intervention that **changes the unit economics rather than working around them**: wire WhatsApp Pay in as the **default, in-chat checkout at the bottom of the Click-to-WhatsApp Ads (CTWA) funnel**, so the chain **ad → chat → catalog → pay → attribution** closes entirely inside WhatsApp. Every completed checkout becomes (a) a measured ad-conversion event that makes CTWA ads more effective and more valuable, and (b) commerce GMV that can carry an ad-take / commerce-take. That is what converts a ₹0 payment into a **positive-LTV** event for Meta — the precondition the diagnosis says was always missing.

The template is proven: WeChat monetizes a zero-MDR-style payment rail not on the transaction but on **commerce and ad take** (~0.6% mini-program commission on >RMB 2T GMV). The funnel is already here and India-led: **CTWA is a ~$1.5B ad business (2025, +80% YoY), India is its #1 market, and 15M+ businesses are on WhatsApp Business.**

---

## 2. Problem & strategic context

### 2.1 The diagnosis this feature answers

The case study's root-cause model ranked thirteen failure drivers and collapsed them to one binding constraint:

> **Zero-MDR → UPI earns ₹0 per transaction → WhatsApp Pay's LTV to Meta ≈ ₹0 → rational non-investment by Meta → no merchant density, no habit loop → <1% share.**

The natural experiment that confirmed it: NPCI removed the 30% market-share cap on Dec 31, 2024, and WhatsApp Pay's *entire* subsequent quarter of growth was **+17%** — proving the cap was never the binding constraint. Meta's *will to invest* was, and will-to-invest is a function of LTV.

### 2.2 Why the constraint is now breakable

When WhatsApp Pay launched, Meta had **no India monetization stack** to attach the payment to. That has changed:

- **CTWA is now Meta's fastest-growing ad product** — ~**$1.5B** revenue in 2025 (**+80% YoY**); CTWA spend **+82% YoY** (Q1'25→Q1'26); **India is the #1 CTWA market**; India cost-per-conversation ~**$0.95** (vs ~$5.20 US).
- A **first-party checkout signal** is the single most valuable thing a performance-ad platform can own. Today a CTWA advertiser's funnel goes dark at the moment of purchase (the sale happens off-platform, on a third-party UPI app or a website). WhatsApp Pay closing the loop hands Meta a **deterministic conversion event** to optimize and bid against.
- The commerce primitive exists to extend: in **Sep 2025** WhatsApp shipped an in-chat QR/UPI payment primitive in India; this PRD productizes it into a **catalog → cart → checkout** flow defaulted to WhatsApp Pay.

### 2.3 The reframe

> We are not asking "how do we get more people to use WhatsApp Pay for P2P?" We are asking **"how do we make a WhatsApp Pay transaction worth something to Meta?"** The answer is to make it the checkout for the ad business Meta already monetizes. Payments stops being a cost center and becomes the **measurement-and-conversion layer of CTWA.**

---

## 3. Goals, non-goals & success metrics

### 3.1 Goals

1. **Close the loop:** make ad → chat → catalog → pay → attribution complete inside WhatsApp, with WhatsApp Pay the **default** payment method at checkout.
2. **Generate LTV-to-Meta:** emit a first-party, deterministic **purchase-conversion event** per completed checkout that flows into Ads ranking/optimization and reporting.
3. **Grow the North Star:** convert CTWA ad-clickers into **Monthly Active P2M Payers (MAPP)** at the moment of purchase intent.
4. **Stand up commerce GMV** that can later carry a commerce-take / ad-take (the zero-MDR-proof monetization path).

### 3.2 North Star & metric tree

**North Star: Monthly Active P2M Payers (MAPP)** — baseline ~**0.5–1M** today against ~100M registered users. This feature is the highest-leverage MAPP input because it intercepts users at *demonstrated purchase intent* (they clicked a shopping ad), not cold.

| Layer | Metric | Definition |
|---|---|---|
| **North Star** | MAPP | Unique users completing ≥1 P2M payment in a trailing 28-day window |
| **Primary (feature)** | CTWA→Pay closed-loop conversion | % of CTWA-initiated conversations that complete an in-chat WhatsApp Pay checkout |
| **Primary (feature)** | Checkout completion rate | % of initiated checkouts that succeed (paid) via WhatsApp Pay |
| **Primary (Meta-side)** | Attributed-purchase rate | % of CTWA conversions with a first-party purchase event returned to Ads |
| **Input** | Checkout attach rate | % of CTWA conversations that reach a cart/checkout surface |
| **Input** | Pay default-selection rate | % of checkouts where WhatsApp Pay is left as the chosen method |
| **Input** | Incremental MAPP | New/reactivated P2M payers first transacting via a CTWA checkout |
| **Business** | Closed-loop GMV | ₹ value of goods transacted through in-chat checkout |
| **Business** | Ad-effectiveness lift | Change in advertiser ROAS / cost-per-purchase from first-party attribution |

### 3.3 Targets (illustrative, assumption-flagged)

> Targets are directional and assume the org-level funding decision (§7.1) is made. They are sized to be defensible, not precise.

| Metric | 6 mo (Pilot) | 12 mo (Expand) | 24 mo (Default) |
|---|---|---|---|
| Merchants live with in-chat checkout | ~500 | ~25,000 | 250,000+ |
| Checkout completion rate (WhatsApp Pay) | ≥30% | ≥45% | ≥55% |
| Pay default-selection rate | ≥70% | ≥80% | ≥85% |
| Incremental MAPP (cumulative) | +0.3M | +3M | +10M |
| Closed-loop GMV run-rate | seed | ₹X00 cr/mo | ₹X,000 cr/mo |
| Advertiser cost-per-purchase | measure | −10% vs off-platform | −20% vs off-platform |

### 3.4 Guardrail metrics (must-not-regress)

- **Checkout latency** (ad-tap → paid) p90 ≤ target; **payment success rate** ≥ NPCI/UPI parity.
- **Chat trust:** spam/block rate on CTWA business threads; user-reported scam rate on checkout.
- **No cannibalization of P2P trust:** WhatsApp Pay P2P success rate and NPS unchanged.
- **Advertiser quality:** merchant fulfilment / dispute / refund rate within thresholds.

### 3.5 Non-goals (explicit scope boundaries)

- **Not** a general e-commerce marketplace, storefront host, or logistics/fulfilment product.
- **Not** building consumer lending or insurance here (separate Big Bet #2; this feature *feeds* its data graph but does not depend on it).
- **Not** changing UPI economics or seeking MDR — monetization is via **ad-take / commerce-take**, not a transaction fee.
- **Not** a P2P/social-payments redesign; scope is **P2M commerce checkout** originating from CTWA.
- **Not** international in v1 — India-only (CTWA's #1 market, and where the zero-MDR thesis lives).

[[PAGEBREAK]]

## 4. Users & personas

### 4.1 The Shopper (consumer)
**"I clicked an ad for something I want; let me buy it without leaving the chat or fighting a checkout."**
- Tier 2/3-heavy, mobile-first, often new to formal e-commerce, high trust in WhatsApp as an interface.
- Pain today: ad → chat → then a hand-off to a clunky external link, a COD form, or a "pay to this UPI ID" message with manual amount entry. Drop-off is brutal.

### 4.2 The Merchant / Advertiser
**"I run CTWA ads because they're cheap and they work; I want the sale to close where the conversation happens, with money settled and tracked."**
- One of 15M+ WhatsApp Business accounts; SMB to mid-market; already paying Meta for CTWA.
- Pain today: manual payment collection, reconciliation, no clean conversion signal to optimize ad spend, leakage to third-party rails.

### 4.3 Internal stakeholder — the Ads (CTWA) team
**"Give me a deterministic, first-party purchase event and my ad ranking, optimization, and advertiser ROAS all improve."**
- This persona matters because **their** value capture (better ads) is what funds the payments investment. The PRD must emit the conversion signal in a form Ads can ingest.

---

## 5. User stories (JTBD)

**Shopper**
- As a shopper who tapped a CTWA ad, I can browse the merchant's catalog **in the chat** so I don't lose context.
- As a shopper ready to buy, I can check out with a **pre-filled cart, address, and WhatsApp Pay already selected**, so paying is one confident tap + UPI PIN.
- As a shopper, I get an **order confirmation and receipt as a chat message** I can return to, so I trust the purchase and can re-engage.

**Merchant**
- As a merchant, I can **attach my catalog to a CTWA ad** so the ad lands on a shoppable conversation.
- As a merchant, I **receive UPI settlement and a clean order record** without manual collection or reconciliation.
- As a merchant, I can **see which ad drove which sale** so I can scale what works.

**Ads team**
- As the Ads platform, I **receive a first-party purchase-conversion event** keyed to the originating ad/campaign so I can optimize delivery and report ROAS.

---

## 6. The solution

### 6.1 The closed loop (four stages)

```
   ┌─────────────────────────────────────────────────────────────┐
   │  (4) ATTRIBUTION                                             │
   │  first-party purchase event → Ads ranking + advertiser ROAS │
   └───────────────▲─────────────────────────────────────────────┘
                   │  feeds optimization (better, more valuable ads)
   (1) AD ─────────┼──────────► (2) CHAT ──────────► (3) PAY
   FB/IG CTWA ad   │            in-chat catalog       in-chat WhatsApp Pay
   "Shop on        │            + cart                checkout (DEFAULT)
    WhatsApp"      │                                  → UPI PIN → paid
                   └──────────────────────────────────────────┘
            the payment is what makes the ad measurable & monetizable
```

The strategic point sits on the return arrow: **the completed payment is the signal that makes the ad valuable.** Without stage (3) closing inside WhatsApp, stage (4) cannot fire with first-party certainty — which is exactly why the payment, today worth ₹0, becomes worth something.

### 6.2 Functional requirements

Priority: **P0** = required for pilot · **P1** = required for default rollout · **P2** = fast-follow.

#### A. Ad unit (CTWA entry)
| ID | Requirement | Pri |
|---|---|---|
| A1 | CTWA ad supports a "Shop on WhatsApp" objective that deep-links into a shoppable conversation, carrying campaign/ad/product context. | P0 |
| A2 | Deep-link payload preserves **attribution identifiers** end-to-end (ad → chat → checkout → purchase event). | P0 |
| A3 | Ad creative can reference a specific catalog/product so the chat opens on that item. | P1 |

#### B. Chat & catalog
| ID | Requirement | Pri |
|---|---|---|
| B1 | On open, business sends a structured greeting + **catalog/product card** (image, title, price, CTA). | P0 |
| B2 | Shopper can add items to an **in-chat cart**; cart state persists in the thread. | P0 |
| B3 | Catalog supports variants (size/qty), stock state, and price; merchant-managed via Business tools. | P1 |
| B4 | Business-AI / agentic assistant can answer questions and assemble the cart (rides Meta's business-AI rollout). | P2 |

#### C. Checkout (the core change)
| ID | Requirement | Pri |
|---|---|---|
| C1 | A **checkout bottom-sheet** summarizes items, delivery address, and total. | P0 |
| C2 | **WhatsApp Pay is pre-selected as the default payment method.** Other UPI apps remain available but are not the default. | P0 |
| C3 | Address is **pre-filled** from saved profile; editable; minimal typing. | P1 |
| C4 | Checkout shows merchant identity, refund/return terms, and a **safety/trust badge**. | P0 |
| C5 | Price integrity: amount is server-set from cart; never user-entered (anti-fraud). | P0 |

#### D. Payment (WhatsApp Pay / UPI)
| ID | Requirement | Pri |
|---|---|---|
| D1 | Tapping **Pay** invokes the NPCI UPI PIN flow **in-context**, returning to the chat on completion. | P0 |
| D2 | Settlement routes to the merchant's account; **order record** generated automatically. | P0 |
| D3 | Support **RuPay-credit-on-UPI** as an eligible instrument where available (the one MDR-bearing UPI flow → future commerce-take headroom). | P2 |
| D4 | Idempotent payment handling; safe retry on network failure; no double-charge. | P0 |

#### E. Post-purchase
| ID | Requirement | Pri |
|---|---|---|
| E1 | **Confirmation + receipt delivered as a chat message** (order ID, items, amount, merchant, track-order CTA). | P0 |
| E2 | Order/track surface for status updates; merchant can post shipment/updates into the thread. | P1 |
| E3 | Refund/dispute entry point from the order message. | P1 |

#### F. Attribution & measurement (the LTV layer)
| ID | Requirement | Pri |
|---|---|---|
| F1 | On successful payment, emit a **first-party purchase-conversion event** keyed to the originating CTWA ad/campaign. | P0 |
| F2 | Event flows to **Ads optimization** (bidding/ranking) and to **advertiser reporting** (ROAS, cost-per-purchase). | P0 |
| F3 | Funnel instrumentation across all stages (impression → tap → conversation → catalog view → add-to-cart → checkout → paid). | P0 |
| F4 | Privacy-compliant data handling per NPCI/RBI rules on payment data; consent + purpose limitation respected. | P0 |

[[PAGEBREAK]]

## 7. Dependencies

### 7.1 The critical dependency — the funding decision
The diagnosis names this explicitly: **Meta must choose to fund WhatsApp Pay as the default CTWA checkout.** This is an org-level commitment, not an engineering task, and it is *the exact thing that has been missing.* Everything below is downstream of it. **This PRD is, in effect, the artifact that makes the funding case investable** by showing the LTV mechanism concretely.

### 7.2 Cross-team & external
| Dependency | Owner | Note |
|---|---|---|
| Catalog + cart + in-chat UPI checkout productization | WhatsApp Commerce | Extends the Sep-2025 QR/UPI primitive |
| First-party conversion event ingestion | Ads / CTWA | The value-capture path; must accept and optimize on the event |
| UPI PIN / settlement rails | Payments + NPCI | PSP/bank partners; UPI PIN UX; settlement |
| Business-AI / agentic commerce | Messaging AI | Accelerant for cart assembly (P2) |
| Self-preferencing review | Legal / Regulatory | Defaulting Meta's own rail inside an ad funnel (see §8) |
| Merchant onboarding & enablement | Business Platform / GTM | Catalog setup, KYC, settlement onboarding |

---

## 8. Risks & mitigations (the honest "why it might not")

A core principle of this case study is that **every proposed fix carries its failure case.** This feature's are real:

| Risk | Severity | Mitigation |
|---|---|---|
| **Self-preferencing / antitrust.** Defaulting Meta's own payment rail inside Meta's ad funnel may draw regulatory scrutiny (CCI, NPCI fairness norms). | High | Keep other UPI apps selectable (default ≠ exclusive); document consumer-benefit (lower friction, fraud protection); proactive reg engagement. |
| **Zero-MDR still means the payment itself earns ₹0.** Value is *indirect* (ad-take/attribution). If Ads doesn't actually bid up CTWA on the new signal, the LTV thesis doesn't convert to revenue. | High | Instrument the ad-effectiveness lift (§3.2) as a **gating metric**; run a holdout to prove incremental ROAS; commerce-take on GMV as a second revenue path. |
| **Merchant enablement friction.** Catalogs, KYC, settlement setup are work; SMBs may not adopt. | Med | Templated catalog import; AI-assisted setup; default-on for advertisers already running CTWA; white-glove for anchor merchants. |
| **Checkout friction / UPI PIN drop-off.** A clunky PIN hand-off kills completion. | Med | In-context PIN return-to-chat; pre-filled cart/address; aggressive p90 latency budget; relentless funnel optimization. |
| **Trust & fraud.** Shoppable ads + payments invite scam merchants and farming. | High | Server-set amounts (C5); merchant KYC; trust badges; dispute/refund flow; T&S monitoring on CTWA threads. |
| **Habit fragility.** Commerce checkout may not generalize to daily P2P habit (the "spikes then recedes" risk from the diagnosis). | Med | Accept scope: this bet wins *commerce*, not daily P2P. Sequenced with merchant-lending (Bet #2) to deepen the relationship. |

---

## 9. Rollout plan

| Phase | Timeline | Scope | Exit gate |
|---|---|---|---|
| **0 — Foundation** | 0–3 mo | Productize catalog→cart→checkout on the Sep-2025 UPI primitive; build the first-party conversion event; instrument the funnel. | Internal E2E closed loop works; event lands in Ads reporting. |
| **1 — Pilot** | 3–6 mo | ~500 invited merchants (incl. 3–5 anchor merchants); WhatsApp Pay default at checkout; measure completion + attribution lift. | ≥30% checkout completion; demonstrated ROAS lift on a holdout. |
| **2 — Expand** | 6–18 mo | Open to all CTWA advertisers in India; AI-assisted cart; RuPay-credit-on-UPI eligibility. | ≥45% completion; +3M incremental MAPP; advertiser cost-per-purchase −10%. |
| **3 — Default** | 18–24 mo | In-chat WhatsApp Pay checkout is the **standard** CTWA endpoint; commerce-take productized. | ≥55% completion; +10M MAPP; measurable ad-spend lift; commerce-take live. |

**GTM note:** acquisition cost for merchants is near-zero — *running a CTWA ad becomes the act of adopting the checkout.* That is the structural advantage this feature has over a field-force merchant build (the expensive path the diagnosis warns against).

---

## 10. Open questions

1. **Commerce-take rate & timing** — when do we introduce a take on closed-loop GMV, and at what rate, without suppressing merchant adoption? (WeChat's ~0.6% is the reference point.)
2. **Attribution windows & model** — click vs view; window length; how to handle multi-session purchases.
3. **Default-selection policy** — exact treatment of competing UPI apps to stay defensible on self-preferencing while preserving the default's conversion benefit.
4. **RuPay-credit-on-UPI** — prioritize sooner as the one MDR-bearing instrument (direct revenue) vs. complexity cost.
5. **Anchor-merchant selection** — which 3–5 high-volume merchants (e.g., a grocery anchor ≈ 40–160M txns/mo) seed the volume proof fastest?

---

## 11. Appendix — evidence & benchmarks

| Claim | Figure | Source basis |
|---|---|---|
| CTWA scale & growth | ~$1.5B revenue 2025, +80% YoY; spend +82% YoY Q1'25→Q1'26 | Storyboard18 / Spocket |
| India is CTWA's #1 market | ~$0.95 cost/conversation (vs ~$5.20 US) | Searchlab / industry |
| WhatsApp Business base | 15M+ businesses in India | Searchlab |
| Closed-loop monetization template | WeChat ~0.6% mini-program commission on >RMB 2T GMV ≈ ~RMB 12B/yr; 900M WeChat Pay users | CIW/Tencent; TechBuzzChina |
| The binding constraint | Cap removed Dec 31 2024 → only +17% growth (natural experiment) | Phase-2 diagnosis |
| North Star baseline | MAPP ~0.5–1M of ~100M registered | Phase-3 strategy |

**Glossary:** **CTWA** = Click-to-WhatsApp Ads · **MDR** = Merchant Discount Rate (₹0 under India UPI) · **MAPP** = Monthly Active P2M Payers · **P2M** = person-to-merchant · **LTV** = lifetime value · **ROAS** = return on ad spend · **CLOU** = credit-line-on-UPI.

---

*This PRD specs Tier-1 solution #15 / Big Bet #1 from the WhatsApp Pay India Rejuvenation Strategy. It is a portfolio artifact demonstrating the path from root-cause diagnosis → prioritized strategy → executable product spec. Companion UX: `WhatsApp_Pay_CTWA_Wireframes.pptx`.*
