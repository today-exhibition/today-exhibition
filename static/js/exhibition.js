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
    
  // 공백 입력 방지
  const user_id = "{{ data.user_id | safe }}";

  function validateForm() {
    const commentTextarea = document.getElementById("comment");
    const commentContent = commentTextarea.value.trim();
    
    // 세션 로그인 여부 확인
    const isLoggedIn = user_id !== "";
    
    // 공백 입력 방지 (로그인된 경우에만)
    if (isLoggedIn && commentContent === "") {
      alert("내용을 입력해주세요.");
      return false;
    }

    return true;
  }

// 공유하기 버튼 (URL 클립보드 저장)
document.getElementById("shareLink").addEventListener("click", function(event) {
  event.preventDefault(); // 기본 링크 동작을 중지

  const url = window.location.href;

  if (navigator.clipboard) {
    navigator.clipboard.writeText(url)
      .then(function() {
        alert("클립보드에 복사되었습니다.");
      })
      .catch(function(error) {
        console.error("URL 복사 중 오류가 발생했습니다.", error);
      });
  } else {
    alert("현재 브라우저에서는 클립보드 복사를 지원하지 않습니다.");
  }
});

  