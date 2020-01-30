is_my_turn = null;

$(document).ready(function() {
    current_turn_blink();
    current_duration();
    update_page();

    console.log('Ready')
    if (document.location.hash == '#just_won') {
        congratulate();
        document.location.hash = '';
    }
});

function congratulate() {
    $.toast({ 
        heading: 'You Won',
        icon: 'success',
        text: 'Congratulations. You won. Good job',
        textAlign : 'center',
        textColor : '#fff',
        bgColor : '#0da114',
        hideAfter : false,
        stack : false,
        position : 'mid-center',
        allowToastClose : true,
        showHideTransition : 'fade',
        loader: false,
    });
}


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
    }
    else if (data['just_won']) {
        document.location.hash = 'just_won'
        document.location.reload();
    } else {
        // швидкість менша при doc
        document.location.reload()
        // console.log(data);
        // document.open();
        // document.write(data);
        // document.close();
        // console.log('yep'); 
    }
}

function cellHandler(cell) {
    let data = {};
    data.x = parseInt(cell.attributes["x"].nodeValue);
    data.y = parseInt(cell.attributes["y"].nodeValue);
    data["csrfmiddlewaretoken"] = document.getElementsByName("csrfmiddlewaretoken")[0].value;
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
    // TODO - щоб дні виводило
    let game_duration = document.getElementsByClassName("game-duration-time")[0];
    let game_time = new Date(game_duration.innerText);

    let game_ended = document.getElementsByClassName("game-detail-map-ended");
    if (game_ended.length) {
        return;
    }

    setInterval(() => {
        let today = new Date();
        let diff = new Date(Math.abs(game_time - today));
        game_duration.innerText = datetime_with_leading_zeros(diff);
    }, 1000);
}

function datetime_with_leading_zeros(dt) {
    hours = ((dt.getHours() - 3) < 10 ? '0' : '') + (dt.getHours() - 3);
    minutes = (dt.getMinutes() < 10 ? '0' : '') + dt.getMinutes();
    seconds = (dt.getSeconds() < 10 ? '0' : '') + dt.getSeconds();
    return hours + ":" + minutes + ":" + seconds;
}


function update_page() {
    const url = document.location.href + 'my_move/';
    $.ajax({
        url: url,
        type: 'GET',
        success: (data => {
            is_my_turn = data['my_move'];
        }),
    });

    let id = 1;
    setInterval(() => {
        $.ajax({
            url: url,
            type: 'GET',
            success: (data) => {
                // console.log(id);
                // console.log(is_my_turn);
                // console.log(data);
                // console.log();
                id += 1;

                if (is_my_turn != data['my_move']) {
                    if (data['my_move'] = true) {
                        console.log('RELOAD');
                        document.location.reload();
                    }
                    is_my_turn = data['my_move'];
                }
            },
        });
    }, 5000);
}