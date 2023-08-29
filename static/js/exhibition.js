function toggleEditForm(commentId) {
    const editForm = document.getElementById(`edit-form-${commentId}`);
    const commentContent = document.getElementById(`comment-content-${commentId}`);
    const editButton = document.querySelector(`.edit-button[data-comment-id="${commentId}"]`);
    const saveButton = document.querySelector(`.save-button[data-comment-id="${commentId}"]`);
    
    editForm.style.display = 'block';
    commentContent.style.display = 'none';
    editButton.style.display = 'none';
    saveButton.style.display = 'inline-block';
  }
  
  // 수정 버튼 이벤트 리스너 추가
  const editButtons = document.querySelectorAll('.edit-button');
  
  editButtons.forEach(button => {
    button.addEventListener('click', event => {
      event.preventDefault();
      const commentId = button.getAttribute('data-comment-id');
      toggleEditForm(commentId);
    });
  });
  
  // 수정 완료 버튼 클릭에 따른 처리
  function saveEditedComment(commentId) {
    const editForm = document.getElementById(`edit-form-${commentId}`);
    const commentContent = document.getElementById(`comment-content-${commentId}`);
    const editButton = document.querySelector(`.edit-button[data-comment-id="${commentId}"]`);
    const saveButton = document.querySelector(`.save-button[data-comment-id="${commentId}"]`);
    const editedContent = editForm.querySelector('textarea[name="edited_content"]').value;
    
    // 서버로 수정 내용 전송
    fetch(editForm.getAttribute('action'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `edited_content=${encodeURIComponent(editedContent)}`,
    })
    .then(response => {
        window.location.href = response.url;
      })
      .catch(error => {
        console.error('An error occurred:', error);
      });
      
  }
  