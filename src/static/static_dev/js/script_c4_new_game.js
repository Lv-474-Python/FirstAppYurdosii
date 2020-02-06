// handle sending request to play
function requestNewGameHandler(user_row) {
    let user_username = user_row.attributes["user"].nodeValue;
    let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    const url = document.location.href;
    let data = {};
    data["csrfmiddlewaretoken"] = csrf_token;
    data['player_2_username'] = user_username;

    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        beforeSend: (xhr) => {
            xhr.setRequestHeader("X-CSRFToken", `${csrf_token}`);
        },
        success: (response) => {
            user_row.innerText = 'Request sent. Check your history';
            user_row.className += '-sent';
            user_row.setAttribute('disabled', true);
        },
        error: (response) => {
            somethingWentWrong();
        }
    });
}

function somethingWentWrong() {
    $.toast({ 
        heading: 'Error',
        icon: 'error',
        text: 'Something went wrong. Please reload page and try again.',
        textAlign : 'left',
        textColor : '#fff',
        bgColor : '#d90400',
        hideAfter : 2000,
        stack : 3,
        position : 'bottom-right',
        allowToastClose : true,
        showHideTransition : 'slide',
        loader: false,
    });
}
