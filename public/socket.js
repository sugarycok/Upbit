const socket = io();

socket.on('connect', () => {
    console.log('서버에 연결되었습니다.');
    const sid = socket.id;
    $('#startForm').submit((event) => {
        event.preventDefault();
        const ticker = $('#ticker').val();
        $.ajax({
            url: '/start',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ ticker: ticker, sid: sid }),
            success: (data) => {
                console.log('Start response:', data);
            },
            error: (xhr, status, error) => {
                console.log(`Error: ${xhr.responseText}`);
            }
        });
    });
});

socket.on('disconnect', () => {
    console.log('서버와의 연결이 끊어졌습니다.');
});

socket.on('status_update', (data) => {
    const message = data.message;
    console.log('Status update received:', message); // 로그 추가
    $('#statusList').append(`<li class="neutral">${message}</li>`);
    const statusUpdates = document.getElementById('statusUpdates');
    statusUpdates.scrollTop = statusUpdates.scrollHeight;
});

socket.on('connect_error', (err) => {
    console.log('Connection Error:', err);
});

socket.on('error', (err) => {
    console.log('Error:', err);
});
