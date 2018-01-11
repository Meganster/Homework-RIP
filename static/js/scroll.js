var inProgress = false;
var startFrom = 20;
$(window).scroll(function () {
    if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100 && !inProgress) {
        $.ajax({
            url: '/load/',
            method: 'get',
            data: {"start": startFrom},
            beforeSend: function () {
                inProgress = true;
            }
        }).done(function (data) {
            //data = jQuery.parseJSON(data);
            console.log(data);
            if (data.length > 0) {
                for(var i = 0; i < data.length; i++){
                    var inf = data[i];
                    var $newposts = $('#post_id-19').clone();
                    $newposts.attr('id', 'post_id-'+inf.id);
                    $newposts.find('#title').text(inf.title);
                    $newposts.find('#title').attr('href', '/question/'+inf.id);
                    $newposts.find('#post-text').text(inf.text);
                    $newposts.find('#score').text(inf.likes);
                    $newposts.find('#number_answers').text('Answer '+inf.number_answers);
                    $newposts.find('#number_answers').attr('href', '/question/'+inf.id);
                    $('#thread').append($newposts);
                }

                inProgress = false;
                startFrom += 4;
            }
        });
    }
});