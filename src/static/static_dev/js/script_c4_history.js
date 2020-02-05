$(document).ready(function() {
    console.log( "ready!" );

});


function choiceGameHandler(btn) {
    let data = {};
    data["csrfmiddlewaretoken"] = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    data['game_pk'] = +btn.attributes['game_pk'].nodeValue;
    if (btn.attributes['accept']) {
        data['accept'] = +btn.attributes['accept'].nodeValue;
    }

    const url = document.location.href;
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        success: (response) => {
            document.location.reload();
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
    })
}