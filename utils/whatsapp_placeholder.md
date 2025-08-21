# WhatsApp Integration (Placeholder)

In production, connect via WhatsApp Business API using providers like Twilio or 360dialog.

- Set up a webhook server (e.g., Flask) to receive messages.
- Verify the sender (member phone) and map to Membership ID.
- Forward intents (status, fees, events, certificate) to the same backend functions used by Streamlit.
- Return text or document URLs (e.g., generated certificate PDF).