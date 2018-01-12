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
            var inf = data;

            var $oldanswers = $('#answer_id-129').clone();
            $oldanswers.attr('id', 'answer_id-' + inf.id);
            $oldanswers.find('#answer-create_date').text(inf.createdate);
            $oldanswers.find('#answer-text').text($('#textQuestion').val());
            $('#thread-answer').append($oldanswers);
            $('#textQuestion').val(' ');
        });
    })
})();