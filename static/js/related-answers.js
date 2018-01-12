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
            //var inf = jQuery.parseJSON(data);
            //var inf = JSON.parse(data);
            //alert(data['id']);
            var inf = data;

            var div01 = document.getElementById('thread-answer');
            div01.innerHTML += div01.firstElementChild.outerHTML;
            div01.lastElementChild.id = 'answer_id-' + inf.id;
            div01.lastElementChild.querySelector('#answer-create_date').textContent = "Jan. 12, 2018";
            div01.lastElementChild.querySelector('#answer-text').textContent = $('#textQuestion').val();
            $('#textQuestion').val('');
            /*var inf = data;

            var $newanswer = $('#answer_id-5').clone();
            $newanswer.attr('id', 'answer_id-' + inf.id);
            $newanswer.find('#answer-create_date').text(inf.createdate);
            $newanswer.find('#answer-text').text($('#textQuestion').val());
            $('#thread-answer').append($newanswer);
            $('#textQuestion').val('');*/
        });
    })
})();