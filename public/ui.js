$(document).ready(function() {
    console.log('UI script loaded');

    // 폼 제출 시 버튼 비활성화
    $('#startForm').on('submit', function(event) {
        $('#startForm button').prop('disabled', true);
        $('#startForm button').text('거래 시작 중...');
    });

    // 실시간 상태 업데이트 강조 표시 및 자동 스크롤
    socket.on('status_update', function(data) {
        const message = data.message;
        console.log('Status update received:', message); // 로그 추가
        const $newMessage = $(`<li class="neutral">${message}</li>`);
        $('#statusList').append($newMessage);

        // 새 메시지를 강조 표시
        $newMessage.css('background-color', '#dff0d8');
        setTimeout(() => {
            $newMessage.css('background-color', '');
        }, 2000);

        // 상태 업데이트 창을 자동으로 스크롤
        const statusUpdates = document.getElementById('statusUpdates');
        statusUpdates.scrollTop = statusUpdates.scrollHeight;
    });
});
