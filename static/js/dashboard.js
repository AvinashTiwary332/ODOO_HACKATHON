document.addEventListener("DOMContentLoaded", () => {
  const attendance = document.getElementById("attendanceChart");
  if (attendance) {
    new Chart(attendance, {
      type: "line",
      data: { labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], datasets: [{ label: "Present", data: [12, 16, 15, 19, 18, 11], borderColor: "#7c3aed", backgroundColor: "rgba(124,58,237,.12)", tension: .35, fill: true }] },
      options: { responsive: true, plugins: { legend: { display: false } } }
    });
  }
  const leave = document.getElementById("leaveChart");
  if (leave) {
    new Chart(leave, {
      type: "doughnut",
      data: { labels: ["Pending", "Approved", "Rejected"], datasets: [{ data: [leave.dataset.pending || 0, leave.dataset.approved || 0, leave.dataset.rejected || 0], backgroundColor: ["#f59e0b", "#10b981", "#ef4444"] }] },
      options: { responsive: true, cutout: "68%" }
    });
  }
});
