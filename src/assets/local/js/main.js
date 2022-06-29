$(document).ready(function () {
    let isClose = false;
    $('#sidebarToggle').on('click', function () {
        isClose = !isClose
        $('#sidebarToggle').toggleClass('sidebarClose')
        $('#sidebarToggle svg').toggleClass('rotate')
        $('.sidebar').toggleClass('sidebarClose');
        $('.scrollbar > ul > li > a > i').toggleClass('bigger');
        $('.sidebarItem').toggleClass('hideSpan')
        $('.dropdownContent').removeClass('flex')
        $('.dropdownBtn').removeClass('isClicked')
        $('.dropdownItem').removeClass('display')
        $('.dropdownBtn > a > i').toggleClass('bigger')
        $('.dropdown-icon').toggleClass('d-none').removeClass('sidebarIcon')
    })

    dropdown = (element) => {
        if(!isClose){
            element.getElementsByClassName("dropdownBtn")[0].classList.toggle("isClicked")
            element.getElementsByClassName("dropdownContent")[0].classList.toggle("flex")
            element.getElementsByClassName("dropdown-icon")[0].classList.toggle("sidebarIcon")
            element.getElementsByClassName("dropdownItem")[0].classList.toggle("display")
        }
    }

    $('.treeTypes div a').on('click', function () {
        $('.treeTypes div a').removeClass('pressed')
        $(this).addClass('pressed')
    })

    $('.list').on('click', function () {
        $('.sidebar ul li ').removeClass('active')
        $(this).addClass('active')
    })

    $('.gj-icon').replaceWith("<i class=\"far fa-calendar-alt\"></i>")
})

