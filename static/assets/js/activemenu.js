document.querySelectorAll('#navmenu a').forEach(navmenu => {
    let location = window.location.pathname;
    let link = navmenu.getAttribute('href');
    if (location == link) {
        navmenu.setAttribute('class', 'active');
    }
});
