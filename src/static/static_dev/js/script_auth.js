$(document).ready(function() {
    console.log('Ready')

    set_token_sent_class();
});

function resendTokenHandle(btn) {
    let username = btn.attributes['username'].nodeValue

    let data = {};
    data["csrfmiddlewaretoken"] = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    data['username'] = username
    const url = document.location.href;

    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        success: (response) => {
            // console.log(sessionStorage);
            sessionStorage['activation_email_sent'] = true;
            set_token_sent_class();
        },
        error: (response) => {
            console.log('Error');
            console.log(response);
            somethingWentWrong();
        }
    });
}

function set_token_sent_class() {
    let elem = document.getElementsByClassName("token-expired-btn")[0];
    if (sessionStorage['activation_email_sent']) {
        elem.className += " token-expired-btn-disabled";
        elem.innerText = "Sent";
    }
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