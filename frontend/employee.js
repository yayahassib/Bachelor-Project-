/**
 * Employee profile: ?id= → GET /employees/{id}, GET /interventions/{id}, add intervention.
 */
(function () {
  "use strict";

  var params = new URLSearchParams(window.location.search);
  var rawId = params.get("id");
  var employeeId = rawId && /^\d+$/.test(rawId) ? parseInt(rawId, 10) : null;

  var panelMissing = document.getElementById("panel-missing-id");
  var panelMain = document.getElementById("panel-main");
  var heading = document.getElementById("employee-heading");
  var fieldsEl = document.getElementById("employee-fields");
  var riskScoreDisplay = document.getElementById("risk-score-display");
  var riskLevelDisplay = document.getElementById("risk-level-display");
  var intTable = document.getElementById("interventions-table");
  var intBody = document.getElementById("interventions-body");
  var intEmpty = document.getElementById("interventions-empty");
  var form = document.getElementById("intervention-form");
  var dateInput = document.getElementById("date_applied");
  var btnSubmit = document.getElementById("btn-add-intervention");

  function todayISODate() {
    var d = new Date();
    var y = d.getFullYear();
    var m = String(d.getMonth() + 1).padStart(2, "0");
    var day = String(d.getDate()).padStart(2, "0");
    return y + "-" + m + "-" + day;
  }

  function row(label, value) {
    var dt = document.createElement("dt");
    dt.textContent = label;
    var dd = document.createElement("dd");
    dd.textContent = value == null || value === "" ? "—" : String(value);
    fieldsEl.appendChild(dt);
    fieldsEl.appendChild(dd);
  }

  function setEmployeeDetailsLinks(id) {
    var path = "/employee?id=" + encodeURIComponent(String(id));
    var nav = document.getElementById("nav-employee-details");
    var sub = document.getElementById("subnav-employee-details");
    if (nav) nav.href = path;
    if (sub) sub.href = path;
  }

  function renderEmployee(emp) {
    document.title = emp.full_name + " — Employee";
    heading.textContent = emp.full_name;
    fieldsEl.innerHTML = "";
    setEmployeeDetailsLinks(emp.id);

    if (typeof emp.risk_score === "number") {
      riskScoreDisplay.textContent = emp.risk_score.toFixed(4);
    } else {
      riskScoreDisplay.textContent = String(emp.risk_score);
    }
    riskLevelDisplay.textContent = emp.risk_level || "—";
    riskLevelDisplay.className = App.riskBadgeClass(emp.risk_level) || "badge";

    row("ID", emp.id);
    row("Age", emp.age);
    row("Department", emp.department);
    row("Job role", emp.job_role);
    row("Monthly income", emp.monthly_income);
    row("Distance from home", emp.distance_from_home);
    row("Years at company", emp.years_at_company);
    row("Job satisfaction", emp.job_satisfaction);
    row("Environment satisfaction", emp.environment_satisfaction);
    row("Work–life balance", emp.work_life_balance);
    row("Training (last year)", emp.training_times_last_year);
    row("Attendance score", emp.attendance_score);
    row("Task completion rate", emp.task_completion_rate);
    row("Onboarding feedback", emp.onboarding_feedback || "—");
  }

  function escapeHtml(s) {
    if (s == null) return "";
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  function renderInterventions(list) {
    intBody.innerHTML = "";
    if (!list || list.length === 0) {
      intTable.hidden = true;
      intEmpty.hidden = false;
      return;
    }
    intEmpty.hidden = true;
    intTable.hidden = false;
    list.forEach(function (inv) {
      var tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" +
        escapeHtml(inv.intervention_type) +
        "</td>" +
        "<td>" +
        escapeHtml(inv.date_applied) +
        "</td>" +
        "<td>" +
        escapeHtml(inv.notes || "—") +
        "</td>";
      intBody.appendChild(tr);
    });
  }

  function loadInterventions() {
    return App.getJson("/interventions/" + employeeId).then(function (data) {
      renderInterventions(data);
    });
  }

  function loadEmployee() {
    return App.getJson("/employees/" + employeeId).then(function (emp) {
      renderEmployee(emp);
    });
  }

  function loadAll() {
    App.clearAlerts();
    return loadEmployee()
      .then(function () {
        return loadInterventions();
      })
      .catch(function (e) {
        App.showAlert("error", e.message || String(e));
      });
  }

  if (!employeeId) {
    panelMissing.hidden = false;
  } else {
    if (dateInput) dateInput.value = todayISODate();
    panelMain.hidden = false;

    loadAll().catch(function () {});

    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        App.clearAlerts();
        var typeEl = document.getElementById("intervention_type");
        var notesEl = document.getElementById("intervention_notes");
        var typeVal = typeEl && typeEl.value ? typeEl.value.trim() : "";
        if (!typeVal) {
          App.showAlert("error", "Choose an intervention type.");
          return;
        }
        var payload = {
          employee_id: employeeId,
          intervention_type: typeVal,
          notes: notesEl && notesEl.value ? notesEl.value.trim() : "",
          date_applied: dateInput && dateInput.value ? dateInput.value : todayISODate(),
        };
        btnSubmit.disabled = true;
        App.postJson("/interventions", payload)
          .then(function () {
            App.showAlert("success", "Intervention added.");
            if (notesEl) notesEl.value = "";
            if (typeEl) typeEl.selectedIndex = 0;
            if (dateInput) dateInput.value = todayISODate();
            return loadInterventions();
          })
          .catch(function (err) {
            App.showAlert("error", err.message || String(err));
          })
          .finally(function () {
            btnSubmit.disabled = false;
          });
      });
    }
  }
})();
