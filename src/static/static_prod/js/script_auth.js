$(document).ready(function() {
    console.log('Ready')

    set_token_sent_class();
});

// handle resending token
function resendTokenHandle(btn) {
    let username = btn.attributes['username'].nodeValue
    let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    let data = {};
    data["csrfmiddlewaretoken"] = csrf_token;
    data['username'] = username
    const url = document.location.href;

    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        beforeSend: (xhr) => {
            xhr.setRequestHeader("X-CSRFToken", `${csrf_token}`);
        },
        success: (response) => {
            // console.log(sessionStorage);
            sessionStorage['activation_email_sent'] = true;
            token_sent_successfully();
            set_token_sent_class();
        },
        error: (response) => {
            console.log('Error');
            console.log(response);
            somethingWentWrong();
        }
    });
}

// set token sent class after sending token
function set_token_sent_class() {
    let elem = document.getElementsByClassName("token-expired-btn")[0];
    if (sessionStorage['activation_email_sent']) {
        elem.className += " token-expired-btn-disabled";
        elem.innerText = "Sent";
    }
}

function token_sent_successfully() {
    $.toast({ 
        heading: 'Token sent',
        icon: 'success',
        text: 'Token sent. Check your email',
        textAlign : 'left',
        textColor : '#fff',
        bgColor : '#0da114',
        hideAfter : 2000,
        stack : false,
        position : 'bottom-right',
        allowToastClose : true,
        showHideTransition : 'slide',
        loader: false,
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
