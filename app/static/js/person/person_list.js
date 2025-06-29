function editPerson(personId) {
    window.location.href = `/manage/personal_info/edit/${personId}`;
}

function deletePerson(personId) {
    if (confirm('Are you sure you want to delete this person?')) {
        // Create a hidden form and submit as POST
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/manage/personal_info/delete/${personId}`;
        document.body.appendChild(form);
        form.submit();
    }
}

