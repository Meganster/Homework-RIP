(function () {
    $('#add-answer').on('click', function () {
        var $this = $(this);
        var qid = $this.data('qid');
        var uid = $this.data('uid');
        console.log('qid: ' + qid, 'uid: ' + uid, 'text: ' + $('#textQuestion').val());

        $.post('/addanswer/', {
                text: $('#textQuestion').val(),
                user: uid,
                question: qid
            }
        ).done(function (data) {
            console.log(data);
            /*//var inf = jQuery.parseJSON(data);
            var inf = data;
            var p01 = document.getElementById('thread-answer');
            alert('#' + p01.firstElementChild.id);
            //var $newanswer = p01.firstElementChild.clone();
            $('#thread-answer').innerHTML += p01.firstElementChild.outerHTML;
            alert(inf.id);
            p01.lastElementChild.id = 'answer_id-'+inf.id;
            //p01.lastElementChild.find('#answer-create_date').text(inf.createdate);
            //p01.lastElementChild.find('#answer-text').text($('#textQuestion').val());
            //$('#thread-answer').append($newanswer);
            $('#textQuestion').val('');*/
            var inf = data;

            var $oldanswers = $('#answer_id-5').clone();
            $oldanswers.attr('id', 'answer_id-' + inf.id);
            $oldanswers.find('#answer-create_date').text(inf.createdate);
            $oldanswers.find('#answer-text').text($('#textQuestion').val());
            $('#thread-answer').append($oldanswers);
            $('#textQuestion').val('');
        });
    })
})();