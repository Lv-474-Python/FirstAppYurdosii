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
        success: (data) => {
            if (data['status']) {
                user_row.innerText = 'Sent';
                user_row.className += '-sent';
                user_row.setAttribute('disabled', true);
                console.log(user_row.style);
                console.log(user_row);
                console.log(user_username);
                console.log(data)
            } else {
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
                })
            }
        },
    });
}