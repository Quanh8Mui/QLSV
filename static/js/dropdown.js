document.addEventListener("DOMContentLoaded", function () {

    const faculty = document.getElementById("faculty");
    const major = document.getElementById("major");
    const classSelect = document.getElementById("class");

    faculty.addEventListener("change", function () {
        major.innerHTML = '<option value="">-- Chọn ngành --</option>';
        classSelect.innerHTML = '<option value="">-- Chọn lớp --</option>';

        if (!this.value) return;

        fetch(`/api/majors/${this.value}`)
            .then(res => res.json())
            .then(data => {
                data.forEach(m => {
                    major.innerHTML +=
                        `<option value="${m.id}">${m.name}</option>`;
                });
            });
    });

    major.addEventListener("change", function () {
        classSelect.innerHTML = '<option value="">-- Chọn lớp --</option>';

        if (!this.value) return;

        fetch(`/api/classes/${this.value}`)
            .then(res => res.json())
            .then(data => {
                data.forEach(c => {
                    classSelect.innerHTML +=
                        `<option value="${c.id}">${c.name}</option>`;
                });
            });
    });

});
