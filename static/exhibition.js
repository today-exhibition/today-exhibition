// 수정 버튼 클릭에 따른 수정 버튼 및 코멘트 내용 숨김 처리
const editButtons = document.querySelectorAll('.edit-button');

editButtons.forEach(button => {
    button.addEventListener('click', event => {
        event.preventDefault();
        const commentId = button.getAttribute('data-comment-id');
        const editForm = document.getElementById(`edit-form-${commentId}`);
        const commentContent = document.getElementById(`comment-content-${commentId}`);
        const submitButton = editForm.querySelector('button[type="submit"]');
        
        if (submitButton.textContent = '수정') {
            editForm.style.display = 'block';
            commentContent.style.display = 'none';
            submitButton.textContent = '수정 완료';
            button.style.display = 'none';
        } else {
            submitButton.textContent = '수정';
            button.textContent = '수정';
        }
    });
});
