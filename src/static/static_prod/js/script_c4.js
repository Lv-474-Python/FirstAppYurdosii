$(document).ready(function() {
    current_turn_blink();
    current_duration();

    console.log( "ready!" );
});

function ajax_success_handler(data) {
    if (data['errors']) {
        $.toast({ 
        heading: 'Error',
        icon: 'error',
        text: data['errors'],
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
    } else {
        console.log(data);
        document.open();
        document.write(data);
        document.close();
        console.log('yep'); 
    }
}

function cellHandler(cell) {
    let data = {};
    data.x = parseInt(cell.attributes["x"].nodeValue);
    data.y = parseInt(cell.attributes["y"].nodeValue);
    data["csrfmiddlewaretoken"] = document.getElementsByName("csrfmiddlewaretoken")[0].value;;
    const url = document.location.href;
    console.log(data)
    console.log(url)

    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        success: ajax_success_handler,
    });
}

function current_turn_blink() {
    let current_turn_class = document.getElementsByClassName("game-detail-move")[0];
    let current_opacity = 0
    setInterval(() => {
        current_opacity = Math.abs(current_opacity - 0.8)
        current_turn_class.style.opacity = current_opacity;
    }, 700);
}

function current_duration() {
    let game_duration = document.getElementsByClassName("game-duration-time")[0];
    let game_time = new Date(game_duration.innerText);
    console.log(game_time);

    setInterval(() => {
        let today = new Date();
        let diff = new Date(Math.abs(game_time - today));
        game_duration.innerText = datetime_with_leading_zeros(diff);
    }, 1000);
}

function datetime_with_leading_zeros(dt) {
    hours = ((dt.getHours() - 2) < 10 ? '0' : '') + (dt.getHours() - 2);
    minutes = (dt.getMinutes() < 10 ? '0' : '') + dt.getMinutes();
    seconds = (dt.getSeconds() < 10 ? '0' : '') + dt.getSeconds();
    return hours + ":" + minutes + ":" + seconds;
}
