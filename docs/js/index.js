$(document).ready(function(){
	
	// Scrollspy initiation
	$('body').scrollspy({ 
		target: '#scroll-spy',
		offset: 70
	});

	// On render, adjust body padding to ensure last Scroll target can reach top of screen
	var height = $('#howto').innerHeight();
	var windowHeight = $(window).height();
	var navHeight = $('nav.navbar').innerHeight();
	var siblingHeight = $('#howto').nextAll().innerHeight();


	if(height < windowHeight){
		$('body').css("padding-bottom", windowHeight-navHeight-height-siblingHeight + "px");
	}

	// On window resize, adjust body padding to ensure last Scroll target can reach top of screen
	$(window).resize(function(event){
		var height = $('#howto').innerHeight();
		var windowHeight = $(window).height();
		var navHeight = $('nav.navbar').innerHeight();
		var siblingHeight = $('#howto').nextAll().innerHeight();
		
		
		if(height < windowHeight){
			$('body').css("padding-bottom", windowHeight-navHeight-height-siblingHeight + "px");
		}
	});
	
	$('nav.navbar a, .scrollTop').click(function(event){
		// Make sure this.hash has a value before overriding default behavior
		if (this.hash !== "") {
			// Prevent default anchor click behavior
			event.preventDefault();

			// Store hash (#)
			var hash = this.hash;
			
			// Ensure no section has relevant class
			$('section').removeClass("focus");

			// Add class to target
			$(hash).addClass("focus");

			// Remove thy class after timeout
			setTimeout(function(){
				$(hash).removeClass("focus");
			}, 2000);			
			
    // Using jQuery's animate() method to add smooth page scroll
    // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area (the speed of the animation)
			$('html, body').animate({
				scrollTop: $(hash).offset().top - 69
			}, 600, function(){
				
				// Add hash (#) to URL when done scrolling (default click behavior)
				window.location.hash = hash;				
			});
					
			// Collapse Navbar for mobile view
			$(".navbar-collapse").collapse('hide');			
		}

	});
	$(window).scroll(function(){
		var scrollPos = $('body').scrollTop();
		if(scrollPos > 0){
			$('.navbar').addClass('show-color');
			$('.scrollTop').addClass('show-button');
		} else{
			$('.navbar').removeClass('show-color');
			$('.scrollTop').removeClass('show-button');
		}
		
	});
});