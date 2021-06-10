$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
    $('.nav-item').on('click', function () {
        $('.nav-item.active').removeClass('active')
        $(this).addClass('active')
    });
});