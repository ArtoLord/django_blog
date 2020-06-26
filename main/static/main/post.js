function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function postData(where, data, onSuccess) {
    data['csrfmiddlewaretoken'] = getCookie('csrftoken');
    console.log(data);
    $.ajax({
        url: where,
        type: 'POST',
        data: data,
        success: function (msg) {
            onSuccess()
        },
    });
}