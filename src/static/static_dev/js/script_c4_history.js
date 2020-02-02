$(document).ready(function() {
    blink_accept();

    console.log( "ready!" );
});


function blink_accept() {
    let games = document.getElementsByClassName("history-game-accept");
    let current = games[0].style.backgroundColor;
    let change = '#ffff74';
    for (let i = 0; i < games.length; ++i) {
        // let current_opacity = 0
        // setInterval(() => {
        //     current_opacity = Math.abs(current_opacity - 1)
        //     games[i].style.opacity = current_opacity;
        // }, 700);
        console.log(games[i])
    }

    // let current_opacity = 0
    // setInterval(() => {
    //     current_opacity = Math.abs(current_opacity - 0.8)
    //     current_turn_class.style.opacity = current_opacity;
    // }, 700);
}

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
        success: (data) => {
            if (data['status']) {
                document.location.reload();
            } else {
                somethingWentWrong();
            }
        },
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