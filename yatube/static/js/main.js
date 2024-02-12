$(function ($){
$('body').on('submit', '.test', function (e){
    var that=this;
    e.preventDefault()
    $.ajax({
        type: this.method,
        url: this.action,
        data: $(this).serialize(),
        dataType:'json',
        success:
            function (response){
            if (response['status']==='OK'){
            $(that).closest('.raiting').find('.test2').replaceWith( '<div style="font-size: 20px" ' +
                'class="test2">'+response['new_raiting']+'</div>')}
            if (response['status']==='Repeated') {
                alert('Рейтинг можно менять только на 1')}
            if (response['status']==='NeOk') {alert('Для голосования необходимо авторизироваться')}
        }
    })
})
})

