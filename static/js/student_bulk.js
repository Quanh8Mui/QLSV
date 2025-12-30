document.addEventListener("DOMContentLoaded", function () {

    const checkAll = document.getElementById("checkAll");
    const rowChecks = document.querySelectorAll(".row-check");

    if (!checkAll) return;

    // Check / uncheck all
    checkAll.addEventListener("change", function () {
        rowChecks.forEach(cb => cb.checked = checkAll.checked);
    });

    // Nếu bỏ chọn 1 dòng → bỏ checkAll
    rowChecks.forEach(cb => {
        cb.addEventListener("change", function () {
            if (!this.checked) {
                checkAll.checked = false;
            }
        });
    });

});
