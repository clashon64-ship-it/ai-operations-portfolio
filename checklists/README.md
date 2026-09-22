# Production Architecture & Audit Checklists

This directory contains battle-tested, forensic engineering checklists from Penn Enterprises LLC.

---

## Available Checklists

### 1. `7_point_production_hardening_checklist.pdf`
* **Focus:** Next.js + Supabase Backend Optimization & Connection Hardening.
* **Target Audience:** Engineering Leads, Full-Stack Developers, and CTOs scaling Supabase in production.
* **The 7 Forensic Checkpoints:**
  1. **Supavisor Port 6543 Enforcement:** Transaction vs Session mode connection pooling under serverless environments.
  2. **Row-Level Security (RLS) Subquery Optimization:** Wrapping `(select auth.uid())` to prevent row-by-row auth re-execution.
  3. **Index Optimization (B-Tree & Partial GIN):** Eliminating sequential scans on high-cardinality multi-tenant tables.
  4. **Connection Pool Budgeting:** Calculating `max_connections` allocation across Vercel serverless lambdas.
  5. **Direct Postgres Port 5432 Isolation:** Blocking direct pool exhaustion from long-lived migration scripts.
  6. **Client-Side SWR / TanStack Cache Invalidation:** Minimizing repetitive round-trip database queries.
  7. **Automated Health Check & Deadlock Alarms:** Sub-second latency telemetry alerting via Slack/Prometheus.

---

## Direct Download
- [Download 7-Point Checklist (PDF)](7_point_production_hardening_checklist.pdf)
