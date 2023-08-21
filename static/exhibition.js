const editButtons = document.querySelectorAll('.edit-button');
editButtons.forEach(button => {
    button.addEventListener('click', event => {
        event.preventDefault();
        const commentId = button.getAttribute('data-comment-id');
        const editForm = document.getElementById(`edit-form-${commentId}`);
        const submitButton = editForm.querySelector('button[type="submit"]');

        if (submitButton.textContent = '수정') {
            editForm.style.display = 'block';
            submitButton.textContent = '수정완료';
            button.style.display = 'none'; // 수정 버튼 숨기기
        } else {
            editForm.style.display = 'none';
            submitButton.textContent = '수정';
            button.style.display = 'block'; // 수정 버튼 보이기
        }
    });
});