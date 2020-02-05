function requestNewGameHandler(user_row) {
    let user_username = user_row.attributes["user"].nodeValue;

    const url = document.location.href;
    let data = {};
    data["csrfmiddlewaretoken"] = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    data['player_2_username'] = user_username;

    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        success: (response) => {
            // console.log('success');
            // console.log(response);
            user_row.innerText = 'Request sent. Wait';
            user_row.className += '-sent';
            user_row.setAttribute('disabled', true);
        },
        error: (response) => {
            // console.log('error');
            // console.log(response);
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
