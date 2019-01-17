$('.product').click(function() {
    let id = $(this).attr('data-id');
    window.location += id + '/';
});