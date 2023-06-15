$(function() { // Dropdown toggle
  $('.dropdown-toggle').click(function() { $(this).next('.dropdown').slideToggle();
  });
  
  $(document).click(function(e) 
  { 
  var target = e.target; 
  if (!$(target).is('.dropdown-toggle') && !$(target).parents().is('.dropdown-toggle')) 
  //{ $('.dropdown').hide(); }
    { $('.dropdown').slideUp(); }
  });
  });

  // menu bar section
function toggleMenu (btn) {
  const el = btn.parentElement.querySelector('.subMenu')
  el.classList.toggle('hidden')
}
const btn = document.querySelector('.hasSubMenu')
btn.addEventListener('click', function(){
  toggleMenu(btn)
})
//menu bar section...

function toggleModal() {
  document.getElementById('modal').classList.toggle('hidden')
}

// search bar section 
$(".search_icon").click(function () {
  $(this).css({
      "color": "transparent"
  });
  $(".search_bar").show();
});
$(".cross_icon").click(function () {
  $(".search_bar").hide();
  $(".search_icon").css({
      "color": "#035E7B"
  });
});
//search bar section...