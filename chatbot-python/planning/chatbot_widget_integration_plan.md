# Chatbot Widget Integration Plan

## 1. Overview
This document describes how to integrate the AI Education chatbot widget into the website, enable the chat button in the footer, and serve the widget assets via Vercel. It also clarifies the use of `environment.yml` for Python dependencies.

---

## 2. Serving the Chatbot Widget
- **Widget assets** (JS, CSS, SVG, etc.) should be placed in `chatbot/frontend/`.
- Vercel will be configured to serve all files in `chatbot/frontend/` as static assets at `/chatbot/frontend/`.
- This makes the widget portable and easy to embed on other sites by referencing the JS/CSS from this path.

---

## 3. Enabling the Footer Chat Button
- The current HTML files (including `index.html` and all files in `pages/`) have a placeholder button:
  ```html
  <button class="footer-chat-btn" disabled aria-label="Chat (coming soon)">...</button>
  ```
- To enable the chatbot:
  1. **Remove** the `disabled` attribute from the button.
  2. **Add** a script tag to load the chatbot widget JS from `/chatbot/frontend/chat-widget.js` (or the correct filename).
  3. The widget JS should attach an event listener to `.footer-chat-btn` to open the chat popup when clicked.

#### Example HTML Update
```html
<!-- In the <body> or before </body> -->
<script src="/chatbot/frontend/chat-widget.js"></script>
```

---

## 4. Chatbot Widget JS Responsibilities
- Render the chat popup/modal UI when the button is clicked.
- Communicate with the backend API at `/chatbot/api/chat` (and any future endpoints).
- Handle CORS (the backend will allow requests from `ai-course.arjunasoknair.com`).
- Optionally, support configuration for embedding on other domains in the future.

---

## 5. Python Dependencies: environment.yml vs requirements.txt
- You already have an `environment.yml` specifying all Python dependencies for local scripts (e.g., embedding generation, FAISS index creation).
- **This is sufficient** for local/offline use, especially if you use Conda or Mamba.
- A `requirements.txt` is only needed if you want to:
  - Support users who use `pip` instead of Conda.
  - Deploy Python scripts to an environment that requires `requirements.txt` (not needed for current Vercel Node.js deployment).
- **Recommendation:** Stick with `environment.yml` unless you have collaborators who require `pip`/`requirements.txt`.

---

## 6. Summary of Steps
1. Place all chatbot widget assets in `chatbot/frontend/`.
2. Configure Vercel to serve `/chatbot/frontend/` as static assets.
3. Update HTML files to:
   - Remove `disabled` from `.footer-chat-btn`
   - Add a script tag to load the widget JS
4. Ensure backend API endpoints have CORS enabled for your domain.
5. Continue using `environment.yml` for Python scripts; no `requirements.txt` needed unless pip support is required.

---

## 7. Future Considerations
- If you migrate the main site from GitHub Pages to Vercel, you can serve all static assets and APIs from one platform.
- The widget can be published as an npm package or CDN asset for easier reuse across multiple sites. 