/* ============================================================================
   GENESYS PRICING — SINGLE SOURCE OF TRUTH
   Every figure rendered on the Pricing tab comes from this file and nowhere
   else. When the revised ladder is signed off, change this file only.

   Source: Genesys HMIS Subscription & Pricing Proposal (client document).
   All figures in Nigerian Naira. The proposal states figures are indicative,
   shown as ranges pending final scoping; a firm quote follows facility sizing.
   ========================================================================== */
window.GENESYS_PRICING = {
  currency: "\u20A6",
  note: "Indicative, pending final scoping. A firm quote follows once seat count, module mix and facility size are confirmed. Annual billing carries an indicative 15% discount against the monthly rate.",
  billingModel: "Per active named user, billed monthly or annually.",

  tiers: [
    {
      id: "lite",
      name: "GeneSys Lite",
      forWho: "Small clinics and primary care",
      setup: { display: "\u20A61,500,000", amortised: null,
               includes: "Remote setup, core data templates, basic user training." },
      recurring: { display: "\u20A680,000 \u2013 200,000", unit: "per month",
                   detail: "Includes up to 4 active staff accounts. Additional seats \u20A65,000 \u2013 10,000 per user / month." },
      seatModel: "Up to 4 active accounts included",
      supentry: "Email and chat support, 24-hour response window"
    },
    {
      id: "standard",
      name: "GeneSys Standard",
      forWho: "Secondary and mid-sized hospitals",
      setup: { display: "\u20A64,500,000", amortised: null,
               includes: "On-site training, process hand-holding, workflow mapping." },
      recurring: { display: "\u20A6250,000 \u2013 900,000", unit: "per month",
                   detail: "Banded by active seats, not charged per individual seat." },
      bands: [
        { band: "Starter", seats: "Up to 25 users",  price: "\u20A6250,000", unit: "per month" },
        { band: "Growth",  seats: "Up to 60 users",  price: "\u20A6500,000", unit: "per month" },
        { band: "Enterprise", seats: "Up to 120 users", price: "\u20A6900,000", unit: "per month" }
      ],
      seatModel: "Active-user banding, 25 / 60 / 120",
      supentry: "Email and chat support, 8-hour response window"
    },
    {
      id: "enterprise",
      name: "GeneSys Enterprise",
      forWho: "Tertiary hospitals and multi-location chains",
      setup: { display: "\u20A615,000,000", amortised: "12-month milestone billing available",
               includes: "Full process engineering, multi-location configuration, custom report builder." },
      recurring: { display: "\u20A61,500,000", unit: "per month",
                   detail: "Base platform fee. Includes unlimited seats, the custom report builder and multi-location management." },
      seatModel: "Unlimited seats included",
      supentry: "Priority phone support, dedicated account manager, 4-hour response window"
    },
    {
      id: "custom",
      name: "GeneSys Custom",
      forWho: "Bespoke and specialist requirements",
      setup: { display: "By negotiation", amortised: null,
               includes: "Scoped to requirement." },
      recurring: { display: "From \u20A61,500,000", unit: "per month",
                   detail: "Enterprise base plus customisation fees for requested work." },
      seatModel: "Unlimited seats, plus customisation",
      supentry: "24/7 support with a named team and an SLA-backed uptime target"
    }
  ],

  addons: [
    { name: "Additional seat (overage)", basis: "Per seat / month beyond the tier allotment", rate: "\u20A65,000 \u2013 10,000" },
    { name: "PACS / imaging module",     basis: "Flat monthly add-on", rate: "On application" },
    { name: "Cloud hosting",             basis: "Flat monthly add-on", rate: "On application" },
    { name: "Custom API / HL7-FHIR integration", basis: "One-time project fee", rate: "On application" },
    { name: "On-site training",          basis: "Flat fee per session", rate: "On application" },
    { name: "Priority support upgrade",  basis: "Flat monthly add-on", rate: "On application" }
  ],

  terms: [
    "Setup fee and recurring subscription are separate lines. A facility budgets capital and operating spend from different envelopes.",
    "Initial term of 12, 24 or 36 months, auto-renewing unless cancelled with 30 to 60 days' notice.",
    "Pricing is fixed for the initial term. Renewal pricing is reviewed and capped under the Master Services Agreement.",
    "The facility owns all patient data at all times. Export is available on request and guaranteed for a defined window after termination."
  ]
};
