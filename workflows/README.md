# Production n8n Workflow Templates (Sanitized)

This directory contains battle-tested, sanitized workflow exports from live enterprise operations. All private API keys, webhook URLs, and client credentials have been replaced with standard environment placeholders (`CREDENTIAL_ID_PLACEHOLDER`, `CRM_MASTER_SPREADSHEET_ID`).

---

## Available Workflows

### 1. `01-interlocked-sales-reply-watcher.n8n.json`
* **Architecture:** Multi-touch outbound cadence interlocked with a real-time (60s loop) Gmail reply poller.
* **Key Mechanisms:**
  * Auto-identifies inbound prospect replies and immediately updates CRM status to `REPLIED`.
  * Instantly halts active outreach cadences to eliminate embarrassing double-messaging.
  * Auto-detects hard and soft email bounces to protect domain sender reputation.
  * Dispatches real-time Slack alerts to `#leads-and-alerts` for immediate human sales takeover.
* **Case Study Reference:** [02 - Interlocked Outbound Sales Automation](../case-studies/02-interlocked-sales-automation.md)

### 2. `02-document-intelligence-hitl.n8n.json`
* **Architecture:** Multi-modal document ingestion pipeline with confidence-based human-in-the-loop (HITL) routing.
* **Key Mechanisms:**
  * Ingests unstructured invoice data (vendor, invoice #, subtotal, tax, total).
  * Executes a deterministic mathematical balance check (`subtotal + tax == total`).
  * Scores extraction confidence against a 0.90 quality threshold.
  * High confidence (`>= 0.90`): Auto-commits directly to the master general ledger.
  * Low confidence or math anomaly (`< 0.90`): Quarantines the record and dispatches an interactive Slack triage alert for human review.
* **Case Study Reference:** [03 - Intelligent Document Parsing & HITL Review](../case-studies/03-intelligent-document-parsing-hitl.md)

### 3. `03-speed-to-lead-inbound-qualifier.n8n.json`
* **Architecture:** Sub-3-second real-time webhook ingestion, validation, and multi-channel notification engine.
* **Key Mechanisms:**
  * Ingests raw inbound leads from webhooks/forms instantly (<3s latency).
  * Validates and cleans phone numbers (E.164 format) and business email domains.
  * Qualifies high-intent budget signals before routing.
  * Dispatches high-priority Slack notifications to `#leads-and-alerts` and SMS trigger to sales reps.
* **Case Study Reference:** [05 - Real-Time Speed-to-Lead Qualification](../case-studies/05-realtime-speed-to-lead-qualification.md)

---

## How to Import into n8n

1. Open your self-hosted n8n instance.
2. In the top-right menu, select **Workflows** > **Import from File...**
3. Select either `.n8n.json` file.
4. Bind your local credentials (Google OAuth2, Slack API token) in the designated node fields.
5. Activate the workflow.
