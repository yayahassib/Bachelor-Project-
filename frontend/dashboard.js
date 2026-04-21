/**
 * Dashboard: employees table with filters, sort, and links to detail pages.
 */
(function () {
  "use strict";

  var statusEl = document.getElementById("api-status");
  var table = document.getElementById("employees-table");
  var tbody = document.getElementById("employees-body");
  var emptyEl = document.getElementById("employees-empty");
  var filterRisk = document.getElementById("filter-risk");
  var filterDepartment = document.getElementById("filter-department");
  var sortRisk = document.getElementById("sort-risk");
  var btnApply = document.getElementById("btn-apply");
  var btnRefresh = document.getElementById("btn-refresh");

  function escapeHtml(s) {
    if (s == null) return "";
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  function buildQueryString() {
    var params = new URLSearchParams();
    var rl = filterRisk && filterRisk.value ? filterRisk.value.trim() : "";
    if (rl) params.set("risk_level", rl);
    var dept = filterDepartment && filterDepartment.value
      ? filterDepartment.value.trim()
      : "";
    if (dept) params.set("department", dept);
    if (sortRisk && sortRisk.checked) params.set("sort_by_risk_score", "true");
    var s = params.toString();
    return s ? "?" + s : "";
  }

  function hasActiveFilters() {
    return !!(
      (filterRisk && filterRisk.value) ||
      (filterDepartment && filterDepartment.value.trim()) ||
      (sortRisk && sortRisk.checked)
    );
  }

  function renderRows(list) {
    tbody.innerHTML = "";
    if (!list || list.length === 0) {
      table.hidden = true;
      emptyEl.hidden = false;
      emptyEl.textContent = hasActiveFilters()
        ? "No employees match the current filters."
        : "No employees yet. Add one from the home page.";
      return;
    }
    emptyEl.hidden = true;
    table.hidden = false;
    list.forEach(function (emp) {
      var tr = document.createElement("tr");
      var riskCls = App.riskBadgeClass(emp.risk_level);
      var scoreText =
        typeof emp.risk_score === "number"
          ? emp.risk_score.toFixed(4)
          : escapeHtml(emp.risk_score);
      var detailUrl = "/employee?id=" + encodeURIComponent(String(emp.id));

      tr.innerHTML =
        "<td>" +
        escapeHtml(emp.full_name) +
        "</td>" +
        "<td>" +
        escapeHtml(emp.department) +
        "</td>" +
        "<td>" +
        scoreText +
        "</td>" +
        '<td><span class="' +
        riskCls +
        '">' +
        escapeHtml(emp.risk_level || "—") +
        "</span></td>" +
        '<td><a href="' +
        detailUrl +
        '">View details</a></td>';

      tbody.appendChild(tr);
    });
  }

  function loadHealth() {
    return App.getJson("/health")
      .then(function (d) {
        statusEl.textContent =
          "OK — " + (d.message || d.status || "connected");
      })
      .catch(function (e) {
        statusEl.textContent = "Error: " + e.message;
        App.showAlert("error", "Health check failed: " + e.message);
      });
  }

  function loadEmployees() {
    App.clearAlerts();
    var path = "/employees" + buildQueryString();
    return App.getJson(path)
      .then(function (data) {
        renderRows(data);
      })
      .catch(function (e) {
        App.showAlert("error", "Could not load employees: " + e.message);
        table.hidden = true;
        emptyEl.hidden = false;
        emptyEl.textContent = "Could not load employees.";
      });
  }

  function refresh() {
    loadHealth();
    loadEmployees();
  }

  if (btnApply) btnApply.addEventListener("click", loadEmployees);
  if (btnRefresh) btnRefresh.addEventListener("click", refresh);
  if (sortRisk)
    sortRisk.addEventListener("change", function () {
      loadEmployees();
    });

  refresh();
})();
