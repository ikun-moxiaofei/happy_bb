function confirmDelete(postId) {
    if (window.confirm('确定要删除吗？')) {
        // 发送删除请求
        deletePost(postId);
    }
}

function deletePost(postId) {
    // 使用 AJAX 请求发送删除请求
    $.ajax({
        type: 'GET',
        url: '/post/delete_post/' + postId,
        success: function(response) {
            if (response.success) {
                alert('删除成功');
                window.location.href = '/'; // 返回首页
            } else {
                alert('删除成功，请返回首页');
            }
        },
        error: function(xhr, status, error) {
            console.error('AJAX请求错误：', error);
            alert('发生错误');
        }
    });
}
