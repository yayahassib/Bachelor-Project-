/**
 * Shared helpers for the thesis frontend (vanilla JS, same origin as FastAPI).
 */
(function () {
  "use strict";

  window.App = {
    /** API base — empty string = same host as this page */
    apiBase: "",

    _networkErrorMessage:
      "Network error — cannot reach the server. From the project folder run: uvicorn main:app --reload",

    async _fetchSafe(path, init) {
      try {
        return await fetch(this.apiBase + path, init);
      } catch (e) {
        throw new Error(this._networkErrorMessage);
      }
    },

    _parseApiResponse(res, text) {
      let data;
      try {
        data = text ? JSON.parse(text) : null;
      } catch {
        throw new Error("Invalid JSON from server");
      }
      if (!res.ok) {
        const msg =
          data && data.detail
            ? typeof data.detail === "string"
              ? data.detail
              : JSON.stringify(data.detail)
            : res.statusText || "Request failed";
        throw new Error(msg);
      }
      return data;
    },

    /**
     * GET JSON from the API.
     * @param {string} path - e.g. "/employees"
     * @returns {Promise<any>}
     */
    async getJson(path) {
      const res = await this._fetchSafe(path);
      const text = await res.text();
      return this._parseApiResponse(res, text);
    },

    /**
     * POST JSON body.
     * @param {string} path
     * @param {object} body
     * @returns {Promise<any>}
     */
    async postJson(path, body) {
      const res = await this._fetchSafe(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const text = await res.text();
      return this._parseApiResponse(res, text);
    },

    /**
     * POST with no body (e.g. predict-risk trigger).
     * @param {string} path
     * @returns {Promise<any>}
     */
    async postEmpty(path) {
      const res = await this._fetchSafe(path, { method: "POST" });
      const text = await res.text();
      return this._parseApiResponse(res, text);
    },

    /**
     * Show a message inside [data-alert] or create a banner.
     * @param {"error"|"success"|"info"} type
     * @param {string} message
     * @param {HTMLElement} [container]
     */
    showAlert(type, message, container) {
      const host =
        container ||
        document.querySelector("[data-alert]") ||
        document.querySelector("main");
      if (!host) return;
      const el = document.createElement("div");
      el.className = "alert alert--" + type;
      el.setAttribute("role", "alert");
      el.textContent = message;
      const slot = host.querySelector("[data-alert]") || host;
      slot.insertBefore(el, slot.firstChild);
      return el;
    },

    clearAlerts(container) {
      const host = container || document.querySelector("main");
      if (!host) return;
      host.querySelectorAll(".alert").forEach(function (n) {
        n.remove();
      });
    },

    riskBadgeClass(level) {
      if (!level) return "";
      var l = String(level).toLowerCase();
      if (l === "low") return "badge badge--low";
      if (l === "medium") return "badge badge--medium";
      if (l === "high") return "badge badge--high";
      return "badge";
    },
  };
})();
